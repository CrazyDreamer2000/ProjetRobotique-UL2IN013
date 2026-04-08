import math
from .types import Pos2D, CommandeRoues, EtatRoues, Capteurs
from .cinematique import CinematiqueDeuxRoues
from .geom import normaliser_angle
import time

ORIENTATIONS = {
                "droite" : 0,
                "haut" : math.pi / 2,
                "gauche" : math.pi,
                "bas" : -math.pi / 2
             }

class Robot:
    """Le "core" du robot"""
    def __init__(self, rayon_roue_m: float, ecartement_roues_m: float, ori_initiale="droite", x=0.0, y=0.0):
        
        # Modèle qui traduit les vitesses des roues en déplacement du robot
        self.modele_mouvement = CinematiqueDeuxRoues(rayon_roue_m, ecartement_roues_m)

        # Position & angle du robot (séparé du core)
        self.pos = Pos2D(x, y, ORIENTATIONS[ori_initiale])

        # Commandes envoyées aux roues
        self.commande = CommandeRoues(0.0, 0.0)

        # Etat réel des roues (juste pour avoir code plus réaliste)
        self.roues = EtatRoues(
            vitesse_rotation_gauche=0.0,
            vitesse_rotation_droite=0.0,
            rotation_totale_gauche=0.0,
            rotation_totale_droite=0.0,
        )

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


    def definir_commande_roues(self, vitesse_rotation_gauche: float, vitesse_rotation_droite: float):
        #print('vitesse envoyée: ',vitesse_rotation_gauche, vitesse_rotation_droite)
        self.commande = CommandeRoues(vitesse_rotation_gauche, vitesse_rotation_droite)
