import pandas as pd
import networkx as nx
import math

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
    excel = pd.read_excel("CoberturaMovil_v2.xlsx", sheet_name="Hoja 1")

    G = nx.Graph()

    excel_sorted = excel.sort_values(by=['LATITUD', 'LONGITUD'], ascending=[False, True])

    # Nodos
    for idx, row in excel_sorted.iterrows():
        nombre = row['CENTRO_POBLADO']
        latitud = row['LATITUD']
        longitud = row['LONGITUD']

        G.add_node(nombre, lat=latitud, lon=longitud)

    # Aristas 
    for n1 in G.nodes():
        for n2 in G.nodes():
            if n1 != n2:
                lat1 = G.nodes[n1]['lat']
                lon1 = G.nodes[n1]['lon']
                lat2 = G.nodes[n2]['lat']
                lon2 = G.nodes[n2]['lon']

                d = distancia_km(lat1, lon1, lat2, lon2)

                if d < 5:
                    G.add_edge(n1, n2, weight=d)

    # Conexiones adicionales
    conexiones_extra = [
        ('CHACLACAYO', 'CIENEGUILLA'), ('CHACLACAYO', 'SAN FRANCISCO'), ('CHACLACAYO', 'CHOSICA'), ('CHACLLA', 'SHIMAY'), ('CHACLLA', 'ARAHUAY'),
        ('VICAS', 'ARAHUAY'), ('VICAS', 'LARAOS'), ('MARCO', 'HUAMANTANGA'), ('ACOS', 'SAN AGUSTIN DE HUAYOPAMPA'), ('ACOS', 'SAN PEDRO DE HUAROQUIN'),
        ('ACOS', 'IHUARI'), ('ANCON', 'CHACRA Y MAR'), ('ANCON', 'GRAMADALES'), ('LANCHI', 'SANTO DOMINGO DE LOS OLLEROS'), ('LANCHI', 'MARIATANA'),
        ('LANCHI', 'HUANCATA'), ('LANCHI', 'SANTIAGO DE ANCHUCAYA'), ('SANTA ROSA', 'TORRES DE COPACABANA'), ('COTO', 'ESTADIO'), ('YANACOCHA', 'PIRCA'),
        ('YANACOCHA', 'HUACOS'), ('YANACOCHA', 'CHACACANCHA'), ('YAPACOCHA', 'JUSHPA'), ('YAPACOCHA', 'HUACOS'), ('CALLAHUANCA', 'HUALELUCMA'),
        ('SISICAYA', 'SANTA ROSA DE CHONTAY (CHONTAY)'), ('SISICAYA', 'TAMA'), ('ANTIOQUIA', 'TAMA'), ('ANTIOQUIA', 'SAN ANDRES DE TUPICOCHA'), ('ANTIOQUIA', 'CRUZ DE LAYA'),
        ('VILLA EL SALVADOR', 'VILLA MARIA DEL TRIUNFO'), ('VILLA EL SALVADOR', 'LOS ALMACIGOS'), ('VITARTE', 'LA MOLINA'), ('VITARTE', 'SANTA ANITA - LOS FICUS'), ('LA LIBERTAD', 'CARABAYLLO'),
        ('JICAMARCA ANEXO 21', 'FUNDO TORRE BLANCA (BLANCA)'), ('QUIVES', 'SHIMAY'), ('GRANJA N 180', 'COCAYALTA'), ('YANE', 'HUAMANTANGA'), ('YANE', 'SAN JOSE VIEJO'),
        ('HUAQUECHA', 'CHACAHUARO'), ('CHICLA', 'MATIPARADA'),
    ]

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