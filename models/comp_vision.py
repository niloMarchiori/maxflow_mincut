from PIL import Image
import numpy as np
from math import e
# from models.graph import * #Comente essa linha caso execute esse script diretamente
from graph import * #Descomente essa linha caso execute esse script diretamente

# Emparticular, um grafo de imagem é gerado a partir de uma matriz rbg
class ImageGraph(Graph):
    def __init__(self,n,rgbmatrix):
        super().__init__(n)
        self.rgbmatrix=rgbmatrix

    # Ao desenhar o grafo que representa a imagem, em amarelo estão as fontes e em verde os sumidouros
    def draw_gridgraph(self,n,m,residual_graph=False,colors=['lightblue'],output_dir='Results/',fig_name='plot.png'):
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
        
        nx.draw(G,pos, with_labels=True, node_color=colors, font_weight='bold', arrows=True,connectionstyle='arc3,rad=0.2')
        plt.savefig(output_dir+fig_name)
        plt.close()
    
    def add_super_source(self,sources):
        self.residual_graph=np.insert(self.residual_graph,0,[0]*self.size,0)
        self.flow=np.insert(self.flow,0,[0]*self.size,0)
        self.size+=1
        self.residual_graph=np.insert(self.residual_graph,0,[0]*self.size,1)
        self.flow=np.insert(self.flow,0,[0]*self.size,1)
        for sources in sources:
            self.residual_graph[0][sources+1]=2**62

    def remove_super_source(self):
        self.size-=1
        self.residual_graph=np.delete(self.residual_graph,0,0)
        self.residual_graph=np.delete(self.residual_graph,0,1)
        self.flow=np.delete(self.flow,0,0)
        self.flow=np.delete(self.flow,0,1)

    def add_super_sinks(self,sinkss):
        self.residual_graph=np.insert(self.residual_graph,-1,[0]*self.size,0)
        self.flow=np.insert(self.flow,-1,[0]*self.size,0)
        self.size+=1
        self.residual_graph=np.insert(self.residual_graph,self.size-1,[0]*self.size,1)
        self.flow=np.insert(self.flow,self.size-1,[0]*self.size,1)
        for sinks in sinkss:
            self.residual_graph[sinks][-1]=2**62

    def remove_super_sinks(self):
        self.size-=1
        self.residual_graph=np.delete(self.residual_graph,-1,0)
        self.residual_graph=np.delete(self.residual_graph,-1,1)
        self.flow=np.delete(self.flow,-1,0)
        self.flow=np.delete(self.flow,-1,1)

    # Para melhorar o resultado do seccionamento de imagens, o algoritmo de FF
    # Para esse grafo admite múltiplas fontes, para isso antes de executar
    # o algoritmo ele insere super-fontes e super-sumidouros, mas ao fim os remove
    def Multi_source_FF_by_edmond_karp(self,sources,sinkss):
        max_flow=0

        super_source=False
        super_sinks=False

        if len(sources)==1:
            s=sources[0]
        else:
            super_source=True   
            s=0
            self.add_super_source(sources)
            for i in range(len(sinkss)):
                sinkss[i]+=1

        if len(sinkss)==1:
            t=sinkss[0]
        else:
            t=self.size
            super_sinks=True
            self.add_super_sinks(sinkss)
        
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

        if super_source:
            visited.pop(0)
            self.remove_super_source()
            for i in range(len(sinkss)):
                sinkss[i]-=1
            

        if super_sinks:
            visited.pop(-1)
            self.remove_super_sinks()
            

        result={'val':max_flow,'mincut_edges':[],'s_conected':visited}
        for i in range(self.size):
            if visited[i]:
                for j,f in enumerate(self.flow[i]):
                    if f>0 and not visited[j]:
                        result['mincut_edges'].append((i,j))

        return result
    
    # Transforma um grafo em uma imagem, em vermelho são os pixeis conectados às fontes, e em azul conectados
    # aos sumidouros após a execução de um FF
    def graph_to_image(self,visited,fig_name='imagem_rgb.png',output_dir='Results/Images'):
        n=len(self.rgbmatrix)
        m=len(self.rgbmatrix[0])
    
        matrix_rgb=np.array([[[0, 10, 230] for _ in range(m)] for _ in range(n)], dtype=np.uint8)
        for i,vertex in enumerate(visited):
            if vertex:
                l=i//m
                c=i%m
                matrix_rgb[l][c]=[230,10,0]

        imagem = Image.fromarray(matrix_rgb)
        imagem.save(output_dir+fig_name)

def image_to_rgbmatrix(image_dir):
    imagem = Image.open(image_dir)

    imagem_rgb = imagem.convert('RGB')
    matriz_pixels = np.array(imagem_rgb)

    return matriz_pixels
    
def cij(cor1,cor2,sigma=1,decimal=10):
    c=np.array(cor1,dtype=int)-np.array(cor2,dtype=int)
    dij= np.linalg.norm(c)
    x=int(e**(-dij/sigma)*10**decimal)
    return x

def rgbmatrix_to_graphmatrix(rgbmatrix,sigma=1):
    w=len(rgbmatrix)
    l=len(rgbmatrix[0])

    visited=[[False]*l for _ in range(w)]
    graph=[[0]*l*w for _ in range(w*l)]
    
    n=0
    for i in range(w):
        for j in range(l):
            if i==0:
                graph[n][n+l]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j],sigma)
                graph[n+l][n]=graph[n][n+l]
                if j+1<l:
                    graph[n][n+1]=cij(rgbmatrix[i][j],rgbmatrix[i][j+1],sigma)
                    graph[n+1][n]=graph[n][n+1]
                    graph[n][n+l+1]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j+1],sigma)
                    graph[n+l+1][n]=graph[n][n+l+1]

            elif i==(w-1) and (j+1<l):
                graph[n][n+1]=cij(rgbmatrix[i][j],rgbmatrix[i][j+1],sigma)
                graph[n+1][n]=graph[n][n+1]
                graph[n][n-l+1]=cij(rgbmatrix[i][j],rgbmatrix[i-1][j+1],sigma)
                graph[n-l+1][n]=graph[n][n-l+1]
            
            
            elif n+1<w*l:
                graph[n][n+l]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j],sigma)
                graph[n+l][n]=graph[n][n+l]
                if j+1<l:
                    graph[n][n+1]=cij(rgbmatrix[i][j],rgbmatrix[i][j+1],sigma)
                    graph[n+1][n]=graph[n][n+1]
                    graph[n][n+l+1]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j+1],sigma)
                    graph[n+l+1][n]=graph[n][n+l+1]
                    graph[n][n-l+1]=cij(rgbmatrix[i][j],rgbmatrix[i-1][j+1],sigma)
                    graph[n-l+1][n]=graph[n][n-l+1]
            n+=1
    return graph

def sectionalize_image(sources,sinks,fig_name,fig_dir='Instances/Images/',sigma=100, output_dir='Results/image/'):
    image_dir =fig_dir+fig_name

    rgbmatrix=image_to_rgbmatrix(image_dir)
    n=len(rgbmatrix)
    m=len(rgbmatrix[0])

    graph=rgbmatrix_to_graphmatrix(rgbmatrix,sigma=100)
    g=ImageGraph(len(graph),rgbmatrix)
    g.set_graph(graph)

    result= g.Multi_source_FF_by_edmond_karp(sources, sinks)
    colors=['lightblue']*g.size
    for i in range(g.size):
        if i in sinks:
            colors[i]='green'
        elif i in sources:
            colors[i]='yellow'
        elif result['s_conected'][i]:
            colors[i]='red'

    g.draw_gridgraph(n,m,fig_name='graph_'+fig_name,colors=colors,output_dir=output_dir)
    g.draw_gridgraph(n,m,residual_graph=True,fig_name='residual_graph_'+fig_name,colors=colors,output_dir=output_dir)
    g.graph_to_image(result['s_conected'],fig_name,output_dir=output_dir)
    print('OK')
    

if __name__=='__main__':
    from graph import *
    fig_name='ex_3x3.png'
    sectionalize_image(sources=[0],sinks=[8],fig_name=fig_name,output_dir='Results/Images')

    fig_name='mao_30x36.png'
    sectionalize_image(sources=[x for x in range(30)],sinks=[34*30+y for y in range(16,24)],fig_name=fig_name,output_dir='Results/Images')