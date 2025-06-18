// Autocomplétion d'adresse avec Nominatim + affichage sur carte Leaflet
// Pour les champs #lieu_depart_autocomplete et #lieu_arrivee_autocomplete

document.addEventListener('DOMContentLoaded', function () {
    // Initialisation de la carte
    var map = L.map('map').setView([6.4, 2.5], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);
    var departMarker = null;
    var arriveeMarker = null;

    function autocomplete(inputId, suggestionsId, markerType) {
        var input = document.getElementById(inputId);
        var suggestions = document.getElementById(suggestionsId);
        input.addEventListener('input', function () {
            var query = input.value.trim();
            if (query.length < 3) {
                suggestions.style.display = 'none';
                suggestions.innerHTML = '';
                return;
            }
            fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(query))
                .then(response => response.json())
                .then(data => {
                    suggestions.innerHTML = '';
                    if (data.length === 0) {
                        suggestions.style.display = 'none';
                        return;
                    }
                    data.slice(0, 5).forEach(function (item) {
                        var div = document.createElement('div');
                        div.className = 'autocomplete-suggestion';
                        div.textContent = item.display_name;
                        div.addEventListener('click', function () {
                            input.value = item.display_name;
                            suggestions.style.display = 'none';
                            // Afficher le marqueur sur la carte
                            var lat = parseFloat(item.lat);
                            var lon = parseFloat(item.lon);
                            if (markerType === 'depart') {
                                if (departMarker) map.removeLayer(departMarker);
                                departMarker = L.marker([lat, lon], {icon: L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png', iconSize: [32,32], iconAnchor: [16,32]})}).addTo(map).bindPopup('Départ').openPopup();
                            } else {
                                if (arriveeMarker) map.removeLayer(arriveeMarker);
                                arriveeMarker = L.marker([lat, lon], {icon: L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png', iconSize: [32,32], iconAnchor: [16,32]})}).addTo(map).bindPopup('Arrivée').openPopup();
                            }
                            map.setView([lat, lon], 14);
                        });
                        suggestions.appendChild(div);
                    });
                    suggestions.style.display = 'block';
                });
        });
        // Cacher les suggestions si on clique ailleurs
        document.addEventListener('click', function (e) {
            if (!suggestions.contains(e.target) && e.target !== input) {
                suggestions.style.display = 'none';
            }
        });
    }

    autocomplete('lieu_depart_autocomplete', 'suggestions-depart', 'depart');
    autocomplete('lieu_arrivee_autocomplete', 'suggestions-arrivee', 'arrivee');
});
