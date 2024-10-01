from math import e
from PIL import Image
import json
import os
from models.comp_vision import * #Comente essa linha caso execute esse script diretamente
from models.graph import * #Comente essa linha caso execute esse script diretamente

def process_graphs_instances(instances_dir='Instances/Graphs/',output_dir='Results/Graphs/'):
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

        G = nx.DiGraph()
        for i in range(n):
            G.add_node(i)
        for i in range(n):
            for j in range(n):
                if graph[i][j] > 0:
                    G.add_edge(i, j, capacity=graph[i][j])

        flow_value_ek = nx.maximum_flow_value(G, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)

        print('Instância: ',file_name)
        print('Implementação_______', result['val'])
        print('Networkx:___________', flow_value_ek)
        print('Arestas de corte:___', result['mincut_edges'])
        print()

        # with open(output_dir+file_name[:-4]+'_output.json', 'w') as json_file:
        #     json.dump(result, json_file, indent=4)
                
# def process_comp_vision_instances(instances_dir ='Instances/Images/',output_dir='Results/Images/'):
#     files_names=[]
    
#     if os.path.exists(instances_dir) and os.path.isdir(instances_dir):
#         for item in os.listdir(instances_dir):
#             item_path = os.path.join(instances_dir, item)
#             if os.path.isfile(item_path):
#                 files_names.append(item)
#     else:
#         print(f'O diretório {instances_dir} não existe ou não é um diretório.')

#     for file_name in files_names:
#         sectionalize_image(sources=[0],sinks=[8],fig_name=file_name)