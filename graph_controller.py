import pygame
import numpy as np
from graph_generation import *

class Player:
    def __init__(self, cur_node, color):
        self.cur_node = cur_node
        self.color = color
    def change_node(self, node):
        self.cur_node = node

class Nodes:
    def __init__(self, pos, adj_list):
        self.pos = pos
        self.color = "Pink"
        self.adj_list = adj_list

    def update_list(self, adj_list):
        self.adj_list = adj_list

    def display(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 15)

    def change_color(self, color, screen):
        self.color = color
        self.display(screen)
        for neigh in self.adj_list:
            pygame.draw.line(screen, 'white', self.pos, neigh.pos)
            neigh.display(screen)
            #print(neigh)


def move_p(Players, id, list_of_nodes, screen):
    while True:
        pygame.display.flip()
        ev = pygame.event.get()
        for event in ev:
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                clicked_nodes = [node for node in list_of_nodes if node in Players[id].cur_node.adj_list and node.color == "Pink" and pygame.Rect.collidepoint(pygame.Rect(node.pos[0]-20,node.pos[1]-20,40,40),pos)]
                if clicked_nodes:
                    Players[id].change_node(clicked_nodes[0])
                    clicked_nodes[0].change_color(Players[id].color, screen)
                    return 1
                    


def play(Players, id, list_of_nodes, screen):
    nodes_left = len(list_of_nodes)
    while (nodes_left):
        id = (id+1)%2
        nodes_left -= move_p(Players, id, list_of_nodes, screen)
        

def create_Nodes(num_nodes, graph, position):
    A = []
    Listas_finales = []
    for i in range(num_nodes):
        graph[i] = graph[i].split()
        u = np.array([1,1])
        position[i] = (position[i]+u)/2
        position[i][0]*=(1080)+50
        position[i][1]*=(720)+50
        Node = Nodes(position[i], graph[i])
        #print(graph[i])
        A.append(Node)
        Listas_finales.append([])

    for j in range(num_nodes):
        B = []
        #print(graph[j])
        x = int(graph[j][0])
        y = int(graph[j][1])
        Listas_finales[x].append(A[y])
        Listas_finales[y].append(A[x])
        
    for i in range(num_nodes):
        A[i].update_list(Listas_finales[i])
    return A


def start_game(num_players = 2, difficulty = 1):
    graph, num_nodes, start_nodes, position = Generate_graph(num_players, difficulty)
    lista_clase = create_Nodes(num_nodes, graph, position)
    pygame.init()
    screen = pygame.display.set_mode((1280, 820))
    Node0 = lista_clase[start_nodes[0]]
    p1 = Player(Node0, 'red')
    p1.cur_node.change_color(p1.color, screen)
    Node1 = lista_clase[start_nodes[1]]
    p2 = Player(Node1, 'blue')
    p2.cur_node.change_color(p2.color, screen)
    Players = [p1, p2]
    play(Players, 0, lista_clase, screen)

    pygame.quit()


start_game()
