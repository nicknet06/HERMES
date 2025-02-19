// // Initialize map when the page loads
// document.addEventListener('DOMContentLoaded', function() {
//     // Initialize the map
//     const map = L.map('map').setView([38.2749497, 23.8102717], 7);
//
//     // Add OpenStreetMap tiles
//     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//         attribution: '© OpenStreetMap contributors'
//     }).addTo(map);
//
//     // Define custom icons for different service types
//     const icons = {
//         hospital: L.icon({
//             iconUrl: '/images/hospital-marker.png',
//             iconSize: [32, 32],
//             iconAnchor: [16, 32],
//             popupAnchor: [0, -32]
//         }),
//         police: L.icon({
//             iconUrl: '/images/police-marker.png',
//             iconSize: [32, 32],
//             iconAnchor: [16, 32],
//             popupAnchor: [0, -32]
//         }),
//         fire: L.icon({
//             iconUrl: '/images/fire-marker.png',
//             iconSize: [32, 32],
//             iconAnchor: [16, 32],
//             popupAnchor: [0, -32]
//         }),
//         default: L.icon({
//             iconUrl: '/images/default-marker.png',
//             iconSize: [32, 32],
//             iconAnchor: [16, 32],
//             popupAnchor: [0, -32]
//         })
//     };
//
//     // Function to get the appropriate icon based on service type
//     function getServiceIcon(type) {
//         if (!type) return icons.default;
//         const serviceType = type.toLowerCase();
//         return icons[serviceType] || icons.default;
//     }
//
//     // Add markers for all emergency services
//     const services = document.querySelectorAll('[data-service-type]');
//     services.forEach(service => {
//         const lat = parseFloat(service.getAttribute('data-lat'));
//         const lng = parseFloat(service.getAttribute('data-lng'));
//         const type = service.getAttribute('data-service-type');
//         const name = service.getAttribute('data-name');
//         const address = service.getAttribute('data-address');
//         const phone = service.getAttribute('data-phone');
//
//         if (lat && lng) {
//             const marker = L.marker([lat, lng], {
//                 icon: getServiceIcon(type)
//             }).addTo(map);
//
//             // Add popup with service information
//             marker.bindPopup(`
//                 <div class="popup-content">
//                     <h3>${name}</h3>
//                     <p>${address}</p>
//                     <p>${phone}</p>
//                 </div>
//             `);
//         }
//     });
//
//     // Handle service type filter changes
//     document.querySelectorAll('.checkbox-label input[type="checkbox"]').forEach(checkbox => {
//         checkbox.addEventListener('change', function() {
//             const serviceType = this.id.replace('show-', '');
//             const isChecked = this.checked;
//
//             document.querySelectorAll(`[data-service-type="${serviceType}"]`).forEach(service => {
//                 const lat = parseFloat(service.getAttribute('data-lat'));
//                 const lng = parseFloat(service.getAttribute('data-lng'));
//
//                 if (isChecked) {
//                     // Add marker if checkbox is checked
//                     L.marker([lat, lng], {
//                         icon: getServiceIcon(serviceType)
//                     }).addTo(map);
//                 } else {
//                     // Remove marker if checkbox is unchecked
//                     map.eachLayer((layer) => {
//                         if (layer instanceof L.Marker) {
//                             const markerLatLng = layer.getLatLng();
//                             if (markerLatLng.lat === lat && markerLatLng.lng === lng) {
//                                 map.removeLayer(layer);
//                             }
//                         }
//                     });
//                 }
//             });
//         });
//     });
// });
//
// // View service details
// function viewService(id) {
//     console.log(`Viewing service ${id}`);
//     // Implementation for viewing service details
// }
//
// // Show location on map
// function showLocation(lat, lng) {
//     const map = document.querySelector('#map')._leaflet_map;
//     // Use panTo instead of setView to maintain zoom level
//     map.panTo([lat, lng]);
// }
//
// // Handle emergency type filter change
// document.getElementById('emergency-type').addEventListener('change', function() {
//     const selectedType = this.value;
//     // Implementation for filtering by emergency type
// });
//
// // Handle status filter change
// document.getElementById('status').addEventListener('change', function() {
//     const selectedStatus = this.value;
//     // Implementation for filtering by status
// });
//
// // Handle time range filter change
// document.getElementById('time-range').addEventListener('change', function() {
//     const selectedRange = this.value;
//     // Implementation for filtering by time range
// });
//
// async function showResources(serviceId, serviceName, serviceType) {
//     try {
//         const response = await fetch(`/api/services/${serviceId}/resources`);
//         const data = await response.json();
//
//         // Show the resources panel
//         document.getElementById('resources-panel').style.display = 'block';
//
//         // Update service details
//         document.getElementById('service-details').innerHTML = `
//             <div class="service-header ${serviceType}">
//                 <h4>${serviceName}</h4>
//                 <span class="service-type">${serviceType}</span>
//             </div>
//         `;
//
//         // Update equipment list
//         document.getElementById('equipment-list').innerHTML = data.equipment.map(item => `
//             <div class="resource-item ${item.available > 0 ? 'available' : 'unavailable'}">
//                 <div class="resource-header">
//                     <span>${item.name}</span>
//                     <span>${item.available}/${item.quantity}</span>
//                 </div>
//                 <div>Status: ${item.condition}</div>
//             </div>
//         `).join('');
//
//         // Update vehicles list
//         document.getElementById('vehicles-list').innerHTML = data.vehicles.map(item => `
//             <div class="resource-item ${item.status === 'available' ? 'available' : 'unavailable'}">
//                 <div class="resource-header">
//                     <span>${item.type} - ${item.model}</span>
//                     <span>${item.status}</span>
//                 </div>
//                 <div>Plate: ${item.plate_number}</div>
//             </div>
//         `).join('');
//
//         // Update personnel list
//         document.getElementById('personnel-list').innerHTML = data.personnel.map(item => `
//             <div class="resource-item ${item.status === 'on-duty' ? 'available' : 'unavailable'}">
//                 <div class="resource-header">
//                     <span>${item.name}</span>
//                     <span>${item.status}</span>
//                 </div>
//                 <div>Role: ${item.role}</div>
//                 <div>Specialty: ${item.speciality}</div>
//             </div>
//         `).join('');
//
//     } catch (error) {
//         console.error('Error loading resources:', error);
//     }
// }
//
// // Delete service
// function deleteService(id) {
//     if (confirm('Are you sure you want to delete this service?')) {
//         fetch(`/api/services/${id}`, {
//             method: 'DELETE',
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => {
//             if (response.ok) {
//                 location.reload();
//             } else {
//                 throw new Error('Failed to delete service');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('Failed to delete service. Please try again.');
//         });
//     }
// }
//
// // Update current time
// function updateCurrentTime() {
//     const currentTime = new Date();
//     document.querySelector('.admin-info span:first-child').textContent =
//         `Current Time: ${currentTime.toISOString().replace('T', ' ').slice(0, 19)}`;
// }
//
// // Update time every minute
// setInterval(updateCurrentTime, 60000);
//
// // Initial time update
// updateCurrentTime();

// Initialize map when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    const map = L.map('emergency-map').setView([38.2749497, 23.8102717], 7);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add markers for all emergency reports with locations
    const reports = document.querySelectorAll('.view-location-btn');
    reports.forEach(report => {
        const lat = parseFloat(report.getAttribute('data-lat'));
        const lng = parseFloat(report.getAttribute('data-lng'));
        if (lat && lng) {
            L.marker([lat, lng]).addTo(map);
        }
    });
});

// View report details
function viewReport(id) {
    // Implement view report functionality
    console.log(`Viewing report ${id}`);
    // You can implement a modal or redirect to a details page
}

// Show location on map
function showLocation(lat, lng) {
    // Center map on the location
    const map = document.querySelector('#emergency-map')._leaflet_map;
    map.setView([lat, lng], 13);
}

// Delete report
function deleteReport(id) {
    if (confirm('Are you sure you want to delete this report?')) {
        fetch(`/api/reports/${id}`, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.ok) {
                // Refresh the page to show updated data
                location.reload();
            } else {
                throw new Error('Failed to delete report');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete report. Please try again.');
        });
    }
}

// Auto-refresh the data every 30 seconds
setInterval(() => {
    location.reload();
}, 30000);