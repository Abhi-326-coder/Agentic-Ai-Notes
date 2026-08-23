function getUserLocation() {
    // 1. Check if the browser supports Geolocation
    if (!navigator.geolocation) {
        console.error("Geolocation is not supported by your browser.");
        return;
    }

    // Optional optimization settings
    const options = {
        enableHighAccuracy: true, // Uses GPS if available
        timeout: 5000,            // Wait max 5 seconds
        maximumAge: 0             // Do not use cached location
    };

    // 2. Request the coordinates
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
}

// Handles successful location retrieval
function successCallback(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const accuracy = position.coords.accuracy;

    console.log(`Latitude: ${latitude}`);
    console.log(`Longitude: ${longitude}`);
    console.log(`Accurate within ${accuracy} meters.`);
}

// Handles errors or user rejections
function errorCallback(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.error("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            console.error("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.error("The request to get user location timed out.");
            break;
        default:
            console.error("An unknown error occurred.", error.message);
    }
}

// Execute the function
getUserLocation();
