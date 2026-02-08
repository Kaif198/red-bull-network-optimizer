/**
 * Leaflet Map Visualization for Red Bull Network
 * Interactive network map with plants, DCs, markets, and flows
 */

let networkMap = null;
let mapLayers = {
    plants: null,
    dcs: null,
    markets: null,
    flows: null
};
let networkData = null;

// Initialize map when network section becomes visible
document.addEventListener('DOMContentLoaded', function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.target.id === 'network' && mutation.target.classList.contains('active')) {
                if (!networkMap) {
                    setTimeout(initializeNetworkMap, 100); // Small delay for container to be visible
                }
            }
        });
    });
    
    const networkSection = document.getElementById('network');
    if (networkSection) {
        observer.observe(networkSection, { attributes: true, attributeFilter: ['class'] });
    }
});

/**
 * Initialize Leaflet network map
 */
async function initializeNetworkMap() {
    const mapContainer = document.getElementById('network-map');
    if (!mapContainer || networkMap) return;
    
    try {
        // Create map centered on Europe (Red Bull HQ region)
        networkMap = L.map('network-map', {
            center: [30.0, 15.0],
            zoom: 2,
            minZoom: 2,
            maxZoom: 10
        });
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(networkMap);
        
        // Load network data
        const response = await fetch(`${API_BASE}/api/network-data`);
        const data = await response.json();
        
        if (data.success) {
            networkData = data;
            createMapLayers(data);
            setupLayerControls();
        }
        
        // Force map to recalculate size
        setTimeout(() => {
            if (networkMap) networkMap.invalidateSize();
        }, 200);
        
    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

/**
 * Create map layers for plants, DCs, markets, and flows
 */
function createMapLayers(data) {
    // Create layer groups
    mapLayers.plants = L.layerGroup().addTo(networkMap);
    mapLayers.dcs = L.layerGroup().addTo(networkMap);
    mapLayers.markets = L.layerGroup().addTo(networkMap);
    mapLayers.flows = L.layerGroup().addTo(networkMap);
    
    // Add plants (large red circles)
    data.plants.forEach(plant => {
        const marker = L.circleMarker([plant.latitude, plant.longitude], {
            radius: 12,
            fillColor: '#DB0A40',
            color: '#FFF',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(mapLayers.plants);
        
        marker.bindPopup(`
            <div style="min-width:220px; font-family: sans-serif;">
                <h4 style="color:#DB0A40; margin:0 0 10px 0; font-size:16px; border-bottom:2px solid #FFCC00; padding-bottom:5px;">
                    ${plant.name}
                </h4>
                <p style="margin:5px 0;"><strong>📍 Location:</strong> ${plant.city}, ${plant.country}</p>
                <p style="margin:5px 0;"><strong>⚡ Capacity:</strong> ${plant.capacity_annual_millions}M units/year</p>
                <p style="margin:5px 0;"><strong>💰 Cost:</strong> €${plant.cost_per_unit_eur}/unit</p>
                <p style="margin:10px 0 5px 0; font-size:13px; font-style:italic; color:#666;">
                    ${plant.notes}
                </p>
            </div>
        `);
    });
    
    // Add DCs (medium yellow circles)
    data.dcs.forEach(dc => {
        const marker = L.circleMarker([dc.latitude, dc.longitude], {
            radius: 9,
            fillColor: '#FFCC00',
            color: '#FFF',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(mapLayers.dcs);
        
        marker.bindPopup(`
            <div style="min-width:200px; font-family: sans-serif;">
                <h4 style="color:#FFCC00; margin:0 0 10px 0; font-size:15px; border-bottom:2px solid #DB0A40; padding-bottom:5px;">
                    ${dc.name}
                </h4>
                <p style="margin:5px 0;"><strong>📍 Location:</strong> ${dc.city}, ${dc.country}</p>
                <p style="margin:5px 0;"><strong>🌍 Region:</strong> ${dc.region}</p>
                <p style="margin:5px 0;"><strong>📦 Capacity:</strong> ${dc.storage_capacity_millions}M units</p>
                <p style="margin:5px 0;"><strong>💵 Fixed Cost:</strong> €${(dc.fixed_cost_monthly_eur / 1000).toFixed(0)}K/month</p>
            </div>
        `);
    });
    
    // Add markets (small blue circles)
    data.markets.forEach(market => {
        const marker = L.circleMarker([market.latitude, market.longitude], {
            radius: 6,
            fillColor: '#005EB8',
            color: '#FFF',
            weight: 1.5,
            opacity: 1,
            fillOpacity: 0.7
        }).addTo(mapLayers.markets);
        
        marker.bindPopup(`
            <div style="min-width:180px; font-family: sans-serif;">
                <h4 style="color:#005EB8; margin:0 0 10px 0; font-size:14px; border-bottom:2px solid #FFCC00; padding-bottom:5px;">
                    ${market.name}
                </h4>
                <p style="margin:5px 0;"><strong>📊 Demand:</strong> ${market.annual_demand_millions}M units/year</p>
                <p style="margin:5px 0;"><strong>💵 Revenue:</strong> €${market.revenue_per_unit_eur}/unit</p>
                <p style="margin:5px 0;"><strong>📈 Market:</strong> ${market.market_maturity}</p>
            </div>
        `);
    });
    
    // Add flows if available
    if (data.flows && (data.flows.plant_to_dc || data.flows.dc_to_market)) {
        addFlowLines(data);
    }
}

/**
 * Add flow lines to map
 */
function addFlowLines(data) {
    // Helper function to find coordinates
    const findCoords = (id, type) => {
        let item;
        if (type === 'plant') {
            item = data.plants.find(p => p.plant_id === id);
        } else if (type === 'dc') {
            item = data.dcs.find(d => d.dc_id === id);
        } else if (type === 'market') {
            item = data.markets.find(m => m.market_id === id);
        }
        return item ? [item.latitude, item.longitude] : null;
    };
    
    // Plant to DC flows (thicker lines, red-yellow gradient)
    if (data.flows.plant_to_dc) {
        data.flows.plant_to_dc.forEach(flow => {
            const from = findCoords(flow.from, 'plant');
            const to = findCoords(flow.to, 'dc');
            
            if (from && to) {
                // Volume-based line thickness
                const volume = flow.volume / 1e6; // Convert to millions
                const weight = Math.max(2, Math.min(8, volume / 50));
                
                const line = L.polyline([from, to], {
                    color: '#DB0A40',
                    weight: weight,
                    opacity: 0.6,
                    dashArray: '5, 5'
                }).addTo(mapLayers.flows);
                
                line.bindTooltip(`${flow.from} → ${flow.to}: ${volume.toFixed(0)}M units`, {
                    permanent: false,
                    direction: 'center'
                });
            }
        });
    }
    
    // DC to Market flows (thinner lines, yellow-blue gradient)
    if (data.flows.dc_to_market) {
        data.flows.dc_to_market.forEach(flow => {
            const from = findCoords(flow.from, 'dc');
            const to = findCoords(flow.to, 'market');
            
            if (from && to) {
                const volume = flow.volume / 1e6;
                const weight = Math.max(1, Math.min(4, volume / 30));
                
                const line = L.polyline([from, to], {
                    color: '#FFCC00',
                    weight: weight,
                    opacity: 0.4,
                    dashArray: '3, 3'
                }).addTo(mapLayers.flows);
                
                line.bindTooltip(`${flow.from} → ${flow.to}: ${volume.toFixed(0)}M units`, {
                    permanent: false,
                    direction: 'center'
                });
            }
        });
    }
}

/**
 * Setup layer control checkboxes
 */
function setupLayerControls() {
    document.getElementById('show-plants')?.addEventListener('change', function(e) {
        if (e.target.checked && mapLayers.plants) {
            networkMap.addLayer(mapLayers.plants);
        } else if (mapLayers.plants) {
            networkMap.removeLayer(mapLayers.plants);
        }
    });
    
    document.getElementById('show-dcs')?.addEventListener('change', function(e) {
        if (e.target.checked && mapLayers.dcs) {
            networkMap.addLayer(mapLayers.dcs);
        } else if (mapLayers.dcs) {
            networkMap.removeLayer(mapLayers.dcs);
        }
    });
    
    document.getElementById('show-markets')?.addEventListener('change', function(e) {
        if (e.target.checked && mapLayers.markets) {
            networkMap.addLayer(mapLayers.markets);
        } else if (mapLayers.markets) {
            networkMap.removeLayer(mapLayers.markets);
        }
    });
    
    document.getElementById('show-flows')?.addEventListener('change', function(e) {
        if (e.target.checked && mapLayers.flows) {
            networkMap.addLayer(mapLayers.flows);
        } else if (mapLayers.flows) {
            networkMap.removeLayer(mapLayers.flows);
        }
    });
}

/**
 * Update map with new scenario flows
 */
function updateMapFlows(scenarioData) {
    if (!networkMap || !networkData) return;
    
    // Clear existing flows
    if (mapLayers.flows) {
        mapLayers.flows.clearLayers();
    }
    
    // Add new flows from scenario
    if (scenarioData.flows) {
        addFlowLines({
            ...networkData,
            flows: scenarioData.flows
        });
    }
}

