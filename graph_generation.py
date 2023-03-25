import networkx as nx
import matplotlib.pyplot as plt
import pygame
import pandas

def Generate_graph (num_players, difficulty):
    density = (1-difficulty/4)/4.5
    rng_graph = nx.fast_gnp_random_graph(10*num_players, density)
    #print(rng_graph) number of nodes and edges
    nodes = rng_graph.number_of_nodes()
    if (not nx.is_connected(rng_graph)):
        components = nx.connected_components(rng_graph)
        First = True
        for c in components:
            #print(c)
            if First:
                f = list(c)[0]
                First = False
            else:
                s = list(c)[0]
                nx.add_path(rng_graph,[f,s])
        #print('Sus')
    #Tenemos un grafo conexo
    #Escogemos dos puntos lo mas alejados posibles
    path = list(nx.shortest_path(rng_graph, 0))
    distance = max(path)
    start_node_1 = path.index(distance)
    path = list(nx.shortest_path(rng_graph, start_node_1))

    distance = max(path)
    start_node_2 = path.index(distance)
    start_nodes = [start_node_1, start_node_2]
    #nt.generic_graph_view(rng_graph)
    #nx.draw(rng_graph)
    pos = nx.spring_layout(rng_graph)
    plt.show()
    return list(nx.generate_edgelist(rng_graph)), nodes, start_nodes, pos

#Generate_graph(2,1)