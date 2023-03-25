import pygame
import networkx as nx
import numpy as np
from multiprocessing import Process
import socket
import time

# Initialize pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 500, 500
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set captions for the screens
# pygame.display.set_caption("Graph game")

# Set colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set game variables
NODE_RADIUS = 20
PLAYER_RADIUS = 10
FPS = 30


def create_graph():
    # Create the graph using networkx
    graph = nx.random_geometric_graph(10, 0.5)

    # Compute the layout
    pos = nx.spring_layout(graph)

    # Scale layout to screen dimensions
    minx, miny = pos[0]
    maxx, maxy = pos[0]
    for node in pos:
        minx = min(minx, pos[node][0])
        maxx = max(maxx, pos[node][0])
        miny = min(miny, pos[node][1])
        maxy = max(maxy, pos[node][1])
    for node in pos:
        x, y = pos[node]
        x, y = (x - minx) / (maxx - minx), (y - miny) / (maxy - miny)
        x = int(x * (WIDTH - NODE_RADIUS*2) + NODE_RADIUS)
        y = int(y * (HEIGHT - NODE_RADIUS*2) + NODE_RADIUS)
        pos[node] = np.array((x,y))

    distances = nx.shortest_path_length(graph)
    farthest_nodes = None
    max_distance = -1
    for node, node_distances in distances:
        node_max_distance = max(node_distances.values())
        if node_max_distance > max_distance:
            max_distance = node_max_distance
            farthest_nodes = node, max(node_distances, key=node_distances.get)

    # Create players
    player1, player2 = farthest_nodes
    return graph, pos, player1, player2


def draw_node(screen, pos, color):
    pygame.draw.circle(screen, color, pos, NODE_RADIUS)


def draw_edge(screen, p1, p2):
    pygame.draw.line(screen, BLACK, p1, p2, 2)


def draw_player(screen, pos, color):
    pygame.draw.circle(screen, color, pos, PLAYER_RADIUS)


def draw_graph(screen, player, other_player, player_color, other_player_color, graph, pos):
    visible_nodes = list(graph.neighbors(player)) + [player]
    for node in visible_nodes:
        if node == player:
            color = player_color
        elif node == other_player:
            color = other_player_color
        else:
            color = BLACK
        draw_node(screen, pos[node], color)

        for neighbor in graph.neighbors(node):
            if neighbor in visible_nodes:
                draw_edge(screen, pos[node], pos[neighbor])


def player_screen(player_num, player, other_player, player_color, other_player_color, graph, pos):

    this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if player_num == 1:
        this_socket.bind(('127.0.0.1', 40002))
        this_socket.listen()
        other_socket, _ = this_socket.accept()
    else:
        this_socket.connect(('127.0.0.1', 40002))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Player {player_num}'s Screen")

    clock = pygame.time.Clock()
    run = True

    while run:
        if player_num == 1:
            other_socket.send(str(player).encode())
            other_player = int(other_socket.recv(1024).decode())
        else:
            other_player = int(this_socket.recv(1024).decode())
            this_socket.send(str(player).encode())

        clock.tick(FPS)
        screen.fill(WHITE)
        draw_graph(screen, player, other_player, player_color, other_player_color, graph, pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node in graph.nodes:
                    if np.linalg.norm(np.array(pygame.mouse.get_pos()) - np.array(pos[node])) <= NODE_RADIUS:
                        if node in graph.neighbors(player):
                            player = node

        pygame.display.update()

    this_socket.close()
    if player_num == 1:
        other_socket.close()

    pygame.quit()


def main():
    graph, pos, player1, player2 = create_graph()

    player1_thread = Process(target=player_screen, args=(1, player1, player2, RED, BLUE, graph, pos))
    player2_thread = Process(target=player_screen, args=(2, player2, player1, BLUE, RED, graph, pos))

    player1_thread.start()
    time.sleep(1)
    player2_thread.start()

    player1_thread.join()
    player2_thread.join()


# def main():
#     global player1, player2
#     clock = pygame.time.Clock()
#     run = True

#     player1_turn = True

#     while run:
#         if player1 == player2:
#             print('You winned')
#             run = False
#         clock.tick(FPS)
        
#         screen.fill(WHITE)

#         draw_graph(screen, player1, player2, RED, BLUE)
#         draw_graph(screen, player2, player1, BLUE, RED)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 for node in graph.nodes:
#                     if np.linalg.norm(np.array(pygame.mouse.get_pos()) - np.array(pos[node])) <= NODE_RADIUS:
#                         if player1_turn:
#                             if node in graph.neighbors(player1):
#                                 player1 = node
#                                 player1_turn = not player1_turn
#                         else:
#                             if node in graph.neighbors(player2):
#                                 player2 = node
#                                 player1_turn = not player1_turn

#         pygame.display.update()

#     pygame.quit()


if __name__ == "__main__":
    main()
