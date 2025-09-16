import random

import numpy as np

from Color import Color


class Graph:
    def __init__(self, nb_nodes):
        self.coloring = np.random.randint(1, 4, size=nb_nodes)
        self.structure = np.zeros((nb_nodes, nb_nodes), dtype=bool)

        for row in range(self.structure.shape[0]):
            for column in range(self.structure.shape[0]):
                if row != column and self.coloring[row] != self.coloring[column] and random.randint(1, 2) == 1:
                    self.structure[row][column] = 1
                    self.structure[column][row] = 1

    def print(self):
        print("Matrice d'adjacence :")
        n = self.structure.shape[0]
        print("   ", end="")
        for j in range(n):
            print(f"{j + 1:3}", end="")
        print()

        # Corps du tableau
        for i in range(n):
            print(f"{i + 1:3}", end="")  # index ligne
            for j in range(n):
                if self.structure[i, j] == 1:
                    print("  x", end="")
                else:
                    print("   ", end="")
            print()
        print("\nTableau de coloriage :")
        print(self.coloring)
