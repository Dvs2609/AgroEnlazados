document.addEventListener('DOMContentLoaded', function() {  
    var map = L.map('map');

    // Agrega una capa de OpenStreetMap al mapa
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; OpenStreetMap contributors'
    }).addTo(map);

    // Crea un objeto L.latLngBounds vacío
    var bounds = L.latLngBounds();

    // Agrega marcadores para cada cooperativa y extiende los límites
    {% for cooperativaMapa in cooperativaMapa %}
        {% if cooperativaMapa.latitude and cooperativaMapa.longitude %}
            var marker = L.marker([{{ cooperativaMapa.latitude }}, {{ cooperativaMapa.longitude }}]).addTo(map);
            marker.bindPopup("<strong>{{ cooperativaMapa.denominación_social }}</strong><br>{{ cooperativaMapa.localidad_coop }}, {{ cooperativaMapa.provincia_coop }}");
            
            // Extiende los límites para incluir las coordenadas del marcador
            bounds.extend(marker.getLatLng());
        {% endif %}
    {% endfor %}

    // Ajusta la vista del mapa para que todos los marcadores sean visibles
    map.fitBounds(bounds);

    function zoomToCoop(lat, lon) {
        if (!isNaN(lat) && !isNaN(lon)) {
            map.setView([lat, lon], 14);
        }
    }

 // Agregar evento de clic a las celdas de la columna "Número de inscripción"
    var table = document.getElementById('cooperativa-table');
    table.addEventListener('click', function(event) {
        var target = event.target;
        if (target.classList.contains('coop-link')) {
            event.preventDefault(); // Evita que se siga el enlace
            var lat = parseFloat(target.getAttribute('data-lat'));
            var lon = parseFloat(target.getAttribute('data-lon'));
            zoomToCoop(lat, lon);
        }
    });
});