/**
 * Red Bull Network Optimizer - Main Application Logic
 */

const API_BASE = window.location.origin;

// State management
let currentScenario = 'baseline';
let scenarioResults = {};

// Initialize application on page load
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    loadInitialData();
});

/**
 * Initialize navigation between sections
 */
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.dashboard-section');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetSection = this.dataset.section;
            
            // Update active nav button
            navButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show target section
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });
        });
    });
}

/**
 * Load initial KPI data on page load
 */
async function loadInitialData() {
    try {
        const response = await fetch(`${API_BASE}/api/kpis`);
        const data = await response.json();
        
        if (data.success) {
            updateKPICards(data.kpis);
        }
    } catch (error) {
        console.error('Error loading initial data:', error);
        showErrorMessage('Unable to load dashboard data. Please refresh the page.');
    }
}

/**
 * Update KPI cards with data
 */
function updateKPICards(kpis) {
    // Total Cost
    document.getElementById('kpi-cost-value').textContent = kpis.total_cost.formatted;
    document.getElementById('kpi-cost-trend').textContent = kpis.total_cost.vs_optimal;
    document.getElementById('kpi-cost-impact').textContent = kpis.total_cost.impact;
    document.getElementById('kpi-cost-action').textContent = '→ ' + kpis.total_cost.action;
    
    // Fill Rate
    document.getElementById('kpi-fillrate-value').textContent = kpis.fill_rate.formatted;
    document.getElementById('kpi-fillrate-trend').textContent = kpis.fill_rate.vs_target;
    document.getElementById('kpi-fillrate-trend').className = kpis.fill_rate.value >= 95 ? 'trend positive' : 'trend negative';
    document.getElementById('kpi-fillrate-impact').textContent = kpis.fill_rate.impact;
    document.getElementById('kpi-fillrate-action').textContent = '→ ' + kpis.fill_rate.action;
    
    // Lead Time
    document.getElementById('kpi-leadtime-value').textContent = kpis.avg_lead_time.formatted;
    document.getElementById('kpi-leadtime-trend').textContent = kpis.avg_lead_time.vs_competitor;
    document.getElementById('kpi-leadtime-impact').textContent = kpis.avg_lead_time.impact;
    document.getElementById('kpi-leadtime-action').textContent = '→ ' + kpis.avg_lead_time.action;
    
    // CO2
    document.getElementById('kpi-co2-value').textContent = kpis.co2_emissions.formatted;
    document.getElementById('kpi-co2-trend').textContent = kpis.co2_emissions.vs_target;
    document.getElementById('kpi-co2-impact').textContent = kpis.co2_emissions.impact;
    document.getElementById('kpi-co2-action').textContent = '→ ' + kpis.co2_emissions.action;
    
    // Update resilience score if on insights page
    if (document.getElementById('resilience-score')) {
        document.getElementById('resilience-score').textContent = kpis.network_resilience_score.value;
        document.getElementById('resilience-context').textContent = kpis.network_resilience_score.context;
    }
}

/**
 * Run optimization scenario
 */
async function runScenario(scenarioId) {
    currentScenario = scenarioId;
    
    // Show loading state
    document.getElementById('optimization-status').classList.remove('hidden');
    document.getElementById('scenario-results').classList.add('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/api/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ scenario_id: scenarioId })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Optimization failed');
        }
        
        // Store results
        scenarioResults[scenarioId] = data;
        
        // Hide loading, show results
        document.getElementById('optimization-status').classList.add('hidden');
        document.getElementById('scenario-results').classList.remove('hidden');
        
        // Update displays
        updateKPICards(data.kpis);
        updateComparisonTable(data);
        updateRecommendations(data.insights);
        
        // Trigger chart updates if charts.js is loaded
        if (typeof updateChartsWithScenario === 'function') {
            updateChartsWithScenario(data);
        }
        
        showSuccessMessage(`${scenarioId.toUpperCase()} scenario completed successfully!`);
        
    } catch (error) {
        console.error('Optimization error:', error);
        document.getElementById('optimization-status').classList.add('hidden');
        showErrorMessage(`Optimization failed: ${error.message}`);
    }
}

/**
 * Update comparison table with scenario results
 */
function updateComparisonTable(data) {
    const tbody = document.getElementById('comparison-table-body');
    tbody.innerHTML = '';
    
    const kpis = data.kpis;
    
    // Get baseline values (if available)
    const baseline = scenarioResults['baseline'];
    const baselineCost = baseline ? baseline.kpis.total_cost.formatted : '€338.7M';
    const baselineFill = baseline ? baseline.kpis.fill_rate.formatted : '100.0%';
    
    const metrics = [
        {
            name: 'Total Cost',
            baseline: baselineCost,
            current: kpis.total_cost.formatted,
            change: kpis.total_cost.vs_optimal,
            impact: kpis.total_cost.impact
        },
        {
            name: 'Fill Rate',
            baseline: baselineFill,
            current: kpis.fill_rate.formatted,
            change: kpis.fill_rate.vs_target,
            impact: kpis.fill_rate.impact
        },
        {
            name: 'Resilience Score',
            baseline: '80/100',
            current: kpis.network_resilience_score.formatted,
            change: kpis.network_resilience_score.vs_benchmark,
            impact: kpis.network_resilience_score.context
        }
    ];
    
    metrics.forEach(metric => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${metric.name}</strong></td>
            <td>${metric.baseline}</td>
            <td class="highlight">${metric.current}</td>
            <td>${metric.change}</td>
            <td>${metric.impact}</td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Update recommendations panel
 */
function updateRecommendations(insights) {
    const container = document.getElementById('recommendations-list');
    container.innerHTML = '';
    
    if (!insights || insights.length === 0) {
        container.innerHTML = '<p>No specific recommendations for this scenario.</p>';
        return;
    }
    
    insights.forEach(insight => {
        const card = document.createElement('div');
        card.className = `insight-card priority-${insight.priority}`;
        card.innerHTML = `
            <span class="priority-badge">${insight.priority.toUpperCase()}</span>
            <h4>${insight.title}</h4>
            <p>${insight.description}</p>
            <p style="margin-top:10px;"><strong>Expected Impact:</strong> ${insight.impact}</p>
            <p><strong>Implementation:</strong> ${insight.implementation}</p>
        `;
        container.appendChild(card);
    });
}

/**
 * Export scenario results to Excel
 */
async function exportExcel() {
    if (!currentScenario) {
        showErrorMessage('Please run a scenario first before exporting.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/export-excel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ scenario_id: currentScenario })
        });
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        // Trigger download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `red_bull_network_analysis_${currentScenario}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        
        showSuccessMessage('Excel file downloaded successfully!');
        
    } catch (error) {
        console.error('Export error:', error);
        showErrorMessage('Failed to export Excel file. Please try again.');
    }
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #F44336;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
