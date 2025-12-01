import networkx as nx

def find(parent, node):
    if parent[node] != node:
        parent[node] = find(parent, parent[node])
    return parent[node]

def union(parent, rank, u, v):
    root_u = find(parent, u)
    root_v = find(parent, v)

    if root_u != root_v:
        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        elif rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

def arbol_kruskal(G):
    MST = nx.Graph()
    MST.add_nodes_from(G.nodes())
    parent = {node: node for node in G.nodes()}
    rank = {node: 0 for node in G.nodes()}

    edges = sorted(G.edges(data=True), key = lambda x: x[2]['weight'])

    total_cost = 0

    for u, v, data in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)

        if root_u != root_v:
            # Agregar al MST
            MST.add_edge(u, v, weight=data['weight'])
            total_cost += data['weight']

            # Unir componentes
            union(parent, rank, root_u, root_v)

    print("Costo total del MST:", total_cost)

    return MST