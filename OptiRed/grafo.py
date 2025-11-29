import pandas as pd
import networkx as nx
import math
from nodos_extras import conexiones_extra

def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def construir_grafo():
    excel = pd.read_csv("Cobertura móvil por empresa operadora.csv")

    G = nx.Graph()

    excel_sorted = excel.sort_values(by=['LATITUD', 'LONGITUD'], ascending=[False, True])

    # Nodos
    for idx, row in excel_sorted.iterrows():
        nombre = row['CENTRO_POBLADO']
        distrito = row['DISTRITO']

        latitud = row['LATITUD']
        longitud = row['LONGITUD']

        G.add_node(nombre, lat=latitud, lon=longitud, distrito=distrito)

    # Aristas 
    for n1 in G.nodes():
        for n2 in G.nodes():
            if n1 != n2:
                lat1 = G.nodes[n1]['lat']
                lon1 = G.nodes[n1]['lon']
                lat2 = G.nodes[n2]['lat']
                lon2 = G.nodes[n2]['lon']

                d = distancia_km(lat1, lon1, lat2, lon2)

                if d < 3:
                    G.add_edge(n1, n2, weight=d)

    # Conexiones extra
    for u, v in conexiones_extra:
        if u in G.nodes and v in G.nodes:
            G.add_edge(u, v)

    # Calcular pesos
    for u, v in G.edges():
        lat1 = G.nodes[u]['lat']
        lon1 = G.nodes[u]['lon']
        lat2 = G.nodes[v]['lat']
        lon2 = G.nodes[v]['lon']
        G[u][v]['weight'] = distancia_km(lat1, lon1, lat2, lon2)

    return G

G = construir_grafo()