from models.graph import *
from models.image_to_graph import *
from math import e
from PIL import Image
import json

import os

def get_instances_graphs(instances_dir='Instances/',output_dir='Results/Graphs/'):
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
        with open(output_dir+file_name[:-4]+'_output.json', 'w') as json_file:
            json.dump(result, json_file, indent=4)
            
        



if __name__=='__main__':
    get_instances_graphs()
    