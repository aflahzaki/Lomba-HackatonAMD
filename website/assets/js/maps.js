/**
 * LangkahKampus - Maps JavaScript
 * Leaflet.js map with university markers, filters, radius
 */

document.addEventListener('DOMContentLoaded', function() {
    initUniversityMap();
});

/* === University Map === */
function initUniversityMap() {
    var mapContainer = document.getElementById('map');
    if (!mapContainer || typeof L === 'undefined') return;

    // Initialize map centered on Indonesia
    var map = L.map('map').setView([-2.5, 118.0], 5);

    // Tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);

    // Sample university data
    var universities = [
        { name: 'Universitas Indonesia', lat: -6.3627, lng: 106.8273, type: 'PTN', accreditation: 'A', programs: 45, province: 'DKI Jakarta' },
        { name: 'Institut Teknologi Bandung', lat: -6.8915, lng: 107.6107, type: 'PTN', accreditation: 'A', programs: 38, province: 'Jawa Barat' },
        { name: 'Universitas Gadjah Mada', lat: -7.7713, lng: 110.3778, type: 'PTN', accreditation: 'A', programs: 52, province: 'DI Yogyakarta' },
        { name: 'Institut Teknologi Sepuluh Nopember', lat: -7.2819, lng: 112.7948, type: 'PTN', accreditation: 'A', programs: 35, province: 'Jawa Timur' },
        { name: 'Universitas Airlangga', lat: -7.2695, lng: 112.7630, type: 'PTN', accreditation: 'A', programs: 42, province: 'Jawa Timur' },
        { name: 'Universitas Diponegoro', lat: -7.0496, lng: 110.4380, type: 'PTN', accreditation: 'A', programs: 40, province: 'Jawa Tengah' },
        { name: 'Universitas Padjadjaran', lat: -6.9260, lng: 107.7734, type: 'PTN', accreditation: 'A', programs: 36, province: 'Jawa Barat' },
        { name: 'Universitas Brawijaya', lat: -7.9553, lng: 112.6145, type: 'PTN', accreditation: 'A', programs: 48, province: 'Jawa Timur' },
        { name: 'Universitas Hasanuddin', lat: -5.1332, lng: 119.4878, type: 'PTN', accreditation: 'A', programs: 35, province: 'Sulawesi Selatan' },
        { name: 'Universitas Sumatera Utara', lat: 3.5651, lng: 98.6561, type: 'PTN', accreditation: 'A', programs: 33, province: 'Sumatera Utara' }
    ];

    var markers = [];
    var markerLayer = L.layerGroup().addTo(map);

    // Custom marker icon
    var blueIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background:#1A73E8;width:24px;height:24px;border-radius:50%;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [24, 24],
        iconAnchor: [12, 12],
        popupAnchor: [0, -12]
    });

    var greenIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background:#27AE60;width:24px;height:24px;border-radius:50%;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [24, 24],
        iconAnchor: [12, 12],
        popupAnchor: [0, -12]
    });

    // Add markers
    function addMarkers(filteredData) {
        markerLayer.clearLayers();
        markers = [];

        filteredData.forEach(function(uni) {
            var icon = uni.type === 'PTN' ? blueIcon : greenIcon;
            var marker = L.marker([uni.lat, uni.lng], { icon: icon });

            marker.bindPopup(
                '<div style="min-width:200px;font-family:Inter,sans-serif;">' +
                '<h4 style="margin:0 0 8px;color:#2E4057;font-size:14px;">' + uni.name + '</h4>' +
                '<p style="margin:0 0 4px;font-size:12px;color:#6C757D;">' +
                '<strong>Tipe:</strong> ' + uni.type + '<br>' +
                '<strong>Akreditasi:</strong> ' + uni.accreditation + '<br>' +
                '<strong>Program Studi:</strong> ' + uni.programs + '<br>' +
                '<strong>Provinsi:</strong> ' + uni.province + '</p>' +
                '<a href="prediksi.php" style="display:inline-block;margin-top:8px;padding:4px 12px;background:#1A73E8;color:white;border-radius:4px;font-size:11px;text-decoration:none;">Prediksi untuk PTN ini</a>' +
                '</div>'
            );

            markerLayer.addLayer(marker);
            markers.push({ marker: marker, data: uni });
        });

        // Update count
        var countEl = document.getElementById('universityCount');
        if (countEl) countEl.textContent = filteredData.length;
    }

    addMarkers(universities);

    // === Filters ===
    var radiusSlider = document.getElementById('radiusSlider');
    var radiusValue = document.getElementById('radiusValue');
    var provinceFilter = document.getElementById('provinceFilter');
    var typeFilter = document.getElementById('typeFilter');
    var accreditationFilter = document.getElementById('accreditationFilter');

    var radiusCircle = null;
    var userLocation = null;

    // Radius slider
    if (radiusSlider) {
        radiusSlider.addEventListener('input', function() {
            var value = this.value;
            if (radiusValue) radiusValue.textContent = value + ' km';
            applyFilters();
        });
    }

    // Province filter
    if (provinceFilter) {
        provinceFilter.addEventListener('change', applyFilters);
    }

    // Type filter
    if (typeFilter) {
        typeFilter.addEventListener('change', applyFilters);
    }

    // Accreditation filter
    if (accreditationFilter) {
        accreditationFilter.addEventListener('change', applyFilters);
    }

    function applyFilters() {
        var filtered = universities.filter(function(uni) {
            var provinceMatch = !provinceFilter || !provinceFilter.value || uni.province === provinceFilter.value;
            var typeMatch = !typeFilter || !typeFilter.value || uni.type === typeFilter.value;
            var accMatch = !accreditationFilter || !accreditationFilter.value || uni.accreditation === accreditationFilter.value;
            return provinceMatch && typeMatch && accMatch;
        });

        addMarkers(filtered);

        // Update university list in sidebar
        updateUniversityList(filtered);
    }

    function updateUniversityList(data) {
        var list = document.getElementById('universityList');
        if (!list) return;

        list.innerHTML = '';

        data.forEach(function(uni) {
            var item = document.createElement('div');
            item.className = 'university-list-item';
            item.innerHTML = '<strong>' + uni.name + '</strong>' +
                '<small>' + uni.type + ' | ' + uni.province + ' | ' + uni.programs + ' prodi</small>';
            item.addEventListener('click', function() {
                map.setView([uni.lat, uni.lng], 12);
            });
            list.appendChild(item);
        });
    }

    updateUniversityList(universities);

    // Get user location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(pos) {
            userLocation = [pos.coords.latitude, pos.coords.longitude];
            map.setView(userLocation, 8);

            L.marker(userLocation, {
                icon: L.divIcon({
                    className: 'user-marker',
                    html: '<div style="background:#C0392B;width:16px;height:16px;border-radius:50%;border:3px solid white;box-shadow:0 0 10px rgba(192,57,43,0.5);"></div>',
                    iconSize: [16, 16],
                    iconAnchor: [8, 8]
                })
            }).addTo(map).bindPopup('Lokasi Anda');
        });
    }
}
