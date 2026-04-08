import math
from .types import Pos2D, Roue, Capteurs
from .cinematique import CinematiqueDeuxRoues
from .geom import normaliser_angle
import time

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

        self.last_step_time = None
        self.last_capteurs_time = None

    def calcul_dt(self, last_time):
        now = time.perf_counter() #on lit l’heure actuelle
        
        if last_time is None: #c’est le tout premier appel, on n’a pas encore d’ancienne heure
            return 0.0, now
        
        dt = now - last_time #on calcule le temps écoulé depuis le dernier appel
        return dt, now # le nouveau temps actuel now qui va remplacer last-time dans robot
