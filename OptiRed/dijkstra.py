import math
import heapq as hq

def dijkstra(G, start):
  # Diccionarios para manejar nodos con nombre
  visited = {n: False for n in G.nodes()}
  cost = {n: math.inf for n in G.nodes()}
  parent = {n: None for n in G.nodes()}
  cost[start] = 0
  pq = [(0, start)]

  while pq:
    g, u = hq.heappop(pq)

    if not visited[u]:
      visited[u] = True
    
      for v in G[u]:

        w = G[u][v]['weight'] # peso de la arista u — v
        f = g + w

        if not visited[v] and f < cost[v]:
          cost[v] = f
          parent[v] = u
          hq.heappush(pq, (f, v))

  return parent, cost

def ejecutar_dijkstra(G, origen, destino):
  parent, cost = dijkstra(G, origen)

  if cost[destino] == math.inf:
    return None, None
  
  # reconstruir ruta
  camino = []
  actual = destino

  while actual is not None:
    camino.append(actual)
    actual = parent[actual]

  camino.reverse()

  return camino, cost[destino]