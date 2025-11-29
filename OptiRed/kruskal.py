import networkx as nx

def arbol_kruskal(G):
    return nx.minimum_spanning_tree(G, algorithm='kruskal', weight='weight')
