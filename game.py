import pygame
import networkx as nx
import numpy as np

# Initialize pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Game")

# Set colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set game variables
NODE_RADIUS = 20
PLAYER_RADIUS = 10
FPS = 30

# Create the graph using networkx
graph = nx.random_geometric_graph(10, 0.5)

# Compute the layout
pos = nx.spring_layout(graph)

# Scale layout to screen dimensions
for node in pos:
    x, y = pos[node]
    x, y = (x+1)/2, (y+1)/2
    x = int(x * (WIDTH - NODE_RADIUS*2) + NODE_RADIUS)
    y = int(y * (HEIGHT - NODE_RADIUS*2) + NODE_RADIUS)
    pos[node] = np.array((x,y))

# Create players
player1 = 0
player2 = len(graph) - 1


def draw_node(pos, color):
    pygame.draw.circle(screen, color, pos, NODE_RADIUS)


def draw_edge(p1, p2):
    pygame.draw.line(screen, BLACK, p1, p2, 2)


def draw_player(pos, color):
    pygame.draw.circle(screen, color, pos, PLAYER_RADIUS)


def draw_graph():
    for edge in graph.edges:
        draw_edge(pos[edge[0]], pos[edge[1]])

    for node in graph.nodes:
        draw_node(pos[node], WHITE)

    draw_player(pos[player1], RED)
    draw_player(pos[player2], BLUE)


def main():
    global player1, player2
    clock = pygame.time.Clock()
    run = True

    player1_turn = True

    while run:
        clock.tick(FPS)
        screen.fill((255, 255, 255))

        draw_graph()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node in graph.nodes:
                    if np.linalg.norm(np.array(pygame.mouse.get_pos()) - np.array(pos[node])) <= NODE_RADIUS:
                        if player1_turn:
                            if node in graph.neighbors(player1):
                                player1 = node
                                player1_turn = not player1_turn
                        else:
                            if node in graph.neighbors(player2):
                                player2 = node
                                player1_turn = not player1_turn

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
