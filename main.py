import random

from Color import Color
from Graph import Graph

COLORS = [Color.RED, Color.BLUE, Color.GREEN]

def generate_graph_3_colorable(nb_nodes)-> Graph:
    gr = Graph(nb_nodes)
    gr.print()
    return gr

def commitment_coloring():
    random_colors = COLORS
    random.shuffle(random_colors)
    print(random_colors)

generate_graph_3_colorable(5)
commitment_coloring()
