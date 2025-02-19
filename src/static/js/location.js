document.addEventListener('DOMContentLoaded', function() {
    const coordsDisplay = document.getElementById('coordinates-display');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const locationStatus = document.getElementById('locationStatus');
    const submitBtn = document.getElementById('submitBtn');

    function handleLocationError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                locationStatus.textContent = "Please enable location services to continue";
                break;
            case error.POSITION_UNAVAILABLE:
                locationStatus.textContent = "Location information unavailable";
                break;
            case error.TIMEOUT:
                locationStatus.textContent = "Location request timed out";
                break;
            default:
                locationStatus.textContent = "Unable to get location";
        }
        locationStatus.classList.add('location-error');
        coordsDisplay.textContent = "Location not available";
    }

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            latitudeInput.value = latitude;
            longitudeInput.value = longitude;
            coordsDisplay.textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;

            locationStatus.textContent = "Location detected successfully";
            locationStatus.classList.remove('location-error');
            submitBtn.disabled = false;
        }, handleLocationError);
    } else {
        locationStatus.textContent = "Geolocation is not supported by your browser";
        locationStatus.classList.add('location-error');
        coordsDisplay.textContent = "Location not available";
    }
});