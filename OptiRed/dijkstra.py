import networkx as nx

def ejecutar_dijkstra(G, origen, destino):
    try:
        path = nx.dijkstra_path(G, origen, destino, weight='weight')
        distancia = nx.dijkstra_path_length(G, origen, destino, weight='weight')
        return path, distancia
    except:
        return None, None