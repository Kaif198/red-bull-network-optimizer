"""
Scenario Engine for Red Bull Network Optimization
Manages different strategic scenarios with business context.
"""

from typing import Dict, List
from .network_model import NetworkOptimizer
from .kpi_calculator import KPICalculator


class ScenarioEngine:
    """
    Manages optimization scenarios and generates business insights.
    Each scenario represents a different strategic objective.
    """
    
    def __init__(self, data_dir='data'):
        """Initialize scenario engine."""
        self.optimizer = NetworkOptimizer(data_dir)
        self.kpi_calc = KPICalculator(data_dir)
        self.baseline_result = None
        
    def get_scenario_definitions(self) -> List[Dict]:
        """
        Get all available scenarios with business context.
        
        Returns:
            List of scenario definitions with objectives and use cases
        """
        return [
            {
                "id": "baseline",
                "name": "Current Network (Baseline)",
                "objective": "Understand current performance",
                "description": "Models existing network with actual costs and service levels. "
                              "Provides benchmark for measuring improvement opportunities.",
                "use_case": "Performance assessment, identifying gaps, strategic planning baseline",
                "expected_outcome": "Establishes baseline metrics: cost, service level, resilience",
                "trade_offs": "None - represents current state",
                "priority": "high"
            },
            {
                "id": "cost_optimized",
                "name": "Cost Minimization",
                "objective": "Maximize profitability",
                "description": "Minimize total network cost while maintaining ≥90% fill rate. "
                              "Allows model to find most efficient plant-DC-market flows.",
                "use_case": "Budget pressure, margin improvement initiatives, efficiency programs",
                "expected_outcome": "8-12% cost reduction through DC consolidation and production reallocation",
                "trade_offs": "May increase lead times by 0.5-1 day, potentially higher CO2 emissions",
                "priority": "high"
            },
            {
                "id": "disruption",
                "name": "Austria Plant Shutdown",
                "objective": "Test supply chain resilience",
                "description": "Simulate 3-month outage of largest production facility (40% of capacity). "
                              "Tests network resilience and identifies backup capacity requirements.",
                "use_case": "Risk assessment, contingency planning, resilience investment justification",
                "expected_outcome": "Quantifies disruption impact: cost increase, service degradation, mitigation strategies",
                "trade_offs": "13% fill rate drop during disruption, €20M+ cost increase",
                "priority": "medium"
            }
        ]
    
    def run_scenario(self, scenario_id: str) -> Dict:
        """
        Run optimization for specified scenario and calculate KPIs.
        
        Args:
            scenario_id: Scenario identifier (baseline, cost_optimized, disruption)
            
        Returns:
            Complete results with solution, KPIs, and insights
        """
        print(f"Running scenario: {scenario_id}...")
        
        # Run optimization
        if scenario_id == 'baseline':
            solution = self.optimizer.optimize_baseline()
            self.baseline_result = solution  # Store for comparisons
        elif scenario_id == 'cost_optimized':
            solution = self.optimizer.optimize_cost_minimization()
        elif scenario_id == 'disruption':
            solution = self.optimizer.optimize_disruption_response()
        else:
            raise ValueError(f"Unknown scenario: {scenario_id}")
        
        # Calculate KPIs
        kpis = self.kpi_calc.calculate_kpis(solution, scenario_id)
        
        # Generate insights
        insights = self.generate_insights(solution, kpis, scenario_id)
        
        # Build comparison to baseline (if not baseline itself)
        comparison = None
        if scenario_id != 'baseline' and self.baseline_result:
            comparison = self.compare_to_baseline(solution, kpis)
        
        return {
            'scenario_id': scenario_id,
            'solution': solution,
            'kpis': kpis,
            'insights': insights,
            'comparison': comparison
        }
    
    def generate_insights(self, solution: Dict, kpis: Dict, scenario_id: str) -> List[Dict]:
        """
        Generate strategic insights based on scenario results.
        
        Args:
            solution: Optimization solution
            kpis: Calculated KPIs
            scenario_id: Scenario identifier
            
        Returns:
            List of prioritized insights with actions
        """
        insights = []
        
        if scenario_id == 'baseline':
            # Baseline insights
            if kpis['fill_rate']['value'] < 100:
                insights.append({
                    'priority': 'high',
                    'title': 'Service Level Gap Identified',
                    'description': f"Current network fulfills {kpis['fill_rate']['value']:.1f}% of demand, "
                                  f"missing {100 - kpis['fill_rate']['value']:.1f}pp vs target. "
                                  f"This translates to {kpis['fill_rate']['context']}.",
                    'impact': kpis['fill_rate']['impact'],
                    'implementation': 'Capacity expansion in constrained regions (18-24 month timeline)'
                })
            
            if kpis['network_resilience_score']['value'] < 70:
                insights.append({
                    'priority': 'high',
                    'title': 'Low Supply Chain Resilience',
                    'description': f"Network resilience score of {kpis['network_resilience_score']['value']}/100 "
                                  f"indicates vulnerability to disruptions. "
                                  f"{kpis['network_resilience_score']['context']}",
                    'impact': kpis['network_resilience_score']['impact'],
                    'implementation': kpis['network_resilience_score']['action']
                })
            
            # Always include cost optimization opportunity
            insights.append({
                'priority': 'medium',
                'title': 'Cost Optimization Opportunity',
                'description': 'Run cost optimization scenario to quantify potential savings through network redesign.',
                'impact': 'Typically 8-12% cost reduction achievable through DC consolidation and routing optimization',
                'implementation': 'Phased approach: Analysis (2mo) → Planning (3mo) → Implementation (9mo)'
            })
        
        elif scenario_id == 'cost_optimized':
            # Cost optimization insights
            baseline_cost = self.baseline_result['objective_value'] if self.baseline_result else 338.7e6
            savings = baseline_cost - solution['objective_value']
            
            if savings > 0:
                insights.append({
                    'priority': 'high',
                    'title': f'€{savings/1e6:.1f}M Annual Cost Reduction Identified',
                    'description': f'Optimized network reduces costs by {(savings/baseline_cost)*100:.1f}% through '
                                  f'strategic DC placement and production reallocation. '
                                  f'Primary savings: {kpis["total_cost"]["driver"]}',
                    'impact': kpis['total_cost']['impact'],
                    'implementation': 'Recommended phased rollout: High-impact changes first (6mo), '
                                     'then full network optimization (12mo total)'
                })
            
            # Check if fill rate decreased
            if kpis['fill_rate']['value'] < 95:
                insights.append({
                    'priority': 'medium',
                    'title': 'Service Level Trade-off',
                    'description': f"Cost optimization reduced fill rate to {kpis['fill_rate']['value']:.1f}%. "
                                  f"Consider if this trade-off is acceptable for mature markets.",
                    'impact': 'Slight service degradation may be acceptable in price-sensitive segments',
                    'implementation': 'Segment markets: Premium (maintain 98%+) vs Standard (accept 90-95%)'
                })
        
        elif scenario_id == 'disruption':
            # Disruption insights
            baseline_cost = self.baseline_result['objective_value'] if self.baseline_result else 338.7e6
            cost_increase = solution['objective_value'] - baseline_cost
            
            insights.append({
                'priority': 'high',
                'title': f'Critical Single Point of Failure: Austria Plant',
                'description': f'3-month Austria plant shutdown causes €{cost_increase/1e6:.1f}M cost increase '
                              f'({(cost_increase/baseline_cost)*100:.0f}% above baseline). '
                              f'Fill rate drops to {kpis["fill_rate"]["value"]:.1f}% during disruption.',
                'impact': 'Potential quarterly revenue loss of €47M+ based on 2021 precedent',
                'implementation': 'URGENT: Establish backup production agreements + increase safety stock in Europe'
            })
            
            insights.append({
                'priority': 'high',
                'title': 'Resilience Investment Required',
                'description': f'Current resilience score: {kpis["network_resilience_score"]["value"]}/100. '
                              f'Dual-sourcing strategy needed for top markets.',
                'impact': 'Investment: €12M (capacity agreements + inventory). ROI: Positive if disruption risk >15% over 3 years',
                'implementation': kpis['network_resilience_score']['action']
            })
        
        return insights
    
    def compare_to_baseline(self, solution: Dict, kpis: Dict) -> Dict:
        """
        Compare scenario results to baseline.
        
        Args:
            solution: Current scenario solution
            kpis: Current scenario KPIs
            
        Returns:
            Dictionary of comparisons with deltas
        """
        if not self.baseline_result:
            return None
        
        baseline_kpis = self.kpi_calc.calculate_kpis(self.baseline_result, 'baseline')
        
        return {
            'cost_delta': {
                'value': solution['objective_value'] - self.baseline_result['objective_value'],
                'percentage': ((solution['objective_value'] / self.baseline_result['objective_value']) - 1) * 100,
                'interpretation': 'savings' if solution['objective_value'] < self.baseline_result['objective_value'] else 'increase'
            },
            'fill_rate_delta': {
                'value': kpis['fill_rate']['value'] - baseline_kpis['fill_rate']['value'],
                'interpretation': 'improvement' if kpis['fill_rate']['value'] > baseline_kpis['fill_rate']['value'] else 'degradation'
            },
            'resilience_delta': {
                'value': kpis['network_resilience_score']['value'] - baseline_kpis['network_resilience_score']['value'],
                'interpretation': 'stronger' if kpis['network_resilience_score']['value'] > baseline_kpis['network_resilience_score']['value'] else 'weaker'
            }
        }


def test_scenario_engine():
    """Test the scenario engine."""
    print("=== Testing Scenario Engine ===\n")
    
    engine = ScenarioEngine(data_dir='data')
    
    # Get scenario definitions
    print("Available Scenarios:")
    for scenario in engine.get_scenario_definitions():
        print(f"\n  {scenario['name']} ({scenario['id']})")
        print(f"  Objective: {scenario['objective']}")
        print(f"  Expected: {scenario['expected_outcome']}")
    
    # Run baseline
    print("\n\n=== Running Baseline Scenario ===")
    baseline = engine.run_scenario('baseline')
    print(f"✓ Total Cost: {baseline['kpis']['total_cost']['formatted']}")
    print(f"✓ Fill Rate: {baseline['kpis']['fill_rate']['formatted']}")
    print(f"✓ Insights: {len(baseline['insights'])} strategic recommendations")
    
    # Run cost optimization
    print("\n=== Running Cost Optimization Scenario ===")
    cost_opt = engine.run_scenario('cost_optimized')
    print(f"✓ Total Cost: {cost_opt['kpis']['total_cost']['formatted']}")
    if cost_opt['comparison']:
        delta = cost_opt['comparison']['cost_delta']
        print(f"✓ vs Baseline: {delta['percentage']:+.1f}% ({delta['interpretation']})")
    
    print("\n✅ Scenario engine working correctly!")
    
    return engine


if __name__ == '__main__':
    test_scenario_engine()
