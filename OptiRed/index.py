from flask import Flask, jsonify, render_template, request
from grafo import G
from dijkstra import ejecutar_dijkstra
from prim import arbol_prim
from kruskal import arbol_kruskal

app = Flask(__name__)

# Grafo a java
@app.route('/data/grafo')
def data_grafo():
    nodes = []
    edges = []

    for name, data in G.nodes(data=True):
        nodes.append({
            "id": name,
            "lat": data["lat"],
            "lon": data["lon"],
            "distrito": data["distrito"],
            "label": f"{data['distrito']} - {name}"
        })

    for u, v in G.edges():
        edges.append({
            "from": u,
            "to": v,
            "coords": [
                [G.nodes[u]["lat"], G.nodes[u]["lon"]],
                [G.nodes[v]["lat"], G.nodes[v]["lon"]]
            ]
        })

    return jsonify({"nodes": nodes, "edges": edges})

# Dijkstra
@app.route('/dijkstra')
def api_dijkstra():
    origen = request.args.get('origen')
    destino = request.args.get('destino')

    if origen not in G or destino not in G:
        return jsonify({"error": "Nodo inválido"}), 400

    path, distancia = ejecutar_dijkstra(G, origen, destino)

    if path is None:
        return jsonify({"error": "No existe ruta"}), 400

    coords = [[G.nodes[n]["lat"], G.nodes[n]["lon"]] for n in path]

    return jsonify({
        "path": path,
        "distance": distancia,
        "coords": coords
    })

# Prim / Kruskal
@app.route('/mst')
def api_mst():
    alg = request.args.get("alg", "prim")

    if alg == "prim":
        mst = arbol_prim(G)
        nombre = "Prim"
    elif alg == "kruskal":
        mst = arbol_kruskal(G)
        nombre = "Kruskal"
    else:
        return jsonify({"error": "Algoritmo no válido"}), 400

    edges = []
    total_cost = 0

    for u, v, data in mst.edges(data=True):
        edges.append([
            [G.nodes[u]["lat"], G.nodes[u]["lon"]],
            [G.nodes[v]["lat"], G.nodes[v]["lon"]]
        ])
        total_cost += data.get("weight", 0)

    return jsonify({
        "algoritmo": nombre,
        "edges": edges,
        "total_cost": total_cost
    })

# Routas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

if __name__ == '__main__':
    app.run(debug=True, port=5017)