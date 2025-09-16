import random
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def shuffle_enum(enum_cls):
        """Retourne une liste des valeurs de l'enum mélangées."""
        valeurs = list(enum_cls)
        random.shuffle(valeurs)
        return valeurs