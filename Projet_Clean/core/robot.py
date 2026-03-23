import math
from .types import Pos2D, CommandeRoues, EtatRoues, Capteurs
from .cinematique import CinematiqueDeuxRoues
from .geom import normaliser_angle


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
    
    def maj_capteurs(self, dt, monde, vitesse_actuelle):
        """Mettre à jour l'état du capteur du robot"""

        "(a = Δv / Δt)"

        accel = 0.0 # Initialiser l'accélération
        if dt > 0:
           accel = (vitesse_actuelle - self.vitesse_precedante) / dt
        self.vitesse_precedante = vitesse_actuelle

        self.dist_obstacle = monde.lire_distance_devant(self.pos)
        dist = self.dist_obstacle
        print(dist)  #pour tester
        self.capteurs.accelerometre = accel
        self.capteurs.capteur_distance = dist

    def definir_commande_roues(self, vitesse_rotation_gauche: float, vitesse_rotation_droite: float):
        self.commande = CommandeRoues(vitesse_rotation_gauche, vitesse_rotation_droite)

    def step(self, dt: float, monde):
        """
        Avance la simulation de dt secondes
        - met à jour les roues
        - calcule le mouvement
        - met à jour la pos (avec vérification des collisions)
        - gère la reculade après collision
        
        Paramètres:
            dt: Temps écoulé en secondes
            monde: Instance de Monde pour vérifier les collisions
        """

        if dt<0:
            return

        # Application de la commande
        self.roues.vitesse_rotation_gauche = self.commande.vitesse_rotation_gauche
        self.roues.vitesse_rotation_droite = self.commande.vitesse_rotation_droite

        # Mise a jour de l'etat des roues
        self.roues.rotation_totale_gauche += self.roues.vitesse_rotation_gauche * dt
        self.roues.rotation_totale_droite += self.roues.vitesse_rotation_droite * dt

        # Calcul de la nouvelle position possible
        vitesse_avant, vitesse_rotation = self.modele_mouvement.vitesses_robot_depuis_roues(
            self.roues.vitesse_rotation_gauche,
            self.roues.vitesse_rotation_droite
        )
        pos_suiv = self.modele_mouvement.avance_pos(self.pos, vitesse_avant, vitesse_rotation, dt)
        
        self.en_collision = monde.collision(pos_suiv)
        if not self.en_collision:
            self.pos = pos_suiv

        # Normaliser l'orientation dans [-pi, +pi] 
        self.pos.orientation = normaliser_angle(self.pos.orientation
                                                )

        self.vitesse_linaire_actuellement = vitesse_avant # utiliser le v pour calculer acceleration


        print(self.en_collision)