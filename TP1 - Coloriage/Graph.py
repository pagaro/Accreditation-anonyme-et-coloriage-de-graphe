import random
import numpy as np

class Graph:
    def __init__(self, nb_nodes):
        # tirer une couleur au hasard pour chaque noeud entre "rouge", "vert" et "bleu"
        self.coloring = np.random.randint(1, 4, size=nb_nodes) # 1 = rouge, 2 = vert, 3 = bleu

        self.structure = np.zeros((nb_nodes, nb_nodes), dtype=bool)

        # générer la matrice d’adjacence d’un graphe qui contient seulement des arêtes reliant des noeuds comportant des couleurs différentes
        for row in range(nb_nodes):
            for column in range(row + 1, nb_nodes):
                if self.coloring[row] != self.coloring[column] and random.random() < 0.5:
                    self.structure[row][column] = 1 
                    self.structure[column][row] = 1 # la matrice est symétrique donc on peut remplir les deux cases

    def print(self):
        print("Matrice d'adjacence :")
        n = self.structure.shape[0]
        print("   ", end="")
        for j in range(n):
            print(f"{j + 1:3}", end="")
        print()

        for i in range(n):
            print(f"{i + 1:3}", end="")
            for j in range(n):
                if self.structure[i, j] == 1:
                    print("  x", end="")
                else:
                    print("   ", end="")
            print()
        print("\nTableau de coloriage :")
        print(self.coloring)
