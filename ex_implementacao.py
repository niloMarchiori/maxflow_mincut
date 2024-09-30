import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from models.graph import *

# Classe criada apenas para o grafo de exemplo, mas herda todos os
# métodos de um grafo padrão, a particularidade é que as posições
# dos vértices nesse caso pode ser fixada, por ser um grafo particularizado
class ExGraph(Graph):
    def __init__(self,n=0):
        super().__init__(n)

    # Diferente do FF padrão, esse método salva o grafo residual e de fluxos como uma imagem //
    # no diretório Results/Ex/
    def step_save_FF_by_edmond_karp(self, sources, sinks):
        frame = 0
        max_flow = 0
        
        
        s = sources[0]
        t = sinks[0]

        parent, visited = self.bfs(0, t)
        # Desenha o grafo residual
        self.draw_ex(residual_graph=True, fig_name=f'ex_residgraph{frame}.png', output_dir='Results/Ex/')
        # Desenha a rede de fluxo
        self.draw_ex(residual_graph=False, fig_name=f'ex_flowgraph{frame}.png', output_dir='Results/Ex/')
    

        while parent:
            frame += 1
            increment_flow = float('inf')
            v = t
            while v != s:
                increment_flow = min(increment_flow, self.residual_graph[parent[v]][v])
                v = parent[v]
            max_flow += increment_flow

            v = t
            while v != s:
                u = parent[v]
                self.send_flow(u, v, increment_flow)
                self.increment_edge(u, v, -increment_flow)
                self.increment_edge(v, u, increment_flow)
                v = u

            parent, visited = self.bfs(s, t)
            self.draw_ex(residual_graph=True, fig_name=f'ex_residgraph{frame}.png', output_dir='Results/Ex/')
            self.draw_ex(residual_graph=False, fig_name=f'ex_flowgraph{frame}.png', output_dir='Results/Ex/')
            

        result = {'val': max_flow, 'mincut_edges': [], 's_conected': visited}
        for i in range(self.size):
            if visited[i]:
                for j, f in enumerate(self.flow[i]):
                    if f > 0 and not visited[j]:
                        result['mincut_edges'].append((i, j))

        return result

    def draw_ex(self, residual_graph=False, colors=['lightblue'], output_dir='Results/', fig_name='plot.png'):
        G = nx.DiGraph()
        for i in range(self.size):
            G.add_node(i)
        if residual_graph:
            graph = self.residual_graph
        else:
            graph = self.graph

        for i in range(self.size):
            for j in range(self.size):
                f = self.flow[i][j]
                c = graph[i][j]
                if graph[i][j] > 0 or self.flow[i][j]:
                    if residual_graph:
                        G.add_edge(i, j, label=c)
                    else:
                        G.add_edge(i, j, label=f'{f}/{c}')

        pos = {0: (0, 1), 1: (1, 1.5), 2: (1, 0.5), 3:(2, 1)}

        # Desenhar os nós e as arestas
        nx.draw(G, pos, with_labels=True, node_color=colors, font_weight='bold', arrows=True, connectionstyle='arc3,rad=0.02',)

        # Desenhar os rótulos dos pesos das arestas
        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.3,font_size=22)

        # Salvando a imagem do grafo
        plt.savefig(output_dir + fig_name)
        plt.close()

   

    

if __name__=='__main__':
    graph = [[0, 10, 20, 0],
             [0, 0,  0,  15],
             [0, 10,  0,  6],
             [0, 0,  0,  0]]
    
    g = ExGraph(4)
    g.set_graph(graph)

    source = [0]; sink = [3]
    result=g.step_save_FF_by_edmond_karp(source, sink)
    for chave in result:
        print(chave,':',result[chave])
    