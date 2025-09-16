import hashlib
import random
import secrets

from Color import Color
from Graph import Graph

COLORS = [Color.RED, Color.BLUE, Color.GREEN]

# *********************************************************
# ********* 1 - Génération du graphe et du coloriage *********
# *********************************************************

def generate_graph_3_colorable(nb_nodes)-> Graph:
    gr = Graph(nb_nodes)
    gr.print()
    return gr

gr = generate_graph_3_colorable(20) # graphe de 20 noeuds

# ***********************************************
# ********* 2 - Mise en gage des couleurs *********
# ***********************************************

def get_permuted_colors():
    random_colors = COLORS
    random.shuffle(random_colors)
    return random_colors

def commitment_coloring(colors, random_values):
    commitments = []
    for c, r in zip(colors, random_values):
        r_bytes = r.to_bytes(16, "big") # 128 bits = 16 octets
        c_bytes = c.name.encode() # sérialisation de la couleur
        y = hashlib.sha1(r_bytes + c_bytes).hexdigest()
        commitments.append(y)

    return commitments

# Applique une permutation à la palette et associe-la au coloriage du graphe
palette = get_permuted_colors()
colors = [palette[c - 1] for c in gr.coloring]  # -1 car gr.coloring contient 1,2,3
random_values = [secrets.randbits(128) for _ in range(20)] # génère 20 valeurs de 128 bits
commitments = commitment_coloring(colors, random_values)

# print("Engagements :", commitments)

# ******************************************************************************
# ********* 3 - Preuve de connaissance à divulgation nulle d’un 3-coloriage *********
# ******************************************************************************

def proof_coloring(graph, commitments, i, j, colors, random_values):

    # Vérifier que i et j sont reliés par une arête
    if not graph.structure[i][j]:
        return False

    # Récupérer les valeurs pour i et j
    r_i, c_i = random_values[i], colors[i]
    r_j, c_j = random_values[j], colors[j]

    # Recalculer les engagements
    r_i_bytes = r_i.to_bytes(16, "big")
    r_j_bytes = r_j.to_bytes(16, "big")
    c_i_bytes = c_i.name.encode()
    c_j_bytes = c_j.name.encode()

    y_i = hashlib.sha1(r_i_bytes + c_i_bytes).hexdigest()
    y_j = hashlib.sha1(r_j_bytes + c_j_bytes).hexdigest()

    # Vérification des conditions
    if y_i != commitments[i]:
        return False
    if y_j != commitments[j]:
        return False
    if c_i == c_j:  # les couleurs doivent être différentes
        return False

    return True

def run_protocol(graph, commitments, colors, random_values, rounds=400):
    n = graph.structure.shape[0]
    edges = [(i, j) for i in range(n) for j in range(i+1, n) if graph.structure[i][j]]

    if not edges:
        raise ValueError("Le graphe n'a pas d'arêtes, impossible d'exécuter le protocole.")

    for _ in range(rounds):
        # Choisir une arête (i, j) au hasard
        i, j = random.choice(edges)

        # Vérifier la preuve pour cette arête
        if not proof_coloring(graph, commitments, i, j, colors, random_values):
            return False  # une seule erreur => échec

    return True  # toutes les preuves réussies

authenticated = run_protocol(gr, commitments, colors, random_values, rounds=400)
print("Authentification réussie ?" , authenticated)
