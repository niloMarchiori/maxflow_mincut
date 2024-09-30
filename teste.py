import networkx as nx

# Cria o grafo
G = nx.Graph()

# Adiciona arestas com labels na forma [a, b, c]
# Por exemplo: a aresta entre os nós 1 e 2 tem o label [1, 2, 3]
G.add_edge(1, 2, label=[1, 2, 3])
G.add_edge(2, 3, label=[4, 5, 6])
G.add_edge(3, 4, label=[7, 8, 9])

# Exibe as arestas e seus labels
for u, v, data in G.edges(data=True):
    print(f"Aresta ({u}, {v}) com label: {data['label']}")
