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

    # Conexiones adicionales
    conexiones_extra = [
        ('LOS VIÑOS', 'EL PORVENIR'), ('LOS VIÑOS', 'CALETA VIDAL'), ('LOS VIÑOS', 'CAMAY'), ('LOS VIÑOS', 'MEDIO MUNDO'),
        ('CARAL', 'TOSHI'), ('CARAL', 'SANTA JUANA'),
        ('ARAYA GRANDE', 'CHURLIN BAJO ( SANTA ROSA DE CHURLIN )'), ('ARAYA GRANDE', 'VIRGEN DEL ROSARIO'), ('ARAYA GRANDE', 'RONCADOR'),
        ('CHURLIN BAJO ( SANTA ROSA DE CHURLIN )', 'CARRETERIA'),
        ('CARBONERA', 'LAMPAY'), ('CARBONERA', 'TUNSAN'),
        ('HOYA GRANDE', 'CHUSIN'),
        ('BALCONCILLO', 'VILCAHUAURA'),
        ('SARAPE', 'SANTA TERESA BAJA'),
        ('SAN MIGUEL DE ARCA ANGEL', 'MANCO CAPAC (EL CARMEN)'), ('SAN MIGUEL DE ARCA ANGEL', 'ANDAHUASI (COOPERATIVA)'), ('SAN MIGUEL DE ARCA ANGEL', 'GANZO AZUL'),
        ('HORNO ALTO', 'GANZO AZUL'),
        ('EL SOLITARIO', 'PLAYA CHICA'), ('EL SOLITARIO', 'TABLADA'),
        ('LA UNION BAJA', 'TABLADA'),
        ('LA YESERA', 'PLAYA CHICA'),
        ('LA SALINAS', 'LOS TRIGALES'),
        ('LOS TRIGALES', 'ROCIO'), ('LOS TRIGALES', 'SANTA ANITA'),
        ('EL HATILLO', 'PAMPA CENIZAL'), ('EL HATILLO', 'SAN CAYETANO'), ('EL HATILLO', 'LOS ALAMOS'),
        ('PAMPA CENIZAL', 'SANTA VICTORIA'),
        ('JECUAN', 'SAN CAYETANO'), ('JECUAN', 'NUEVA ESTRELLA'),
        ('IWANCO', 'HARAS LA ESTANCIA'), ('IWANCO', 'CORONA'),
        ('EL TRES (HUAYAN CHICO)', 'TRONCONAL'),
        ('HUAYAN', 'CUYO'),
        ('LUNAVILCA', 'PAMPA EL INCA'), ('LUNAVILCA', 'CHANCAY'),
        ('ANCON', 'CHACRA Y MAR'), ('ANCON', 'TORRES DE COPACABANA'),
        ('TRES UNIDOS', 'VIRGEN DEL CARMEN DE QUIPAN'),
        ('LINDERO TRAPICHE', 'QUILCA'), ('LINDERO TRAPICHE', 'ZAPAN'),
        ('YANAPAMPA', 'VIRGEN DEL ROSARIO'), ('YANAPAMPA', 'CARAL'), ('YANAPAMPA', 'ARAYA GRANDE'), ('YANAPAMPA', 'MANAS'),
        ('MANAS', 'GORGOR'), ('MANAS', 'CAJAMARQUILLA'),
        ('UTCAS', 'COPA'), ('UTCAS', 'HUARNIJIRCA'), ('UTCAS', 'CAJAMARQUILLA'),
        ('CHIPOG', 'ISHANCORRAL'),
        ('HUANCAYOC', 'HUARUPAMPA'), ('HUANCAYOC', 'AIRA'), ('HUANCAYOC', 'POMACANCHA'),
        ('POMACANCHA', 'JAYACANCHA'), ('POMACANCHA', 'OYON'),
        ('ATLA', 'AUQUIN'),
        ('SHIRIPATA', 'PICO'),
        ('SECCHA', 'YARUSH'), ('SECCHA', 'SHAMPORAGRA'),
        ('SURA', 'PISHTAG HUASCAR'), ('SURA', 'GAU GAU'),
        ('GAU GAU', 'PUYHUAN'),
        ('CHURCURUMI', 'PISHTAG HUASCAR'),
        ('QUIVES', 'PUCARA'), ('QUIVES', 'LICAHUASI'), ('QUIVES', 'PICULLO'),
        ('ARAHUAY', 'SHIMAY'), ('ARAHUAY', 'CHACLIMA'), ('ARAHUAY', 'SURCA'), ('ARAHUAY', 'PAMPACOCHA'), ('ARAHUAY', 'VICAS'),
        ('YANE', 'SAN JOSE VIEJO'), ('YANE', 'HUAMANTANGA'), ('YANE', 'SAN CRISTOBAL'),
        ('YAPACOCHA', 'JUSHPA'), ('YAPACOCHA', 'COLLOTAYOK'), ('YAPACOCHA', 'LLAGUASHUASI'),
        ('YANACOCHA', 'CHACACANCHA'), ('YANACOCHA', 'HUACOS'),
        ('CHINCHILCAY', 'CANCAPUCRO'), ('CHINCHILCAY', 'BALCON'),
        ('CAPILLAYOC', 'COLLOTAYOK'),
        ('GRANJA N 180', 'SANTA ROSA DE MACAS'), ('GRANJA N 180', 'HORNILLOS'),
        ('SAN PEDRO DE CASTA', 'VICAS'), ('SAN PEDRO DE CASTA', 'SAN JUAN DE MAYHUAY'),
        ('CALLAHUANCA', 'SAN JUAN DE MAYHUAY'), ('CALLAHUANCA', 'PARCA (SANTA CRUZ DE PARCA ALTA)'),
        ('LA LIBERTAD', 'CARABAYLLO'), ('LA LIBERTAD', 'INDEPENDENCIA'), ('LA LIBERTAD', 'LAS PALMERAS'),
        ('BARRIO OBRERO INDUSTRIAL', 'INDEPENDENCIA'), ('BARRIO OBRERO INDUSTRIAL', 'BREÑA'), ('BARRIO OBRERO INDUSTRIAL', 'RIMAC'),
        ('JICAMARCA ANEXO 21', 'JICAMARCA ANEXO 24'), ('JICAMARCA ANEXO 21', 'FUNDO TORRE BLANCA (BLANCA)'),
        ('SURQUILLO', 'LINCE'), ('SURQUILLO', 'BARRANCO'),
        ('VILLA EL SALVADOR', 'VILLA MARIA DEL TRIUNFO'), ('VILLA EL SALVADOR', 'LOS ALMACIGOS'),
        ('CIUDAD DE DIOS', 'SANTIAGO DE SURCO'),
        ('CHACLACAYO', 'SAN FRANCISCO'), ('CHACLACAYO', 'SANTA ROSA DE CHONTAY (CHONTAY)'), ('CHACLACAYO', 'CHOSICA'),
        ('CIENEGUILLA', 'TAMBO INGA'), ('CIENEGUILLA', 'SAN FRANCISCO'),
        ('LA MOLINA', 'VITARTE'),
        ('SAN FRANCISCO DE BORJA', 'EL AGUSTINO'), ('SAN FRANCISCO DE BORJA', 'LA MOLINA'),
        ('SANTA ANITA - LOS FICUS', 'EL AGUSTINO'), ('SANTA ANITA - LOS FICUS', 'VITARTE'),
        ('CUCUYA', 'PAMPAPACTA'),
        ('PUNTA NEGRA', 'CERRO BOTIJA'), ('PUNTA NEGRA', 'CHANCHERIA'),
        ('HONDA', 'DON BRUNO'),
        ('VIRGEN DEL CARMEN', 'NICOCHAY'),
        ('SARAPAMPA', 'PLAYA LA RIVIERA FRANCESA'), ('SARAPAMPA', 'MAL PASO'),
        ('SAN JUAN DE IHUANCO', 'RIO AZUL'),
        ('LA GRANJA', 'BRISAS DE CONCON'), ('LA GRANJA', 'PALO'), ('LA GRANJA', 'SANTO DOMINGO'),
        ('NUEVO CAÑETE', 'BRISAS DE CONCON'),
        ('CALTOPILLA', 'INCAHUASI'),
        ('LANGLA', 'LUNAHUANA'),
        ('NUEVO CHAVIN', 'ROMANI'),
        ('APOTARA', 'ÑAUPAHUASI'),
        ('RICARDO PALMA', 'CHOSICA'), ('RICARDO PALMA', 'SUSANA PARODI'),
        ('NUEVO CUPICHE (SAN JUAN DE CUPICHE)', 'CORCONA'),
        ('LLUJULLUAIQUE', 'TAMBO'),
        ('CHACAHUARO', 'TAMBORAQUE'),
        ('MATIPARADA', 'LOS PINOS (CALZADA)'),
        ('EL SOLITARIO', 'PAMPA COLORADA'),
        ('PAMPA COLORADA', 'LA COLMENA'),
        ('LA COLMENA', 'HUACHO')
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