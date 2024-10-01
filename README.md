# maxflow_mincut

##Forma das instâncias de grafos

As intâncias de grafos são arquivos .txt bi seguinte padrão:
- linha 1: 'número de vértices do grafo'
- linha 2: 'índice da fonte'
- linha 3: 'índice do sumidouro
As demais linhas são as linhas da matriz de adjacência, com os elementos separados por espaços simples
Inlcluir um documento nessa pasta que siga esse padrão será automaticamente lido caso main.py seja executado.
Não existem validações do formato da entrada, um formato errado pode levar a erros inesperados.

##Objeto Graph()


A definição desse objeto no móduno 'model/graph.py' descreve uma forma padrão para o grafo, com o Algoritmo de Ford-Fuelkerson implementado, entretando por ser muito geral não atende todas as especificidades que um grafo pode ter, como é o caso do objeto ExGraph(), aplicado apenas em ex_implementacao.py para representar o funcionamente do algoritmo em um grafo mais simples, em que é desejado criar imagens da evolução desse grafo.

###ImageGraph
O objeto ImageGraph() em 'model/com_vision.py' é um grafo correspondente a uma imagem que pode ser seccionado a partir de um conjunto de fontes e sumidouros, e não necessariamente de dois pontos únicos. Nesse problema a transformação em grafo é mascarada, pois só é necessário a chamada da função sectionalize_image(sources,sinks,fig_name), como a lista de fontes 'sources' e sumidouros 'sinks', e o nome da imagem 'fig_name', desde que ela esteja salva em 'Instances/Images'.
Embora esse código gere a repsentação do grafo para a imagem, quando o número de vértices é muito grande essa imagem perde o sentido, devido a sobreposição das inúmeras arestas e legendas. Mas para isso existe a reconstrução em imagem do grafo já seccionado.

##Exemplos
Ao final dos documentos que definem os objetos existe um exemplo simples de aplicação


##Model.Read

Criado apenas para automatizar a leitura de instâncias