let grafoCompleto = null;
let dijkstraLayer = null;
let mstLayer = null;
let nodosTecnicos = L.layerGroup();
let aristasTecnicas = L.layerGroup();
let nodosUsuario = L.layerGroup();

const select = document.getElementById('opciones');
const dijkstraPanel = document.getElementById('dijkstra-panel');
const panelTitle = document.getElementById('panel-titulo');
const respuestaOrigen = document.getElementById('respuesta-origen');
const respuestaDestino = document.getElementById('respuesta-destino');
const origenInput = document.getElementById('origen');
const destinoInput = document.getElementById('destino');
const btnCalcular = document.getElementById('btn-calcular');
const resultadoDiv = document.getElementById('resultado');
const btnUsuario = document.getElementById('btn-usuario');
const btnTecnico = document.getElementById('btn-tecnico');
const map = L.map('map').setView([-12.0464, -77.0428], 9);

const iconoUsuario = L.icon({
    iconUrl: '/static/img/antenna-1.svg',
    iconSize: [38, 38],
    iconAnchor: [19, 38],
    popupAnchor: [0, -38]
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: 'OptiRed',
    tileSize: 512,
    zoomOffset: -1,
    minZoom: 1,
    crossOrigin: true
}).addTo(map);

// Cargar grafo
fetch('/data/grafo')
    .then(response => response.json())
    .then(data => {
        grafoCompleto = data;

        const markers = [];
        const datalist = document.getElementById('lista-nodos');

        grafoCompleto.nodes.sort((a, b) => a.label.localeCompare(b.label));

        grafoCompleto.nodes.forEach(nodo => {
            const option = document.createElement('option');
            option.value = nodo.label;
            option.setAttribute("data-id", nodo.id);
            datalist.appendChild(option);
        });

        grafoCompleto.nodes.forEach(nodo => {
            const marker = L.circleMarker([nodo.lat, nodo.lon], { radius: 4 })
                .bindPopup(`<b>${nodo.distrito} - ${nodo.id}</b>`);
            nodosTecnicos.addLayer(marker);
            markers.push([nodo.lat, nodo.lon]);
        });

        grafoCompleto.edges.forEach(edge => {
            L.polyline(edge.coords, { weight: 2 })
                .bindPopup(`Peso: ${edge.weight.toFixed(2)} km`)
                .addTo(aristasTecnicas);
        });

        grafoCompleto.nodes.forEach(nodo => {
            L.marker([nodo.lat, nodo.lon], { icon: iconoUsuario })
                .bindPopup(`<b>${nodo.distrito}</b><br>${nodo.id}`)
                .addTo(nodosUsuario);
        });

        nodosUsuario.addTo(map);

        if (markers.length > 0) map.fitBounds(markers);
    });

function obtenerPesoEntre(a, b) {
    if (!grafoCompleto) return null;

    const e = grafoCompleto.edges.find(edge =>
        (edge.from === a && edge.to === b) ||
        (edge.from === b && edge.to === a)
    );

    return e ? e.weight : null;
}

function buscarNodoPorCoords([lat, lon]) {
    const nodo = grafoCompleto.nodes.find(n =>
        Math.abs(n.lat - lat) < 0.000001 &&
        Math.abs(n.lon - lon) < 0.000001
    );

    return nodo ? nodo.id : null;
}

btnUsuario.addEventListener('click', () => {
    map.removeLayer(nodosTecnicos);
    map.removeLayer(aristasTecnicas);

    if (mstLayer) map.removeLayer(mstLayer);
    if (dijkstraLayer) map.removeLayer(dijkstraLayer);

    map.addLayer(nodosUsuario);
    setResultado("Modo Usuario, mostrando antenas.");
});

btnTecnico.addEventListener('click', () => {
    map.removeLayer(nodosUsuario);
    map.addLayer(nodosTecnicos);
    map.addLayer(aristasTecnicas);

    setResultado("Modo Técnico, mostrando grafo.");
});

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
        panelTitle.textContent = "Ruta con Dijkstra";
        respuestaOrigen.style.display = "flex";
        respuestaDestino.style.display = "flex";
    }
    else {
        panelTitle.textContent = "Árbol de Expansión Mínima - Kruskal";
        respuestaOrigen.style.display = "none";
        respuestaDestino.style.display = "none";
        dibujarMST();
    }
}

btnCalcular.addEventListener('click', () => {
    const opcion = select.value;

    if (opcion === "1") ejecutarDijkstra();
    else dibujarMST();
});

select.addEventListener('change', actualizarPanel);
actualizarPanel();

function setResultado(texto) {
    resultadoDiv.textContent = texto;
}