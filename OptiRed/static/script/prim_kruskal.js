function dibujarMST(alg) {
    fetch(`/mst?alg=${encodeURIComponent(alg)}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                setResultado(`Error: ${data.error}`);
                return;
            }

            if (mstLayer) map.removeLayer(mstLayer);
            if (dijkstraLayer) map.removeLayer(dijkstraLayer);

            mstLayer = L.featureGroup();
            const colorLinea = data.algoritmo === 'Prim' ? 'green' : 'purple';

            data.edges.forEach(coords => {
                const nodoA = buscarNodoPorCoords(coords[0]);
                const nodoB = buscarNodoPorCoords(coords[1]);
                const peso = obtenerPesoEntre(nodoA, nodoB);

                L.polyline(coords, {
                    weight: 4,
                    color: colorLinea
                })
                    .bindPopup(`Peso: ${peso.toFixed(2)} km`)
                    .addTo(mstLayer);
            });

            mstLayer.addTo(map);
            map.fitBounds(mstLayer.getBounds());

            setResultado(
                `Árbol de Expansión Mínima - ${data.algoritmo}:\n\n` +
                `Costo total:\n${data.total_cost.toFixed(2)} km`
            );
        });
}