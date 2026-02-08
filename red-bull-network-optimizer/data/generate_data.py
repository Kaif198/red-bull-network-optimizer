"""
Red Bull Network Data Generation Script
Generates realistic supply chain network data based on actual Red Bull locations
and industry-standard logistics parameters.
"""

import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on earth (in kilometers).
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def generate_plants():
    """Generate 4 manufacturing plants with realistic Red Bull locations."""
    plants = pd.DataFrame([
        {
            'plant_id': 'P1',
            'name': 'Red Bull Headquarters Plant',
            'city': 'Fuschl am See',
            'country': 'Austria',
            'latitude': 47.8011,
            'longitude': 13.2697,
            'capacity_annual_millions': 500,
            'cost_per_unit_eur': 0.18,
            'notes': 'Largest facility - European distribution hub'
        },
        {
            'plant_id': 'P2',
            'name': 'Red Bull North America Plant',
            'city': 'Concord',
            'country': 'USA',
            'latitude': 35.4087,
            'longitude': -80.5795,
            'capacity_annual_millions': 300,
            'cost_per_unit_eur': 0.22,
            'notes': 'Serves Americas region'
        },
        {
            'plant_id': 'P3',
            'name': 'Red Bull South America Plant',
            'city': 'Jundiaí',
            'country': 'Brazil',
            'latitude': -23.1864,
            'longitude': -46.8842,
            'capacity_annual_millions': 200,
            'cost_per_unit_eur': 0.20,
            'notes': 'Growing LATAM market'
        },
        {
            'plant_id': 'P4',
            'name': 'Red Bull Asia-Pacific Plant',
            'city': 'Rayong',
            'country': 'Thailand',
            'latitude': 12.6814,
            'longitude': 101.2815,
            'capacity_annual_millions': 250,
            'cost_per_unit_eur': 0.19,
            'notes': 'Serves Asian markets'
        }
    ])
    
    return plants

def generate_distribution_centers():
    """Generate 12 strategic global distribution centers."""
    dcs = pd.DataFrame([
        {'dc_id': 'DC1', 'name': 'European Hub', 'city': 'Vienna', 'country': 'Austria', 'latitude': 48.2082, 'longitude': 16.3738, 'storage_capacity_millions': 50, 'fixed_cost_monthly_eur': 180000, 'variable_cost_per_unit_eur': 0.03, 'region': 'Europe'},
        {'dc_id': 'DC2', 'name': 'UK & Ireland Hub', 'city': 'London', 'country': 'UK', 'latitude': 51.5074, 'longitude': -0.1278, 'storage_capacity_millions': 35, 'fixed_cost_monthly_eur': 220000, 'variable_cost_per_unit_eur': 0.04, 'region': 'Europe'},
        {'dc_id': 'DC3', 'name': 'Western Europe Hub', 'city': 'Paris', 'country': 'France', 'latitude': 48.8566, 'longitude': 2.3522, 'storage_capacity_millions': 40, 'fixed_cost_monthly_eur': 200000, 'variable_cost_per_unit_eur': 0.035, 'region': 'Europe'},
        {'dc_id': 'DC4', 'name': 'North America West', 'city': 'Los Angeles', 'country': 'USA', 'latitude': 34.0522, 'longitude': -118.2437, 'storage_capacity_millions': 45, 'fixed_cost_monthly_eur': 250000, 'variable_cost_per_unit_eur': 0.045, 'region': 'Americas'},
        {'dc_id': 'DC5', 'name': 'North America East', 'city': 'Miami', 'country': 'USA', 'latitude': 25.7617, 'longitude': -80.1918, 'storage_capacity_millions': 40, 'fixed_cost_monthly_eur': 240000, 'variable_cost_per_unit_eur': 0.04, 'region': 'Americas'},
        {'dc_id': 'DC6', 'name': 'Latin America Hub', 'city': 'Mexico City', 'country': 'Mexico', 'latitude': 19.4326, 'longitude': -99.1332, 'storage_capacity_millions': 30, 'fixed_cost_monthly_eur': 150000, 'variable_cost_per_unit_eur': 0.03, 'region': 'Americas'},
        {'dc_id': 'DC7', 'name': 'Asia-Pacific Hub', 'city': 'Singapore', 'country': 'Singapore', 'latitude': 1.3521, 'longitude': 103.8198, 'storage_capacity_millions': 35, 'fixed_cost_monthly_eur': 210000, 'variable_cost_per_unit_eur': 0.042, 'region': 'Asia-Pacific'},
        {'dc_id': 'DC8', 'name': 'East Asia Hub', 'city': 'Tokyo', 'country': 'Japan', 'latitude': 35.6762, 'longitude': 139.6503, 'storage_capacity_millions': 30, 'fixed_cost_monthly_eur': 280000, 'variable_cost_per_unit_eur': 0.05, 'region': 'Asia-Pacific'},
        {'dc_id': 'DC9', 'name': 'Oceania Hub', 'city': 'Sydney', 'country': 'Australia', 'latitude': -33.8688, 'longitude': 151.2093, 'storage_capacity_millions': 20, 'fixed_cost_monthly_eur': 190000, 'variable_cost_per_unit_eur': 0.045, 'region': 'Asia-Pacific'},
        {'dc_id': 'DC10', 'name': 'MENA Hub', 'city': 'Dubai', 'country': 'UAE', 'latitude': 25.2048, 'longitude': 55.2708, 'storage_capacity_millions': 25, 'fixed_cost_monthly_eur': 170000, 'variable_cost_per_unit_eur': 0.035, 'region': 'MENA'},
        {'dc_id': 'DC11', 'name': 'Africa Hub', 'city': 'Johannesburg', 'country': 'South Africa', 'latitude': -26.2041, 'longitude': 28.0473, 'storage_capacity_millions': 15, 'fixed_cost_monthly_eur': 130000, 'variable_cost_per_unit_eur': 0.03, 'region': 'Africa'},
        {'dc_id': 'DC12', 'name': 'Eastern Europe Hub', 'city': 'Moscow', 'country': 'Russia', 'latitude': 55.7558, 'longitude': 37.6173, 'storage_capacity_millions': 25, 'fixed_cost_monthly_eur': 160000, 'variable_cost_per_unit_eur': 0.032, 'region': 'Europe'}
    ])
    
    return dcs

def generate_markets():
    """Generate 25 aggregated demand regions with realistic volumes."""
    markets = pd.DataFrame([
        {'market_id': 'M1', 'name': 'United States', 'country': 'USA', 'latitude': 37.0902, 'longitude': -95.7129, 'annual_demand_millions': 350, 'revenue_per_unit_eur': 2.80, 'seasonality_summer_multiplier': 1.3, 'market_maturity': 'Mature'},
        {'market_id': 'M2', 'name': 'Germany', 'country': 'Germany', 'latitude': 51.1657, 'longitude': 10.4515, 'annual_demand_millions': 85, 'revenue_per_unit_eur': 2.65, 'seasonality_summer_multiplier': 1.2, 'market_maturity': 'Mature'},
        {'market_id': 'M3', 'name': 'United Kingdom', 'country': 'UK', 'latitude': 55.3781, 'longitude': -3.4360, 'annual_demand_millions': 65, 'revenue_per_unit_eur': 2.70, 'seasonality_summer_multiplier': 1.15, 'market_maturity': 'Mature'},
        {'market_id': 'M4', 'name': 'Brazil', 'country': 'Brazil', 'latitude': -14.2350, 'longitude': -51.9253, 'annual_demand_millions': 55, 'revenue_per_unit_eur': 2.40, 'seasonality_summer_multiplier': 1.1, 'market_maturity': 'Growth'},
        {'market_id': 'M5', 'name': 'France', 'country': 'France', 'latitude': 46.2276, 'longitude': 2.2137, 'annual_demand_millions': 48, 'revenue_per_unit_eur': 2.68, 'seasonality_summer_multiplier': 1.25, 'market_maturity': 'Mature'},
        {'market_id': 'M6', 'name': 'Austria', 'country': 'Austria', 'latitude': 47.5162, 'longitude': 14.5501, 'annual_demand_millions': 42, 'revenue_per_unit_eur': 2.60, 'seasonality_summer_multiplier': 1.2, 'market_maturity': 'Mature'},
        {'market_id': 'M7', 'name': 'Netherlands', 'country': 'Netherlands', 'latitude': 52.1326, 'longitude': 5.2913, 'annual_demand_millions': 38, 'revenue_per_unit_eur': 2.72, 'seasonality_summer_multiplier': 1.18, 'market_maturity': 'Mature'},
        {'market_id': 'M8', 'name': 'Japan', 'country': 'Japan', 'latitude': 36.2048, 'longitude': 138.2529, 'annual_demand_millions': 45, 'revenue_per_unit_eur': 3.00, 'seasonality_summer_multiplier': 1.1, 'market_maturity': 'Mature'},
        {'market_id': 'M9', 'name': 'China', 'country': 'China', 'latitude': 35.8617, 'longitude': 104.1954, 'annual_demand_millions': 40, 'revenue_per_unit_eur': 2.50, 'seasonality_summer_multiplier': 1.05, 'market_maturity': 'High-Growth'},
        {'market_id': 'M10', 'name': 'Australia', 'country': 'Australia', 'latitude': -25.2744, 'longitude': 133.7751, 'annual_demand_millions': 32, 'revenue_per_unit_eur': 2.85, 'seasonality_summer_multiplier': 1.4, 'market_maturity': 'Mature'},
        {'market_id': 'M11', 'name': 'Mexico', 'country': 'Mexico', 'latitude': 23.6345, 'longitude': -102.5528, 'annual_demand_millions': 35, 'revenue_per_unit_eur': 2.30, 'seasonality_summer_multiplier': 1.15, 'market_maturity': 'Growth'},
        {'market_id': 'M12', 'name': 'India', 'country': 'India', 'latitude': 20.5937, 'longitude': 78.9629, 'annual_demand_millions': 28, 'revenue_per_unit_eur': 2.20, 'seasonality_summer_multiplier': 1.3, 'market_maturity': 'High-Growth'},
        {'market_id': 'M13', 'name': 'Canada', 'country': 'Canada', 'latitude': 56.1304, 'longitude': -106.3468, 'annual_demand_millions': 30, 'revenue_per_unit_eur': 2.75, 'seasonality_summer_multiplier': 1.25, 'market_maturity': 'Mature'},
        {'market_id': 'M14', 'name': 'Spain', 'country': 'Spain', 'latitude': 40.4637, 'longitude': -3.7492, 'annual_demand_millions': 28, 'revenue_per_unit_eur': 2.62, 'seasonality_summer_multiplier': 1.35, 'market_maturity': 'Mature'},
        {'market_id': 'M15', 'name': 'Italy', 'country': 'Italy', 'latitude': 41.8719, 'longitude': 12.5674, 'annual_demand_millions': 26, 'revenue_per_unit_eur': 2.66, 'seasonality_summer_multiplier': 1.3, 'market_maturity': 'Mature'},
        {'market_id': 'M16', 'name': 'Poland', 'country': 'Poland', 'latitude': 51.9194, 'longitude': 19.1451, 'annual_demand_millions': 22, 'revenue_per_unit_eur': 2.35, 'seasonality_summer_multiplier': 1.15, 'market_maturity': 'Growth'},
        {'market_id': 'M17', 'name': 'South Korea', 'country': 'South Korea', 'latitude': 35.9078, 'longitude': 127.7669, 'annual_demand_millions': 24, 'revenue_per_unit_eur': 2.90, 'seasonality_summer_multiplier': 1.1, 'market_maturity': 'Mature'},
        {'market_id': 'M18', 'name': 'UAE', 'country': 'UAE', 'latitude': 23.4241, 'longitude': 53.8478, 'annual_demand_millions': 20, 'revenue_per_unit_eur': 2.95, 'seasonality_summer_multiplier': 1.05, 'market_maturity': 'Growth'},
        {'market_id': 'M19', 'name': 'South Africa', 'country': 'South Africa', 'latitude': -30.5595, 'longitude': 22.9375, 'annual_demand_millions': 18, 'revenue_per_unit_eur': 2.25, 'seasonality_summer_multiplier': 1.2, 'market_maturity': 'Growth'},
        {'market_id': 'M20', 'name': 'Turkey', 'country': 'Turkey', 'latitude': 38.9637, 'longitude': 35.2433, 'annual_demand_millions': 19, 'revenue_per_unit_eur': 2.40, 'seasonality_summer_multiplier': 1.25, 'market_maturity': 'Growth'},
        {'market_id': 'M21', 'name': 'Russia', 'country': 'Russia', 'latitude': 61.5240, 'longitude': 105.3188, 'annual_demand_millions': 25, 'revenue_per_unit_eur': 2.45, 'seasonality_summer_multiplier': 1.15, 'market_maturity': 'Growth'},
        {'market_id': 'M22', 'name': 'Thailand', 'country': 'Thailand', 'latitude': 15.8700, 'longitude': 100.9925, 'annual_demand_millions': 21, 'revenue_per_unit_eur': 2.35, 'seasonality_summer_multiplier': 1.1, 'market_maturity': 'Growth'},
        {'market_id': 'M23', 'name': 'Indonesia', 'country': 'Indonesia', 'latitude': -0.7893, 'longitude': 113.9213, 'annual_demand_millions': 17, 'revenue_per_unit_eur': 2.28, 'seasonality_summer_multiplier': 1.08, 'market_maturity': 'High-Growth'},
        {'market_id': 'M24', 'name': 'Argentina', 'country': 'Argentina', 'latitude': -38.4161, 'longitude': -63.6167, 'annual_demand_millions': 15, 'revenue_per_unit_eur': 2.35, 'seasonality_summer_multiplier': 1.12, 'market_maturity': 'Growth'},
        {'market_id': 'M25', 'name': 'Sweden', 'country': 'Sweden', 'latitude': 60.1282, 'longitude': 18.6435, 'annual_demand_millions': 16, 'revenue_per_unit_eur': 2.78, 'seasonality_summer_multiplier': 1.2, 'market_maturity': 'Mature'}
    ])
    
    return markets

def generate_transportation_routes(plants, dcs, markets):
    """Generate realistic transportation routes with costs based on distance and mode."""
    routes = []
    
    # Plant to DC routes
    for _, plant in plants.iterrows():
        for _, dc in dcs.iterrows():
            distance = haversine_distance(plant['latitude'], plant['longitude'], 
                                         dc['latitude'], dc['longitude'])
            
            # Determine transport mode based on distance
            if distance < 500:
                mode = 'road'
                cost_per_unit = 0.02
                lead_time = max(1, int(distance / 400))  # ~400km/day
                co2_per_unit = 0.05
            elif distance < 2000:
                mode = 'road'
                cost_per_unit = 0.025
                lead_time = max(2, int(distance / 500))
                co2_per_unit = 0.06
            else:
                mode = 'sea'
                cost_per_unit = 0.03 + (distance / 100000) * 0.01  # Scale with distance
                lead_time = max(7, int(distance / 800))  # Sea freight
                co2_per_unit = 0.08
            
            # Add realistic variance
            cost_variance = np.random.uniform(0.95, 1.05)
            cost_per_unit *= cost_variance
            
            routes.append({
                'from_id': plant['plant_id'],
                'to_id': dc['dc_id'],
                'from_type': 'plant',
                'to_type': 'dc',
                'distance_km': round(distance, 1),
                'transport_mode': mode,
                'cost_per_unit_eur': round(cost_per_unit, 3),
                'lead_time_days': lead_time,
                'co2_per_unit_kg': round(co2_per_unit, 3),
                'capacity_constraint': 'unlimited'
            })
    
    # DC to Market routes (assign each market to nearest 2-3 DCs for redundancy)
    for _, market in markets.iterrows():
        # Calculate distances to all DCs
        dc_distances = []
        for _, dc in dcs.iterrows():
            distance = haversine_distance(market['latitude'], market['longitude'],
                                         dc['latitude'], dc['longitude'])
            dc_distances.append((dc['dc_id'], distance))
        
        # Sort by distance and take nearest 2-3
        dc_distances.sort(key=lambda x: x[1])
        nearest_dcs = dc_distances[:3]
        
        for dc_id, distance in nearest_dcs:
            if distance < 300:
                mode = 'road'
                cost_per_unit = 0.01
                lead_time = max(0.5, int(distance / 500))
                co2_per_unit = 0.02
            elif distance < 1000:
                mode = 'road'
                cost_per_unit = 0.015
                lead_time = max(1, int(distance / 400))
                co2_per_unit = 0.03
            else:
                mode = 'road'
                cost_per_unit = 0.025
                lead_time = max(2, int(distance / 350))
                co2_per_unit = 0.05
            
            # Add variance
            cost_variance = np.random.uniform(0.95, 1.05)
            cost_per_unit *= cost_variance
            
            routes.append({
                'from_id': dc_id,
                'to_id': market['market_id'],
                'from_type': 'dc',
                'to_type': 'market',
                'distance_km': round(distance, 1),
                'transport_mode': mode,
                'cost_per_unit_eur': round(cost_per_unit, 3),
                'lead_time_days': lead_time,
                'co2_per_unit_kg': round(co2_per_unit, 3),
                'capacity_constraint': 'unlimited'
            })
    
    return pd.DataFrame(routes)

def main():
    """Generate all network data files."""
    print("Generating Red Bull Network Data...")
    
    # Generate data
    plants = generate_plants()
    dcs = generate_distribution_centers()
    markets = generate_markets()
    routes = generate_transportation_routes(plants, dcs, markets)
    
    # Save to CSV
    plants.to_csv('data/plants.csv', index=False)
    dcs.to_csv('data/distribution_centers.csv', index=False)
    markets.to_csv('data/markets.csv', index=False)
    routes.to_csv('data/transportation.csv', index=False)
    
    # Print summary
    print(f"\n✅ Data generation complete!")
    print(f"  - Plants: {len(plants)} facilities")
    print(f"  - Distribution Centers: {len(dcs)} locations")
    print(f"  - Markets: {len(markets)} regions")
    print(f"  - Transportation Routes: {len(routes)} connections")
    print(f"\nTotal annual demand: {markets['annual_demand_millions'].sum():.0f}M units")
    print(f"Total production capacity: {plants['capacity_annual_millions'].sum():.0f}M units")
    print(f"Capacity utilization: {(markets['annual_demand_millions'].sum() / plants['capacity_annual_millions'].sum() * 100):.1f}%")
    
    print("\nSample data preview:")
    print("\nPlants (first 2 rows):")
    print(plants.head(2)[['plant_id', 'name', 'city', 'capacity_annual_millions', 'cost_per_unit_eur']])
    print("\nDistribution Centers (first 3 rows):")
    print(dcs.head(3)[['dc_id', 'name', 'city', 'region', 'storage_capacity_millions']])
    print("\nMarkets (first 5 rows):")
    print(markets.head(5)[['market_id', 'name', 'annual_demand_millions', 'revenue_per_unit_eur']])
    print("\nTransportation Routes (first 5 rows):")
    print(routes.head(5)[['from_id', 'to_id', 'distance_km', 'transport_mode', 'cost_per_unit_eur']])

if __name__ == '__main__':
    main()
