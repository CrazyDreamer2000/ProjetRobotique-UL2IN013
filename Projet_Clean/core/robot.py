import math
from .types import Pos2D, Roue, Capteurs

class Robot:
    """Le "core" du robot"""
    def __init__(self, rayon_roue_m: float, ecartement_roues_m: float, ori_initiale=0, x=0.0, y=0.0):
        
        self.rayon_roue_m = rayon_roue_m
        self.ecartement_roues_m = ecartement_roues_m

        # Position & angle du robot (séparé du core)
        self.pos = Pos2D(x, y, ori_initiale)

        # Etat des roues
        self.roue_gauche = Roue(0.0, 0.0)
        self.roue_droite = Roue(0.0, 0.0)

        self.vitesse_precedante = 0.0
        self.capteurs = Capteurs(accelerometre=0.0, capteur_distance=0.0)

        self.en_collision = False

        self.vitesse_linaire_actuellement = 0