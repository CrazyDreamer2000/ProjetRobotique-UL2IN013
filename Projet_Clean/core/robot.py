import math
from .types import Pos2D, Roue, Capteurs

class Robot:
    """Le "core" du robot"""
    def __init__(self, rayon_roue: float, ecartement_roues: float, ori_initiale=0, x=0.0, y=0.0):
        
        self.rayon_roue = rayon_roue
        self.ecartement_roues = ecartement_roues

        # Position & angle du robot (séparé du core)
        self.pos = Pos2D(x, y, ori_initiale)

        # Etat des roues
        self.roue_gauche = Roue(0.0, 0.0)
        self.roue_droite = Roue(0.0, 0.0)

        self.vitesse_precedante = 0.0
        self.capteurs = Capteurs(accelerometre=0.0, capteur_distance=0.0)

        self.en_collision = False

        self.vitesse_linaire_actuellement = 0