from models.graph import *
from models.image_to_graph import *
from math import e
from PIL import Image
import json

import os

def get_instances_graphs(instances_dir='Instances/Graphs/',output_dir='Results/Graphs/'):
    files_names=[]
    if os.path.exists(instances_dir) and os.path.isdir(instances_dir):
        for item in os.listdir(instances_dir):
            item_path = os.path.join(instances_dir, item)
            if os.path.isfile(item_path):
                files_names.append(item)
    else:
        print(f'O diretório {instances_dir} não existe ou não é um diretório.')

    for file_name in files_names:
        with open(instances_dir+file_name, 'r') as file:
            linhas = file.readlines()
        
        graph = []
        n = int(linhas[0].strip())   
        source = int(linhas[1].strip())
        sink = int(linhas[2].strip())

        graph = []
        for linha in linhas[3:]:
            numeros = list(map(int, linha.strip().split()))
            graph.append(numeros)
        
        g=Graph(n)
        g.set_graph(graph)
        result=g.FF_by_edmond_karp(source, sink)

        colors=['lightblue']*g.size
        for i in range(g.size):
            if result['s_conected'][i]:
                colors[i]='red'
        g.draw(fig_name=file_name[:-4]+'_graph.png',colors=colors, output_dir=output_dir)
        g.draw(residual_graph=True,fig_name=file_name[:-4]+'residual_graph.png',colors=colors,output_dir=output_dir)
        # with open(output_dir+file_name[:-4]+'_output.json', 'w') as json_file:
        #     json.dump(result, json_file, indent=4)
            
def get_instances_image_processing(pixel_source=0,pixel_sink=-1,image_dir ='Instances/Images/',output_dir='Results/Images/'):
    files_names=[]
    
    if os.path.exists(image_dir) and os.path.isdir(image_dir):
        for item in os.listdir(image_dir):
            item_path = os.path.join(image_dir, item)
            if os.path.isfile(item_path):
                files_names.append(item)
    else:
        print(f'O diretório {image_dir} não existe ou não é um diretório.')

    for fig_name in files_names:
    # for fig_name in ['ex_3x3.png']:
        rgbmatrix=image_to_rgbmatrix(image_dir+fig_name)
        n=len(rgbmatrix)
        m=len(rgbmatrix[0])
        if pixel_sink==-1:
            pixel_sink=m*n-1
        graph=rgbmatrix_to_graphmatrix(rgbmatrix)
        g=Graph(len(graph))
        g.set_graph(graph)

        result= g.FF_by_edmond_karp(pixel_source, pixel_sink)
        colors=['lightblue']*g.size
        colors=['lightblue']*g.size
        for i in range(g.size):
            if result['s_conected'][i]:
                colors[i]='red'

        g.draw_gridgraph(n,m,fig_name='graph_'+fig_name,colors=colors,output_dir=output_dir)
        g.draw_gridgraph(n,m,residual_graph=True,fig_name='residual_graph_'+fig_name,colors=colors,output_dir=output_dir)
        # with open(output_dir+file_name[:-4]+'_output.json', 'w') as json_file:
        #     json.dump(result, json_file, indent=4)


if __name__=='__main__':
    # get_instances_graphs()
    get_instances_image_processing()
    