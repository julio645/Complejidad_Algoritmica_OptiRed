import networkx as nx

def arbol_prim(G):
    return nx.minimum_spanning_tree(G, algorithm='prim', weight='weight')