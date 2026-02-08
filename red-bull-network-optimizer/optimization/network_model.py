"""
Red Bull Network Optimization Model
Uses linear programming to minimize total network cost while meeting demand constraints.
"""

import pulp
import pandas as pd
from typing import Dict, Tuple
import os

class NetworkOptimizer:
    """
    Optimizes Red Bull's global distribution network using linear programming.
    
    Objective: Minimize total cost (production + transportation + warehousing + unmet demand penalty)
    Constraints: Capacity limits, flow conservation, demand fulfillment
    """
    
    def __init__(self, data_dir='data'):
        """Initialize optimizer with network data."""
        self.data_dir = data_dir
        self.load_data()
        
    def load_data(self):
        """Load network data from CSV files."""
        self.plants = pd.read_csv(os.path.join(self.data_dir, 'plants.csv'))
        self.dcs = pd.read_csv(os.path.join(self.data_dir, 'distribution_centers.csv'))
        self.markets = pd.read_csv(os.path.join(self.data_dir, 'markets.csv'))
        self.routes = pd.read_csv(os.path.join(self.data_dir, 'transportation.csv'))
        
    def optimize_baseline(self) -> Dict:
        """
        Baseline scenario: Current network configuration.
        No artificial constraints - pure cost minimization with all facilities available.
        """
        return self._run_optimization(scenario_name="baseline", constraints={})
    
    def optimize_cost_minimization(self) -> Dict:
        """
        Cost optimization scenario: Minimize total cost while maintaining ≥90% fill rate.
        Allows model to find most efficient plant-DC-market flows.
        """
        return self._run_optimization(
            scenario_name="cost_optimized",
            constraints={'min_fill_rate': 0.90}
        )
    
    def optimize_disruption_response(self) -> Dict:
        """
        Disruption scenario: Austria plant (P1) completely offline.
        Tests network resilience and identifies backup capacity requirements.
        """
        return self._run_optimization(
            scenario_name="disruption",
            constraints={'disabled_plants': ['P1']}
        )
    
    def _run_optimization(self, scenario_name: str, constraints: Dict) -> Dict:
        """
        Core optimization engine using PuLP.
        
        Args:
            scenario_name: Identifier for the scenario
            constraints: Additional constraints (disabled plants, min fill rate, etc.)
            
        Returns:
            Dictionary containing solution, costs, flows, and KPIs
        """
        # Create the optimization problem
        prob = pulp.LpProblem(f"RedBull_Network_{scenario_name}", pulp.LpMinimize)
        
        # Decision variables
        production = {}  # How much to produce at each plant
        plant_to_dc = {}  # Flow from plants to DCs
        dc_to_market = {}  # Flow from DCs to markets
        unmet_demand = {}  # Demand not fulfilled (penalized)
        
        # Production variables
        for _, plant in self.plants.iterrows():
            plant_id = plant['plant_id']
            production[plant_id] = pulp.LpVariable(
                f"production_{plant_id}",
                lowBound=0,
                upBound=plant['capacity_annual_millions'] * 1e6,  # Convert to units
                cat='Continuous'
            )
        
        # Plant to DC flow variables
        for _, route in self.routes[self.routes['from_type'] == 'plant'].iterrows():
            key = (route['from_id'], route['to_id'])
            plant_to_dc[key] = pulp.LpVariable(
                f"flow_P_{route['from_id']}_to_{route['to_id']}",
                lowBound=0,
                cat='Continuous'
            )
        
        # DC to Market flow variables
        for _, route in self.routes[self.routes['from_type'] == 'dc'].iterrows():
            key = (route['from_id'], route['to_id'])
            dc_to_market[key] = pulp.LpVariable(
                f"flow_DC_{route['from_id']}_to_{route['to_id']}",
                lowBound=0,
                cat='Continuous'
            )
        
        # Unmet demand variables
        for _, market in self.markets.iterrows():
            market_id = market['market_id']
            unmet_demand[market_id] = pulp.LpVariable(
                f"unmet_{market_id}",
                lowBound=0,
                upBound=market['annual_demand_millions'] * 1e6,
                cat='Continuous'
            )
        
        # OBJECTIVE FUNCTION: Minimize total cost
        production_cost = pulp.lpSum([
            production[p['plant_id']] * p['cost_per_unit_eur']
            for _, p in self.plants.iterrows()
        ])
        
        transport_cost_plant_dc = pulp.lpSum([
            plant_to_dc[(r['from_id'], r['to_id'])] * r['cost_per_unit_eur']
            for _, r in self.routes[self.routes['from_type'] == 'plant'].iterrows()
        ])
        
        transport_cost_dc_market = pulp.lpSum([
            dc_to_market[(r['from_id'], r['to_id'])] * r['cost_per_unit_eur']
            for _, r in self.routes[self.routes['from_type'] == 'dc'].iterrows()
        ])
        
        warehousing_cost = pulp.lpSum([
            # Fixed monthly cost * 12 months + variable cost per unit flowing through
            (dc['fixed_cost_monthly_eur'] * 12) + 
            pulp.lpSum([
                dc_to_market.get((dc['dc_id'], m['market_id']), 0) * dc['variable_cost_per_unit_eur']
                for _, m in self.markets.iterrows()
            ])
            for _, dc in self.dcs.iterrows()
        ])
        
        # Unmet demand penalty (€5 per unit = lost revenue + brand damage)
        unmet_penalty = pulp.lpSum([
            unmet_demand[m['market_id']] * 5.0
            for _, m in self.markets.iterrows()
        ])
        
        prob += (production_cost + transport_cost_plant_dc + 
                transport_cost_dc_market + warehousing_cost + unmet_penalty), "Total_Cost"
        
        # CONSTRAINTS
        
        # 1. Plant capacity constraints
        for _, plant in self.plants.iterrows():
            plant_id = plant['plant_id']
            
            # Check if plant is disabled in this scenario
            if 'disabled_plants' in constraints and plant_id in constraints['disabled_plants']:
                prob += production[plant_id] == 0, f"Disabled_{plant_id}"
            else:
                prob += production[plant_id] <= plant['capacity_annual_millions'] * 1e6, \
                        f"Capacity_{plant_id}"
        
        # 2. Flow conservation at plants: production = outflow
        for _, plant in self.plants.iterrows():
            plant_id = plant['plant_id']
            outflow = pulp.lpSum([
                plant_to_dc.get((plant_id, dc['dc_id']), 0)
                for _, dc in self.dcs.iterrows()
            ])
            prob += production[plant_id] == outflow, f"Plant_balance_{plant_id}"
        
        # 3. Flow conservation at DCs: inflow = outflow
        for _, dc in self.dcs.iterrows():
            dc_id = dc['dc_id']
            inflow = pulp.lpSum([
                plant_to_dc.get((p['plant_id'], dc_id), 0)
                for _, p in self.plants.iterrows()
            ])
            outflow = pulp.lpSum([
                dc_to_market.get((dc_id, m['market_id']), 0)
                for _, m in self.markets.iterrows()
            ])
            prob += inflow == outflow, f"DC_balance_{dc_id}"
        
        # 4. Demand fulfillment at markets
        for _, market in self.markets.iterrows():
            market_id = market['market_id']
            demand = market['annual_demand_millions'] * 1e6
            
            supply = pulp.lpSum([
                dc_to_market.get((dc['dc_id'], market_id), 0)
                for _, dc in self.dcs.iterrows()
            ])
            
            prob += supply + unmet_demand[market_id] == demand, f"Demand_{market_id}"
        
        # 5. Minimum fill rate constraint (if specified)
        if 'min_fill_rate' in constraints:
            total_demand = sum(self.markets['annual_demand_millions']) * 1e6
            total_unmet = pulp.lpSum([unmet_demand[m['market_id']] for _, m in self.markets.iterrows()])
            prob += total_unmet <= total_demand * (1 - constraints['min_fill_rate']), \
                    f"Min_fill_rate_{constraints['min_fill_rate']}"
        
        # SOLVE
        solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=30)  # 30 second time limit
        prob.solve(solver)
        
        # Extract solution
        if prob.status != pulp.LpStatusOptimal:
            raise RuntimeError(f"Optimization failed with status: {pulp.LpStatus[prob.status]}")
        
        # Build solution dictionary
        solution = {
            'scenario': scenario_name,
            'status': pulp.LpStatus[prob.status],
            'objective_value': pulp.value(prob.objective),
            'production': {p: pulp.value(production[p]) for p in production},
            'plant_to_dc_flows': {k: pulp.value(v) for k, v in plant_to_dc.items() if pulp.value(v) > 0.1},
            'dc_to_market_flows': {k: pulp.value(v) for k, v in dc_to_market.items() if pulp.value(v) > 0.1},
            'unmet_demand': {m: pulp.value(unmet_demand[m]) for m in unmet_demand if pulp.value(unmet_demand[m]) > 0.1},
            'cost_breakdown': {
                'production': pulp.value(production_cost),
                'transport_plant_dc': pulp.value(transport_cost_plant_dc),
                'transport_dc_market': pulp.value(transport_cost_dc_market),
                'warehousing': pulp.value(warehousing_cost),
                'unmet_penalty': pulp.value(unmet_penalty)
            }
        }
        
        return solution


def test_optimization():
    """Test the optimization model with all scenarios."""
    print("Testing Red Bull Network Optimization Model...\n")
    
    optimizer = NetworkOptimizer(data_dir='data')
    
    # Test baseline
    print("1. Running BASELINE scenario...")
    baseline = optimizer.optimize_baseline()
    print(f"   ✓ Status: {baseline['status']}")
    print(f"   ✓ Total Cost: €{baseline['objective_value']/1e6:.1f}M")
    print(f"   ✓ Production volume: {sum(baseline['production'].values())/1e6:.0f}M units")
    
    # Test cost optimization
    print("\n2. Running COST OPTIMIZED scenario...")
    cost_opt = optimizer.optimize_cost_minimization()
    print(f"   ✓ Status: {cost_opt['status']}")
    print(f"   ✓ Total Cost: €{cost_opt['objective_value']/1e6:.1f}M")
    savings = (baseline['objective_value'] - cost_opt['objective_value']) / baseline['objective_value'] * 100
    print(f"   ✓ Savings vs baseline: {savings:.1f}%")
    
    # Test disruption
    print("\n3. Running DISRUPTION scenario (Austria plant offline)...")
    disruption = optimizer.optimize_disruption_response()
    print(f"   ✓ Status: {disruption['status']}")
    print(f"   ✓ Total Cost: €{disruption['objective_value']/1e6:.1f}M")
    cost_increase = (disruption['objective_value'] - baseline['objective_value']) / baseline['objective_value'] * 100
    print(f"   ✓ Cost increase vs baseline: {cost_increase:.1f}%")
    print(f"   ✓ Austria production: {disruption['production'].get('P1', 0)/1e6:.0f}M units (should be 0)")
    
    print("\n✅ All scenarios completed successfully!")
    return baseline, cost_opt, disruption


if __name__ == '__main__':
    test_optimization()
