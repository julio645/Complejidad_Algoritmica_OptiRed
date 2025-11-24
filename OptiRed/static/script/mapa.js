// Inicia mapa
const map = L.map('map').setView([-12.0464, -77.0428], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: 'OptiRed'
}).addTo(map);

let dijkstraLayer = null;
let mstLayer = null;

fetch('/data/grafo')
    .then(response => response.json())
    .then(data => {
        const markers = [];

        // Dibujar nodos
        data.nodes.forEach(nodo => {
            const marker = L.circleMarker([nodo.lat, nodo.lon], { radius: 4 }).addTo(map);
            marker.bindPopup(`<b>${nodo.id}</b>`);
            markers.push([nodo.lat, nodo.lon]);
        });

        // Dibujar aristas
        data.edges.forEach(edge => {
            L.polyline(edge.coords, { weight: 1 }).addTo(map);
        });

        // Ajustar zoom para cubrir todo
        if (markers.length > 0) {
            map.fitBounds(markers);
        }
    });

const select = document.getElementById('opciones');
const dijkstraPanel = document.getElementById('dijkstra-panel');
const panelTitle = document.getElementById('panel-title');
const fieldOrigen = document.getElementById('field-origen');
const fieldDestino = document.getElementById('field-destino');
const origenInput = document.getElementById('origen');
const destinoInput = document.getElementById('destino');
const btnCalcular = document.getElementById('btn-calcular');
const resultadoDiv = document.getElementById('resultado');

function setResultado(texto) {
    resultadoDiv.textContent = texto;
}

// Grafo Prim / Kruskal
function dibujarMST(alg) {
    fetch(`/mst?alg=${encodeURIComponent(alg)}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                setResultado(`Error: ${data.error}`);
                return;
            }

            // Limpiar ruta previa
            if (mstLayer) {
                map.removeLayer(mstLayer);
            }
            if (dijkstraLayer) {
                map.removeLayer(dijkstraLayer);
                dijkstraLayer = null;
            }

            mstLayer = L.featureGroup();

            const colorLinea = data.algoritmo === 'Prim' ? 'green' : 'purple';

            data.edges.forEach(coords => {
                L.polyline(coords, {
                    weight: 4,
                    color: colorLinea
                }).addTo(mstLayer);
            });

            mstLayer.addTo(map);
            map.fitBounds(mstLayer.getBounds());

            setResultado(
                `Árbol de Expansión Mínima (${data.algoritmo}):\n\n` +
                `Costo total:\n${data.total_cost.toFixed(2)} km`
            );
        });
}

// Cambiar Grafo
function actualizarPanel() {
    const opcion = select.value;

    dijkstraPanel.style.display = 'block';

    // Limpiar capas
    if (dijkstraLayer) {
        map.removeLayer(dijkstraLayer);
        dijkstraLayer = null;
    }
    if (mstLayer) {
        map.removeLayer(mstLayer);
        mstLayer = null;
    }

    // Limpiar resultado
    setResultado("");

    if (opcion === "1") {
        // Dijkstra
        panelTitle.textContent = "Ruta con Dijkstra";
        fieldOrigen.style.display = "flex";
        fieldDestino.style.display = "flex";
    }

    if (opcion === "2") {
        // Prim
        panelTitle.textContent = "Árbol de Expansión Mínima (Prim)";
        fieldOrigen.style.display = "none";
        fieldDestino.style.display = "none";
        dibujarMST('prim');
    }

    if (opcion === "3") {
        // Kruskal
        panelTitle.textContent = "Árbol de Expansión Mínima (Kruskal)";
        fieldOrigen.style.display = "none";
        fieldDestino.style.display = "none";
        dibujarMST('kruskal');
    }
}

select.addEventListener('change', actualizarPanel);

// Estado inicial
actualizarPanel();

// Calcular Dijkstra
btnCalcular.addEventListener('click', () => {
    if (select.value !== "1") {
        setResultado("El botón 'Calcular' solo funciona con Dijkstra.");
        return;
    }

    const origen = origenInput.value.trim();
    const destino = destinoInput.value.trim();

    if (!origen || !destino) {
        setResultado("Por favor ingresa ambos nodos.");
        return;
    }

    fetch(`/dijkstra?origen=${encodeURIComponent(origen)}&destino=${encodeURIComponent(destino)}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                setResultado(`Error: ${data.error}`);
                return;
            }

            // Limpiar ruta anterior
            if (dijkstraLayer) map.removeLayer(dijkstraLayer);
            if (mstLayer) map.removeLayer(mstLayer);

            // Dibujar ruta
            dijkstraLayer = L.polyline(data.coords, {
                weight: 4,
                color: 'red'
            }).addTo(map);

            map.fitBounds(dijkstraLayer.getBounds());

            setResultado(
                `Camino mínimo (Dijkstra):\n` +
                `${data.path.join(' → ')}\n\n` +
                `Distancia total:\n${data.distance.toFixed(2)} km`
            );
        });
});
