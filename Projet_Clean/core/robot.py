import math
from .types import Pos2D, CommandeRoues, EtatRoues
from .cinematique import CinematiqueDeuxRoues

class Robot:
    """Le "core" du robot"""
    def __init__(self, rayon_roue_m: float, ecartement_roues_m: float):
        
        # Modèle qui traduit les vitesses des roues en déplacement du robot
        self.modele_mouvement = CinematiqueDeuxRoues(rayon_roue_m, ecartement_roues_m)

        # Position & angle du robot (séparé du core)
        self.pos = Pos2D(0.0, 0.0, 0.0)

        # Commandes envoyées aux roues
        self.commande = CommandeRoues(0.0, 0.0)

        # Etat réel des roues (juste pour avoir code plus réaliste)
        self.roues = EtatRoues(
            vitesse_rotation_gauche=0.0,
            vitesse_rotation_droite=0.0,
            rotation_totale_gauche=0.0,
            rotation_totale_droite=0.0,
        )
        
        # Pour déterminer si le robot est en collision
        self.en_collision = False

    def definir_commande_roues(self, vitesse_rotation_gauche: float, vitesse_rotation_droite: float):
        self.commande = CommandeRoues(vitesse_rotation_gauche, vitesse_rotation_droite)

    def step(self, dt: float, monde=None):
        """
        Avance la simulation de dt secondes
        - met à jour les roues
        - calcule le mouvement
        - met à jour la pos (avec vérification des collisions)
        """

        # Envoyer la commande (vitesse rotation) aux roues
        self.roues.vitesse_rotation_gauche = self.commande.vitesse_rotation_gauche
        self.roues.vitesse_rotation_droite = self.commande.vitesse_rotation_droite

        # Met a jour la rotation totale des roues (on rajoute l'angle obtenu en dt temps)
        self.roues.rotation_totale_gauche += self.roues.vitesse_rotation_gauche * dt
        self.roues.rotation_totale_droite += self.roues.vitesse_rotation_droite * dt

        # Calcul du mouvement du robot
        vitesse_avant, vitesse_rotation = self.modele_mouvement.vitesses_robot_depuis_roues(
            self.roues.vitesse_rotation_gauche,
            self.roues.vitesse_rotation_droite
        )

        # Calculer la nouvelle position
        pos_suiv = self.modele_mouvement.avance_pos(self.pos, vitesse_avant, vitesse_rotation, dt)
        
        # Vérifier les collisions
        if monde is not None and monde.collisions_robot(pos_suiv):
            # Collision détectée: arrêter le robot
            self.definir_commande_roues(0, 0)
            self.en_collision = True
            # La position ne change pas : on garde self.pos
        else:
            # Pas de collision: mettre à jour la position
            self.pos = pos_suiv
            self.en_collision = False

        # Normaliser l'orientation dans [-pi, +pi] 
        self.pos.orientation = (self.pos.orientation + math.pi) % (2 * math.pi) - math.pi
