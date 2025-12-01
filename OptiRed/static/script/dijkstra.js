function ejecutarDijkstra() {
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

            if (dijkstraLayer) map.removeLayer(dijkstraLayer);
            if (mstLayer) map.removeLayer(mstLayer);

            dijkstraLayer = L.featureGroup();

            for (let i = 0; i < data.coords.length - 1; i++) {
                const puntoA = data.coords[i];
                const puntoB = data.coords[i + 1];
                const nodoA = buscarNodoPorCoords(puntoA);
                const nodoB = buscarNodoPorCoords(puntoB);
                const peso = obtenerPesoEntre(nodoA, nodoB);

                L.polyline([puntoA, puntoB], {
                    weight: 4,
                    color: 'red'
                })
                    .bindPopup(`Peso: ${peso.toFixed(2)} km`)
                    .addTo(dijkstraLayer);
            }

            dijkstraLayer.addTo(map);
            map.fitBounds(dijkstraLayer.getBounds());

            setResultado(
                `Camino mínimo (Dijkstra):\n` +
                `${data.path.join(' → ')}\n\n` +
                `Distancia total:\n${data.distance.toFixed(2)} km`
            );
        });
}