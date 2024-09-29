from PIL import Image
import numpy as np
from math import e
from graph import *

def image_to_rgbmatrix(image_dir):
    imagem = Image.open(image_dir)

    imagem_rgb = imagem.convert('RGB')
    matriz_pixels = np.array(imagem_rgb)

    return matriz_pixels
    
def cij(cor1,cor2,sigma=20,decimal=5):
    c=np.array(cor1,dtype=int)-np.array(cor2,dtype=int)
    dij= np.linalg.norm(c)
    x=int(e**(-dij/sigma)*10**decimal)
    return x

def rgbmatrix_to_graphmatrix(rgbmatix):
    w=len(rgbmatrix)
    l=len(rgbmatrix)

    visited=[[False]*l for _ in range(w)]
    graph=[[0]*l*w for _ in range(w*l)]
    
    n=0
    for i in range(w):
        for j in range(l):
            if i==0:
                graph[n][n+l]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j])
                graph[n+l][n]=graph[n][n+l]
                if j+1<l:
                    graph[n][n+1]=cij(rgbmatrix[i][j],rgbmatrix[i][j+1])
                    graph[n+1][n]=graph[n][n+1]
                    graph[n][n+l+1]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j+1])
                    graph[n+l+1][n]=graph[n][n+l+1]

            elif i==(w-1) and (j+1<l):
                graph[n][n+1]=cij(rgbmatrix[i][j],rgbmatrix[i][j+1])
                graph[n+1][n]=graph[n][n+1]
                graph[n][n-l+1]=cij(rgbmatrix[i][j],rgbmatrix[i-1][j+1])
                graph[n-l+1][n]=graph[n][n-l+1]
            
            
            elif n+1<w*l:
                graph[n][n+l]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j])
                graph[n+l][n]=graph[n][n+l]
                if j+1<l:
                    graph[n][n+1]=cij(rgbmatrix[i][j],rgbmatrix[i][j+1])
                    graph[n+1][n]=graph[n][n+1]
                    graph[n][n+l+1]=cij(rgbmatrix[i][j],rgbmatrix[i+1][j+1])
                    graph[n+l+1][n]=graph[n][n+l+1]
                    graph[n][n-l+1]=cij(rgbmatrix[i][j],rgbmatrix[i-1][j+1])
                    graph[n-l+1][n]=graph[n][n-l+1]
            n+=1
    return graph


if __name__=='__main__':
    fig_name='ex_3x3.png'
    image_dir ='Images/'+fig_name

    rgbmatrix=image_to_rgbmatrix(image_dir)
    n=len(rgbmatrix)
    m=len(rgbmatrix[0])

    graph=rgbmatrix_to_graphmatrix(rgbmatrix)
    g=Graph(len(graph))
    g.set_graph(graph)
    
    source = 0; sink = n*m-1
    result= g.FF_by_edmond_karp(source, sink)
    colors=['lightblue']*g.size
    for i in range(g.size):
        if result['s_conected'][i]:
            colors[i]='red'

    g.draw_gridgraph(n,m,fig_name='graph_'+fig_name,colors=colors)
    g.draw_gridgraph(n,m,residual_graph=True,fig_name='residual_graph_'+fig_name,colors=colors)
    for chave in result:
        print(chave,':',result[chave])
    