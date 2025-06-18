// Script Leaflet pour sélection de points de départ et d'arrivée
// Ce script doit être inclus sur les pages de publication de trajet

document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('map')) return;

    // Centré sur Cotonou par défaut
    var map = L.map('map').setView([6.4, 2.5], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    var departMarker = null;
    var arriveeMarker = null;
    var step = 0; // 0 = départ, 1 = arrivée

    function setMarker(lat, lng, type) {
        var icon = L.icon({
            iconUrl: type === 'depart' ? 'https://cdn-icons-png.flaticon.com/512/684/684908.png' : 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
            iconSize: [32, 32],
            iconAnchor: [16, 32],
        });
        if (type === 'depart') {
            if (departMarker) map.removeLayer(departMarker);
            departMarker = L.marker([lat, lng], {icon: icon}).addTo(map).bindPopup('Départ').openPopup();
            document.getElementById('id_latitude_depart').value = lat;
            document.getElementById('id_longitude_depart').value = lng;
        } else {
            if (arriveeMarker) map.removeLayer(arriveeMarker);
            arriveeMarker = L.marker([lat, lng], {icon: icon}).addTo(map).bindPopup('Arrivée').openPopup();
            document.getElementById('id_latitude_arrivee').value = lat;
            document.getElementById('id_longitude_arrivee').value = lng;
        }
    }

    map.on('click', function (e) {
        if (step === 0) {
            setMarker(e.latlng.lat, e.latlng.lng, 'depart');
            step = 1;
            alert('Cliquez maintenant sur la carte pour choisir le point d\'arrivée.');
        } else {
            setMarker(e.latlng.lat, e.latlng.lng, 'arrivee');
            step = 0;
            alert('Points de départ et d\'arrivée sélectionnés.');
        }
    });

    // Optionnel : réinitialiser les points
    map.on('contextmenu', function () {
        if (departMarker) map.removeLayer(departMarker);
        if (arriveeMarker) map.removeLayer(arriveeMarker);
        departMarker = null;
        arriveeMarker = null;
        document.getElementById('id_latitude_depart').value = '';
        document.getElementById('id_longitude_depart').value = '';
        document.getElementById('id_latitude_arrivee').value = '';
        document.getElementById('id_longitude_arrivee').value = '';
        step = 0;
        alert('Sélection réinitialisée.');
    });
});
