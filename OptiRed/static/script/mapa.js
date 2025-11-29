const key = 'OptiRed';
const map = L.map('map').setView([-12.0464, -77.0428], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: 'OptiRed',
    tileSize: 512,
    zoomOffset: -1,
    minZoom: 1,
    crossOrigin: true
}).addTo(map);

let dijkstraLayer = null;
let mstLayer = null;

const select = document.getElementById('opciones');
const dijkstraPanel = document.getElementById('dijkstra-panel');
const panelTitle = document.getElementById('panel-titulo');
const respuestaOrigen = document.getElementById('respuesta-origen');
const respuestaDestino = document.getElementById('respuesta-destino');
const origenInput = document.getElementById('origen');
const destinoInput = document.getElementById('destino');
const btnCalcular = document.getElementById('btn-calcular');
const resultadoDiv = document.getElementById('resultado');

// Cargar grafo del Phyton
fetch('/data/grafo')
    .then(response => response.json())
    .then(data => {
        const markers = [];

        // Ordena alfabeticamente
        const datalist = document.getElementById('lista-nodos');

        // Ordenar POR LABEL (lo que se muestra)
        data.nodes.sort((a, b) => a.label.localeCompare(b.label));

        data.nodes.forEach(nodo => {
            const option = document.createElement('option');
            option.value = nodo.label;
            option.setAttribute("data-id", nodo.id);
            datalist.appendChild(option);
        });

        // Dibuja nodos
        data.nodes.forEach(nodo => {
            const marker = L.circleMarker([nodo.lat, nodo.lon], { radius: 4 }).addTo(map);
            marker.bindPopup(`<b>${nodo.id}</b>`);
            markers.push([nodo.lat, nodo.lon]);
        });

        // Dibuja aristas
        data.edges.forEach(edge => {
            L.polyline(edge.coords, { weight: 1 }).addTo(map);
        });

        // Ajustar el tamaño del mapa para mostrar los nodos
        if (markers.length > 0) {
            map.fitBounds(markers);
        }
    });

// Cambiar Grafo
function actualizarPanel() {
    const opcion = select.value;

    dijkstraPanel.style.display = 'block';

    if (dijkstraLayer) {
        map.removeLayer(dijkstraLayer);
        dijkstraLayer = null;
    }
    if (mstLayer) {
        map.removeLayer(mstLayer);
        mstLayer = null;
    }

    setResultado("");

    if (opcion === "1") {
        // Dijkstra
        panelTitle.textContent = "Ruta con Dijkstra";
        respuestaOrigen.style.display = "flex";
        respuestaDestino.style.display = "flex";
    }

    if (opcion === "2") {
        // Prim
        panelTitle.textContent = "Árbol de Expansión Mínima - Prim";
        respuestaOrigen.style.display = "none";
        respuestaDestino.style.display = "none";
        dibujarMST('prim');
    }

    if (opcion === "3") {
        // Kruskal
        panelTitle.textContent = "Árbol de Expansión Mínima - Kruskal";
        respuestaOrigen.style.display = "none";
        respuestaDestino.style.display = "none";
        dibujarMST('kruskal');
    }
}

function setResultado(texto) {
    resultadoDiv.textContent = texto;
}

select.addEventListener('change', actualizarPanel);

// Estado inicial
actualizarPanel();

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
                `Árbol de Expansión Mínima - ${data.algoritmo}:\n\n` +
                `Costo total:\n${data.total_cost.toFixed(2)} km`
            );
        });
}

// Calcular Dijkstra
btnCalcular.addEventListener('click', () => {
    if (select.value !== "1") {
        setResultado("El botón 'Calcular' solo funciona con Dijkstra.");
        return;
    }

    const origen = origenInput.value.trim().split(" - ").pop();
    const destino = destinoInput.value.trim().split(" - ").pop();

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