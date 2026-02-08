/**
 * Chart.js Visualizations for Red Bull Network Optimizer
 * Business-focused charts with contextual insights
 */

// Store chart instances
let charts = {};

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeCostBreakdownChart();
    initializeProductionChart();
});

/**
 * Initialize cost breakdown doughnut chart
 */
function initializeCostBreakdownChart() {
    const ctx = document.getElementById('cost-breakdown-chart');
    if (!ctx) return;
    
    charts.costBreakdown = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: [
                'Production',
                'Transport (Plant→DC)',
                'Transport (DC→Market)',
                'Warehousing',
                'Unmet Demand Penalty'
            ],
            datasets: [{
                data: [99.6, 112.1, 53.5, 72.8, 0.7],
                backgroundColor: [
                    '#DB0A40',  // Red Bull Red
                    '#FFCC00',  // Red Bull Yellow
                    '#005EB8',  // Blue
                    '#333333',  // Dark gray
                    '#CCCCCC'   // Light gray
                ],
                borderWidth: 3,
                borderColor: '#FFF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { size: 13 },
                        padding: 15,
                        usePointStyle: true,
                        generateLabels: function(chart) {
                            const data = chart.data;
                            const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                            return data.labels.map((label, i) => {
                                const value = data.datasets[0].data[i];
                                const pct = ((value / total) * 100).toFixed(1);
                                return {
                                    text: `${label} (${pct}%)`,
                                    fillStyle: data.datasets[0].backgroundColor[i],
                                    hidden: false,
                                    index: i
                                };
                            });
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(10, 10, 10, 0.9)',
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((value / total) * 100).toFixed(1);
                            return `${label}: €${value}M (${pct}%)`;
                        },
                        afterLabel: function(context) {
                            const insights = [
                                'Lowest cost component - economies of scale',
                                'Largest cost driver - optimization target',
                                'Last-mile delivery - regional efficiency',
                                'Fixed DC costs - consolidation opportunity',
                                'Service gaps - capacity constraints'
                            ];
                            return insights[context.dataIndex];
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize production utilization bar chart
 */
function initializeProductionChart() {
    const ctx = document.getElementById('production-chart');
    if (!ctx) return;
    
    charts.production = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['Austria\n(500M capacity)', 'USA\n(300M capacity)', 'Brazil\n(200M capacity)', 'Thailand\n(250M capacity)'],
            datasets: [{
                label: 'Current Production',
                data: [457.6, 274.9, 183.3, 228.2],
                backgroundColor: '#DB0A40',
                borderRadius: 6
            }, {
                label: 'Available Capacity',
                data: [42.4, 25.1, 16.7, 21.8],
                backgroundColor: '#CCCCCC',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true,
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    max: 500,
                    title: {
                        display: true,
                        text: 'Production Volume (M units/year)',
                        font: { size: 13, weight: 'bold' }
                    },
                    ticks: {
                        callback: function(value) {
                            return value + 'M';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: { font: { size: 12 }, padding: 15 }
                },
                tooltip: {
                    backgroundColor: 'rgba(10, 10, 10, 0.9)',
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + 'M units';
                        },
                        footer: function(tooltipItems) {
                            const idx = tooltipItems[0].dataIndex;
                            const capacity = [500, 300, 200, 250][idx];
                            const production = tooltipItems[0].parsed.y;
                            const utilization = ((production / capacity) * 100).toFixed(1);
                            return `Utilization: ${utilization}%`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create comparison charts for scenario analysis
 */
function createComparisonCharts(baselineData, scenarioData) {
    // Cost Comparison Chart
    const costCtx = document.getElementById('cost-comparison-chart');
    if (costCtx && charts.costComparison) {
        charts.costComparison.destroy();
    }
    
    if (costCtx) {
        const baselineCost = baselineData.solution_summary.cost_breakdown;
        const scenarioCost = scenarioData.solution_summary.cost_breakdown;
        
        charts.costComparison = new Chart(costCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Production', 'Transport\n(P→DC)', 'Transport\n(DC→M)', 'Warehousing', 'Unmet\nPenalty'],
                datasets: [{
                    label: 'Baseline',
                    data: [
                        baselineCost.production / 1e6,
                        baselineCost.transport_plant_dc / 1e6,
                        baselineCost.transport_dc_market / 1e6,
                        baselineCost.warehousing / 1e6,
                        baselineCost.unmet_penalty / 1e6
                    ],
                    backgroundColor: '#CCCCCC',
                    borderRadius: 4
                }, {
                    label: 'Optimized',
                    data: [
                        scenarioCost.production / 1e6,
                        scenarioCost.transport_plant_dc / 1e6,
                        scenarioCost.transport_dc_market / 1e6,
                        scenarioCost.warehousing / 1e6,
                        scenarioCost.unmet_penalty / 1e6
                    ],
                    backgroundColor: '#DB0A40',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cost (€M)',
                            font: { size: 12, weight: 'bold' }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { size: 12 } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 10, 10, 0.9)',
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': €' + context.parsed.y.toFixed(1) + 'M';
                            }
                        }
                    }
                }
            }
        });
        
        // Update insight text
        const totalBaseline = Object.values(baselineCost).reduce((a, b) => a + b, 0) / 1e6;
        const totalScenario = Object.values(scenarioCost).reduce((a, b) => a + b, 0) / 1e6;
        const savings = totalBaseline - totalScenario;
        const savingsPct = (savings / totalBaseline * 100).toFixed(1);
        
        const insightEl = document.getElementById('cost-insight');
        if (insightEl) {
            if (savings > 0) {
                insightEl.innerHTML = `<strong>Cost Reduction:</strong> €${savings.toFixed(1)}M savings (${savingsPct}%) through optimized routing and DC allocation. Primary driver: ${savings > 20 ? 'production reallocation' : 'transportation efficiency'}.`;
            } else if (savings < -10) {
                insightEl.innerHTML = `<strong>Cost Increase:</strong> €${Math.abs(savings).toFixed(1)}M increase due to disruption impact. Network operating under constrained capacity.`;
            } else {
                insightEl.innerHTML = `<strong>Cost Neutral:</strong> Current configuration already near-optimal given constraints. Focus on service level improvements.`;
            }
        }
    }
    
    // Service Level Comparison
    const serviceCtx = document.getElementById('service-comparison-chart');
    if (serviceCtx && charts.serviceComparison) {
        charts.serviceComparison.destroy();
    }
    
    if (serviceCtx) {
        const baselineFill = baselineData.kpis.fill_rate.value;
        const scenarioFill = scenarioData.kpis.fill_rate.value;
        
        charts.serviceComparison = new Chart(serviceCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Fill Rate', 'Target (100%)'],
                datasets: [{
                    label: 'Baseline',
                    data: [baselineFill, 100],
                    backgroundColor: '#CCCCCC',
                    borderRadius: 4
                }, {
                    label: 'Scenario',
                    data: [scenarioFill, 100],
                    backgroundColor: scenarioFill >= 95 ? '#4CAF50' : scenarioFill >= 90 ? '#FFCC00' : '#DB0A40',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 105,
                        title: {
                            display: true,
                            text: 'Fill Rate (%)',
                            font: { size: 12, weight: 'bold' }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { size: 12 } }
                    }
                }
            }
        });
        
        const serviceInsightEl = document.getElementById('service-insight');
        if (serviceInsightEl) {
            const delta = scenarioFill - baselineFill;
            if (delta > 0) {
                serviceInsightEl.innerHTML = `<strong>Service Improvement:</strong> Fill rate increased by ${delta.toFixed(1)}pp through capacity optimization.`;
            } else if (delta < -5) {
                serviceInsightEl.innerHTML = `<strong>Service Trade-off:</strong> Fill rate decreased by ${Math.abs(delta).toFixed(1)}pp. Assess if cost savings justify service degradation.`;
            } else {
                serviceInsightEl.innerHTML = `<strong>Service Maintained:</strong> Optimization preserves service levels while reducing costs.`;
            }
        }
    }
}

/**
 * Update charts with new scenario data
 */
function updateChartsWithScenario(data) {
    // Update cost breakdown if scenario has cost data
    if (data.solution_summary && data.solution_summary.cost_breakdown) {
        const breakdown = data.solution_summary.cost_breakdown;
        
        if (charts.costBreakdown) {
            charts.costBreakdown.data.datasets[0].data = [
                breakdown.production / 1e6,
                breakdown.transport_plant_dc / 1e6,
                breakdown.transport_dc_market / 1e6,
                breakdown.warehousing / 1e6,
                breakdown.unmet_penalty / 1e6
            ];
            charts.costBreakdown.update();
        }
    }
    
    // Create comparison charts if we have baseline
    if (scenarioResults['baseline'] && data.scenario_id !== 'baseline') {
        createComparisonCharts(scenarioResults['baseline'], data);
    }
}

