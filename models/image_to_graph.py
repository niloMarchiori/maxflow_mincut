from PIL import Image
import numpy as np
from math import e

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

def rgbmatrix_to_graphmatrix(rgbmatrix):
    w=len(rgbmatrix)
    l=len(rgbmatrix[0])

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

def graph_to_image(visited,original_matrix,fig_name='imagem_rgb.png',output_dir='Results/Images'):
    n=len(original_matrix)
    m=len(original_matrix[0])
   
    matrix_rgb=np.array([[[0, 10, 230] for _ in range(m)] for _ in range(n)], dtype=np.uint8)
    for i,vertex in enumerate(visited):
        if vertex:
            l=i//m
            c=i%m
            matrix_rgb[l][c]=[230,10,0]

    imagem = Image.fromarray(matrix_rgb)
    imagem.save(output_dir+fig_name)
    

if __name__=='__main__':
    from graph import *
    fig_name='ex_3x3.png'
    image_dir ='Instances/Images/'+fig_name

    rgbmatrix=image_to_rgbmatrix(image_dir)
    n=len(rgbmatrix)
    m=len(rgbmatrix[0])

    graph=rgbmatrix_to_graphmatrix(rgbmatrix)
    g=Graph(len(graph))
    g.set_graph(graph)
    
    source = [0]
    
    sink = [8]
    result= g.FF_by_edmond_karp(source, sink)
    colors=['lightblue']*g.size
    for i in range(g.size):
        if i in sink:
            colors[i]='black'
        elif i in source:
            colors[i]='white'
        elif result['s_conected'][i]:
            colors[i]='red'

    g.draw_gridgraph(n,m,fig_name='graph_'+fig_name,colors=colors)
    g.draw_gridgraph(n,m,residual_graph=True,fig_name='residual_graph_'+fig_name,colors=colors)
    graph_to_image(result['s_conected'],rgbmatrix,fig_name,output_dir='Results/')
    print('OK')