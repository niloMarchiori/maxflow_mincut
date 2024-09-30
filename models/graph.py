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
    
    # Atribui diretamente uma matriz de adjacências à um grafo
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
        parent,visited=self.bfs(0,t)

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

if __name__=='__main__':
    graph = [[0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0]]
    
    g = Graph(6)
    g.set_graph(graph)

    source = 0; sink = 5
    result=g.FF_by_edmond_karp(source, sink)
    for chave in result:
        print(chave,':',result[chave])
    