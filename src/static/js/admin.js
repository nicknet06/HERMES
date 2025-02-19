let map;
let serviceMarkers = {
    hospital: [],
    police: [],
    fire: []
};

// Icon configurations
const icons = {
    hospital: L.icon({
        iconUrl: '/images/hospital-icon.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    police: L.icon({
        iconUrl: '/images/police-icon.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    fire: L.icon({
        iconUrl: '/images/fire-icon.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    })
};

const incidentIcons = {
    CRITICAL: L.divIcon({
        html: `<div class="incident-marker critical">
                <svg viewBox="0 0 24 24" width="24" height="24">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                </svg>
               </div>`,
        className: 'incident-marker-container',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
    }),
    MODERATE: L.divIcon({
        html: `<div class="incident-marker moderate">
                <svg viewBox="0 0 24 24" width="24" height="24">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                </svg>
               </div>`,
        className: 'incident-marker-container',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
    }),
    LOW: L.divIcon({
        html: `<div class="incident-marker low">
                <svg viewBox="0 0 24 24" width="24" height="24">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                </svg>
               </div>`,
        className: 'incident-marker-container',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
    })
};
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    loadServices();
    setupEventListeners();
    loadRecentIncidents(map);
});
function isWithinLast3Hours(dateString) {
    const now = new Date();
    const incidentDate = new Date(dateString);
    const threeHoursAgo = new Date(now - (3 * 60 * 60 * 1000)); // 3 hours in milliseconds
    return incidentDate >= threeHoursAgo;
}
function initMap() {
    const greeceCenter = [38.2749497, 23.8102717];
    map = L.map('map').setView(greeceCenter, 7);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}
function formatDateTime(isoString) {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat('el-GR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'Asia/Muscat'
    }).format(date);
}
// Add this function to fetch and display incidents
async function loadRecentIncidents(map) {
    try {
        const response = await fetch('/api/incidents/recent');
        if (!response.ok) {
            throw new Error('Failed to fetch recent incidents');
        }

        const data = await response.json();


        data.incidents.forEach(incident => {
            if (incident.coordinates && incident.coordinates.lat && incident.coordinates.lng) {
                // Determine severity category
                const severityCategory = incident.severity_level >= 4 ? 'CRITICAL'
                                     : incident.severity_level >= 2 ? 'MODERATE'
                                     : 'LOW';

                // Create marker with appropriate icon
                const marker = L.marker([incident.coordinates.lat, incident.coordinates.lng], {
                    icon: incidentIcons[severityCategory]
                }).addTo(map);

                // Format timestamp
                const incidentTime = new Date(incident.created_at);
                const timeString = formatDateTime(incident.created_at);

                // Create popup content
                const popupContent = `
                    <div class="incident-popup ${severityCategory.toLowerCase()}">
                        <div class="incident-popup-header">
                            <span class="incident-time">${timeString}</span>
                            <span class="incident-severity ${severityCategory.toLowerCase()}">${severityCategory}</span>
                        </div>
                        <div class="incident-popup-body">
                            <p>${incident.description}</p>
                            ${incident.required_services ? 
                                `<p class="required-services">Services: ${incident.required_services.join(', ')}</p>` : ''}
                        </div>
                        <div class="incident-popup-footer">
                            <button onclick="showIncidentDetails(${incident.id})" class="details-btn">View Details</button>
                        </div>
                    </div>
                `;

                marker.bindPopup(popupContent);
            }
        });

    } catch (error) {
        console.error('Error loading incidents:', error);
    }
}
function loadServices() {
    showLoading();
    fetch('/api/services')
        .then(response => response.json())
        .then(services => {
            services.forEach(service => {
                addServiceMarker(service);
            });
            hideLoading();
        })
        .catch(error => {
            console.error('Error loading services:', error);
            showError('Failed to load emergency services');
            hideLoading();
        });
}

function addServiceMarker(service) {
    const marker = L.marker(
        [service.latitude, service.longitude],
        { icon: icons[service.service_type] }
    );

    const popupContent = `
        <div class="service-info">
            <h3>${service.name}</h3>
            <p>Type: ${service.service_type}</p>
            <p>Address: ${service.address}</p>
            <p>Phone: ${service.phone}</p>
            <button onclick="showServiceResources(${service.id}, '${service.name}', '${service.service_type}')" class="view-resources-btn">View Resources</button>
        </div>
    `;

    marker.bindPopup(popupContent);
    marker.on('click', () => {
        showServiceResources(service.id, service.name, service.service_type);
    });
    marker.addTo(map);
    serviceMarkers[service.service_type].push(marker);
}

// Modify the existing showServiceResources function to include incidents
async function showServiceResources(serviceId, serviceName, serviceType) {
    currentServiceId = serviceId; // Store the current service ID
    const resourcesPanel = document.getElementById('resources-panel');
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.innerHTML = '<span class="spinner"></span> Loading resources...';

    // Clear previous content and show loading
    resourcesPanel.innerHTML = '';
    resourcesPanel.appendChild(loadingIndicator);
    resourcesPanel.style.display = 'block';

    try {
        // Fetch both resources and incidents in parallel
        const [resourcesResponse, incidentsResponse] = await Promise.all([
            fetch(`/api/services/${serviceId}/resources`),
            fetch(`/api/services/${serviceId}/incidents?hours=3`) // Fetch last 3 hours incidents
        ]);

        if (!resourcesResponse.ok || !incidentsResponse.ok) {
            throw new Error('Failed to fetch data');
        }

        const [resourcesData, incidentsData] = await Promise.all([
            resourcesResponse.json(),
            incidentsResponse.json()
        ]);

        // Create the content with both resources and incidents
        const content = `
            <div class="panel-header">
                <div class="service-header ${serviceType}">
                    <h4>${serviceName}</h4>
                    <span class="service-type">${serviceType}</span>
                </div>
                <button class="close-resources-btn" onclick="closeResourcesPanel()">
                    <span class="close-icon">×</span>
                </button>
            </div>
            
            <div class="resource-group">
                <h4>Equipment</h4>
                <div class="resource-items">
                    ${renderEquipmentList(resourcesData.equipment)}
                </div>
            </div>

            <div class="resource-group">
                <h4>Vehicles</h4>
                <div class="resource-items">
                    ${renderVehicleList(resourcesData.vehicles)}
                </div>
            </div>

            <div class="resource-group">
                <h4>Personnel</h4>
                <div class="resource-items">
                    ${renderPersonnelList(resourcesData.personnel)}
                </div>
            </div>

            <div class="resource-group">
                <h4>Incidents (last 3 hours)</h4>
                <div class="resource-items">
                    ${renderIncidentsList(incidentsData.incidents)}
                </div>
            </div>
        `;

        resourcesPanel.innerHTML = content;

    } catch (error) {
        console.error('Error loading data:', error);
        resourcesPanel.innerHTML = `
            <div class="error-message">
                Failed to load data. Please try again later.
                <button onclick="showServiceResources(${serviceId}, '${serviceName}', '${serviceType}')" class="retry-btn">Retry</button>
                <button class="close-resources-btn" onclick="closeResourcesPanel()">
                    <span class="close-icon">×</span>
                </button>
            </div>
        `;
    }
}

// Add this function to render incidents
function renderIncidentsList(incidents = []) {
    if (!incidents || incidents.length === 0) {
        return '<p class="no-data">No incidents in the last 3 hours</p>';
    }

    return incidents.map(incident => {
        // Convert severity_level to severity category
        const severityCategory = incident.severity_level >= 4 ? 'CRITICAL'
                               : incident.severity_level >= 2 ? 'MODERATE'
                               : 'LOW';

        // Format the timestamp
        const incidentTime = new Date(incident.created_at);
        const timeString = formatDateTime(incident.created_at);

        // Format required services and specialties
        const services = incident.required_services ?
            `<div class="incident-services">Required Services: ${incident.required_services.join(', ')}</div>` : '';

        const specialties = incident.required_specialties ?
            `<div class="incident-specialties">Required Specialties: ${incident.required_specialties.join(', ')}</div>` : '';

        const equipment = incident.required_equipment ?
            `<div class="incident-equipment">Required Equipment: ${incident.required_equipment.join(', ')}</div>` : '';

        // Add situation assessment and user response sections
        const assessment = incident.situation_assessment ?
            `<div class="incident-assessment">
                <h5>Situation Assessment</h5>
                <p>${incident.situation_assessment}</p>
            </div>` : '';

        const response = incident.user_response ?
            `<div class="incident-response">
                <h5>Response Instructions</h5>
                <p>${incident.user_response}</p>
            </div>` : '';

        return `
            <div class="resource-item incident-item ${severityCategory.toLowerCase()}">
                <div class="resource-header">
                    <div class="incident-time">${timeString}</div>
                    <div class="incident-severity ${severityCategory.toLowerCase()}">
                        ${severityCategory}
                    </div>
                </div>
                <div class="incident-description">
                    ${incident.description || 'No description available'}
                </div>
                <div class="incident-details">
                    <span class="incident-status">
                        Status: ${incident.is_genuine_emergency ? 'Genuine Emergency' : 'Under Review'}
                    </span>
                    <span class="incident-id">ID: ${incident.id}</span>
                </div>
                ${incident.location ? `<div class="incident-location">Location: ${incident.location}</div>` : ''}
                ${services}
                ${specialties}
                ${equipment}
                ${assessment}
                ${response}
            </div>
        `;
    }).join('');
}

// Add this new function to handle closing the panel
function closeResourcesPanel() {
    const resourcesPanel = document.getElementById('resources-panel');
    resourcesPanel.style.display = 'none';
    resourcesPanel.innerHTML = ''; // Clear the content
}
function renderEquipmentList(equipment) {
    if (!equipment || equipment.length === 0) {
        return '<p class="no-data">No equipment available</p>';
    }

    return equipment.map(item => `
        <div class="resource-item ${item.available > 0 ? 'available' : 'unavailable'}">
            <div class="resource-header">
                <span>${item.name}</span>
                <span>${item.available}/${item.quantity}</span>
            </div>
            <div>Status: ${item.condition}</div>
        </div>
    `).join('');
}

function renderVehicleList(vehicles) {
    if (!vehicles || vehicles.length === 0) {
        return '<p class="no-data">No vehicles available</p>';
    }

    return vehicles.map(vehicle => `
        <div class="resource-item ${vehicle.status === 'available' ? 'available' : 'unavailable'}">
            <div class="resource-header">
                <span>${vehicle.type} - ${vehicle.model}</span>
                <span>${vehicle.status}</span>
            </div>
            <div>Plate: ${vehicle.plate_number}</div>
        </div>
    `).join('');
}

function renderPersonnelList(personnel) {
    if (!personnel || personnel.length === 0) {
        return '<p class="no-data">No personnel available</p>';
    }

    return personnel.map(person => `
        <div class="resource-item ${person.status === 'on-duty' ? 'available' : 'unavailable'}">
            <div class="resource-header">
                <span>${person.name}</span>
                <span>${person.status}</span>
            </div>
            <div>Role: ${person.role}</div>
            ${person.speciality ? `<div>Specialty: ${person.speciality}</div>` : ''}
        </div>
    `).join('');
}

function setupEventListeners() {
    // Service type checkboxes
    document.getElementById('show-hospitals').addEventListener('change', function(e) {
        toggleMarkers('hospital', e.target.checked);
    });

    document.getElementById('show-police').addEventListener('change', function(e) {
        toggleMarkers('police', e.target.checked);
    });

    document.getElementById('show-fire').addEventListener('change', function(e) {
        toggleMarkers('fire', e.target.checked);
    });
}

function toggleMarkers(type, show) {
    serviceMarkers[type].forEach(marker => {
        if (show) {
            marker.addTo(map);
        } else {
            marker.remove();
        }
    });
}

function showLoading() {
    const loadingEl = document.createElement('div');
    loadingEl.id = 'loading-overlay';
    loadingEl.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(loadingEl);
}

function hideLoading() {
    const loadingEl = document.getElementById('loading-overlay');
    if (loadingEl) {
        loadingEl.remove();
    }
}

function showError(message) {
    const errorEl = document.createElement('div');
    errorEl.className = 'error-toast';
    errorEl.textContent = message;
    document.body.appendChild(errorEl);
    setTimeout(() => errorEl.remove(), 5000);
}
async function showIncidentDetails(incidentId) {
    const modal = document.getElementById('incident-details-modal');
    const modalBody = modal.querySelector('.modal-body');
    const closeBtn = modal.querySelector('.close-modal');

    try {
        // Show loading state
        modalBody.innerHTML = '<div class="loading-indicator"><span class="spinner"></span> Loading incident details...</div>';
        modal.style.display = 'block';

        // Fetch incident details
        const response = await fetch(`/api/incidents/${incidentId}`);
        if (!response.ok) throw new Error('Failed to fetch incident details');

        const incident = await response.json();

        // Convert severity level to category
        const severityCategory = incident.severity_level >= 4 ? 'CRITICAL'
                             : incident.severity_level >= 2 ? 'MODERATE'
                             : 'LOW';

        // Format timestamp
        const incidentTime = new Date(incident.created_at);
        const timeString = formatDateTime(incident.created_at);

        // Create content
        const content = `
            <div class="incident-detail-container">
                <div class="incident-detail-header ${severityCategory.toLowerCase()}">
                    <div class="incident-basic-info">
                        <span class="incident-id-badge">ID: ${incident.id}</span>
                        <span class="incident-time-badge">${timeString}</span>
                    </div>
                    <div class="incident-severity-badge ${severityCategory.toLowerCase()}">
                        ${severityCategory}
                    </div>
                </div>

                <div class="incident-detail-section">
                    <h3>Location</h3>
                    <p>${incident.location}</p>
                    <div class="coordinates">
                        <span>Lat: ${incident.coordinates.lat}</span>
                        <span>Lng: ${incident.coordinates.lng}</span>
                    </div>
                </div>

                <div class="incident-detail-section">
                    <h3>Description</h3>
                    <p>${incident.description || 'No description provided'}</p>
                </div>

                <div class="incident-detail-section">
                    <h3>Situation Assessment</h3>
                    <p>${incident.situation_assessment || 'No assessment provided'}</p>
                </div>

                <div class="incident-detail-section">
                    <h3>Response Instructions</h3>
                    <p>${incident.user_response || 'No response instructions provided'}</p>
                </div>

                <div class="incident-resources">
                    <div class="resource-section">
                        <h3>Required Services</h3>
                        <div class="resource-tags">
                            ${incident.required_services ? 
                                incident.required_services.map(service => 
                                    `<span class="resource-tag service-tag">${service}</span>`
                                ).join('') : 
                                'No services specified'}
                        </div>
                    </div>

                    <div class="resource-section">
                        <h3>Required Specialties</h3>
                        <div class="resource-tags">
                            ${incident.required_specialties ? 
                                incident.required_specialties.map(specialty => 
                                    `<span class="resource-tag specialty-tag">${specialty}</span>`
                                ).join('') : 
                                'No specialties specified'}
                        </div>
                    </div>

                    <div class="resource-section">
                        <h3>Required Equipment</h3>
                        <div class="resource-tags">
                            ${incident.required_equipment ? 
                                incident.required_equipment.map(equipment => 
                                    `<span class="resource-tag equipment-tag">${equipment}</span>`
                                ).join('') : 
                                'No equipment specified'}
                        </div>
                    </div>
                </div>

                <div class="incident-status-section">
                    <h3>Status</h3>
                    <div class="status-badge ${incident.is_genuine_emergency ? 'genuine' : 'under-review'}">
                        ${incident.is_genuine_emergency ? 'Genuine Emergency' : 'Under Review'}
                    </div>
                </div>
            </div>
        `;

        modalBody.innerHTML = content;

        // Handle modal close
        closeBtn.onclick = function() {
            modal.style.display = "none";
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

    } catch (error) {
        console.error('Error loading incident details:', error);
        modalBody.innerHTML = `
            <div class="error-message">
                Failed to load incident details. Please try again later.<br>
                Error: ${error.message}
                <button onclick="showIncidentDetails(${incidentId})" class="retry-btn">Retry</button>
            </div>
        `;
    }
}

// Modify your existing map initialization code
