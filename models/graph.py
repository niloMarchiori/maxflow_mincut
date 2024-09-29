import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Graph():
    def __init__(self,n=0):
        self.size=n
        self.graph=[[0]*(n+1) for _ in range(n+1)]
        self.residual_graph=[[0]*(n+1) for _ in range(n+1)]
        self.flow=[[0]*(n+1) for _ in range(n+1)]

    def increment_edge(self,i,j,residual_graph):
        self.residual_graph[i][j]+=residual_graph

    def send_flow(self,i,j,flow):
        self.flow[i][j]+=flow
    
    def set_graph(self,matrix):
        self.residual_graph=np.array(matrix)
        self.graph=np.array(matrix)
        
        self.size=len(matrix)
        self.flow=[[0]*self.size for _ in range(self.size)]

    def bfs(self,s,t):
        visited=[False]*(self.size)
        parent=[-1]*(self.size)

        queue=[]

        queue.append(s)
        visited[s]=True

        while queue:
            u=queue.pop(0)

            for i,c in enumerate(self.residual_graph[u]):
                if visited[i]==False and c>0:
                    queue.append(i)
                    visited[i]=True
                    parent[i]=u
                    if i==t:
                        return parent,visited
        return [],visited
    
    def FF_by_edmond_karp(self,s,t):
        max_flow=0
        parent,visited=self.bfs(s,t)

        while parent:
            increment_flow=float('inf')
            v=t
            while v!=s:
                increment_flow=min(increment_flow,self.residual_graph[parent[v]][v])
                v=parent[v]
            max_flow+=increment_flow


            v=t
            while v!=s:
                u=parent[v]
                self.send_flow(u,v,increment_flow)
                self.increment_edge(u,v,-increment_flow)
                self.increment_edge(v,u,increment_flow)
                v=u

            parent,visited=self.bfs(s,t)

        result={'val':max_flow,'mincut_edges':[],'s_conected':visited}
        for i in range(self.size):
            if visited[i]:
                for j,f in enumerate(self.flow[i]):
                    if f>0 and not visited[j]:
                        result['mincut_edges'].append((i,j))

        return result

    def draw(self,residual_graph=False,colors=['lightblue'],exit_dir='Results/',fig_name='plot.png'):
        G = nx.DiGraph()
        if residual_graph:
            graph=self.residual_graph
        else:
            graph=self.graph
        for i in range(self.size):
            for j in range(self.size):
                if graph[i][j]>0:
                    G.add_edge(i,j,weight=graph[i][j])
        
        pos = nx.spring_layout(G)

        # Desenhar os nós e as arestas
        nx.draw(G,pos, with_labels=True, node_color=colors, font_weight='bold', arrows=True)

        # Desenhar os rótulos dos pesos das arestas
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        # Plotando o grafo

        plt.savefig(exit_dir+fig_name)
        plt.close()
    def draw_gridgraph(self,n,m,residual_graph=False,colors=['lightblue'],exit_dir='Results/',fig_name='plot.png'):
        G = nx.DiGraph()
        if residual_graph:
            graph=self.residual_graph
        else:
            graph=self.graph
        pos={}

        node=0
        for i in range(n-1,-1,-1):
            for j in range(m):
                G.add_node(node)
                pos[node]=(j,i)
                node+=1

        for i in range(self.size):
            for j in range(self.size):
                if graph[i][j]>0:
                    G.add_edge(i,j,weight=graph[i][j])
        
        # Desenhar os nós e as arestas
        nx.draw(G,pos, with_labels=True, node_color=colors, font_weight='bold', arrows=True,connectionstyle='arc3,rad=0.2')

        # Desenhar os rótulos dos pesos das arestas
        # labels = nx.get_edge_attributes(G, 'weight')
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels,label_pos=0.3)
        # Plotando o grafo
        plt.savefig(exit_dir+fig_name)
        plt.close()
    

if __name__=='__main__':
    graph = [[0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0]]
    
    g = Graph(5)
    g.set_graph(graph)

    source = 0; sink = 5
    result=g.FF_by_edmond_karp(source, sink)

    colors=['lightblue']*g.size
    for i in range(g.size):
        if result['s_conected'][i]:
            colors[i]='red'
    g.draw(fig_name='graph.png',colors=colors)
    g.draw(residual_graph=True,fig_name='residual_graph.png',colors=colors)
    for chave in result:
        print(chave,':',result[chave])
    