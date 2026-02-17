import math
from .types import Pos2D, CommandeRoues, EtatRoues, Capteurs
from .cinematique import CinematiqueDeuxRoues

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
        
        # Flag pour déterminer si le robot est en collision
        self.en_collision = False
        
        # Timer pour la reculade après collision
        self.temps_reculade = 0.0  # Durée restante de reculade (en secondes)
        self.temps_rotation = 0.0  # Durée restante de rotation d'évitement
        
        self.TEMPS_RECULADE = 1.0  # Durée de reculade (augmentée pour bien dégager)
        self.TEMPS_ROTATION = 1.05  # Durée de rotation (1.05s * 3.0rad/s ~= 180 deg)
        self.VITESSE_RECULADE = -4.0  # Vitesse de roues en arrière (plus rapide)
        self.VITESSE_ROTATION_EVITEMENT = 3.0 # Vitesse pour tourner après le choc

        self.capteurs = Capteurs(accelerometre=0.0, capteur_distance=0.0)
        self.vitesse_precedante = 0.0  #pour calculer le acceleration

    
    def maj_capteurs(self, dt, monde, vitesse_actuelle):
        """renouvMettre à jour l'état du capteur du robot"""

        "(a = Δv / Δt)"

        accel = 0.0 # Initialiser l'accélération
        if dt > 0:
           accel = (vitesse_actuelle - self.vitesse_precedante) / dt
        self.vitesse_precedante = vitesse_actuelle

        dist = 2.0 #Initialiser la distance

        if monde is not None:
            self.dist_obstacle = monde.lire_distance_devant(self.pos)
        
        self.capteurs.accelerometre = accel
        self.capteurs.capteur_distance = dist

    


    def definir_commande_roues(self, vitesse_rotation_gauche: float, vitesse_rotation_droite: float):
        self.commande = CommandeRoues(vitesse_rotation_gauche, vitesse_rotation_droite)

    def step(self, dt: float, monde=None):
        """
        Avance la simulation de dt secondes
        - met à jour les roues
        - calcule le mouvement
        - met à jour la pos (avec vérification des collisions)
        - gère la reculade après collision
        
        Paramètres:
            dt: Temps écoulé en secondes
            monde: Instance de Monde pour vérifier les collisions (optionnel)
        """

        # 1. Gestion des commandes (Priorité : Reculade -> Rotation -> Algorithme)
        # On utilise une structure if/elif pour prioriser l'évitement d'obstacle
        if self.temps_reculade > 0:
            # Phase 1 : Reculade (Le robot recule pour se dégager du mur)
            self.roues.vitesse_rotation_gauche = self.VITESSE_RECULADE
            self.roues.vitesse_rotation_droite = self.VITESSE_RECULADE
            self.temps_reculade -= dt
            
            # Une fois la reculade terminée, on passe à la phase de rotation
            if self.temps_reculade <= 0:
                self.temps_rotation = self.TEMPS_ROTATION

        elif self.temps_rotation > 0:
            # Phase 2 : Rotation (Le robot tourne sur place pour changer de direction)
            self.roues.vitesse_rotation_gauche = -self.VITESSE_ROTATION_EVITEMENT
            self.roues.vitesse_rotation_droite = self.VITESSE_ROTATION_EVITEMENT
            self.temps_rotation -= dt
            
        else:
            # Phase 3 : Normal (Le robot suit l'algorithme principal, ex: Carré)
            self.en_collision = False # On libère le flag seulement ici
            self.roues.vitesse_rotation_gauche = self.commande.vitesse_rotation_gauche
            self.roues.vitesse_rotation_droite = self.commande.vitesse_rotation_droite

        # 2. Mise à jour de l'état des roues
        self.roues.rotation_totale_gauche += self.roues.vitesse_rotation_gauche * dt
        self.roues.rotation_totale_droite += self.roues.vitesse_rotation_droite * dt

        # 3. Calcul de la nouvelle position théorique
        vitesse_avant, vitesse_rotation = self.modele_mouvement.vitesses_robot_depuis_roues(
            self.roues.vitesse_rotation_gauche,
            self.roues.vitesse_rotation_droite
        )
        pos_suiv = self.modele_mouvement.avance_pos(self.pos, vitesse_avant, vitesse_rotation, dt)
        
        # 4. Application du mouvement avec sécurité
        # On vérifie la collision AVANT d'appliquer la position, même si on recule
        if monde is not None and monde.collisions_robot(pos_suiv):
            # Collision ! On ne bouge pas (on garde self.pos actuel)
            self.en_collision = True
            # On déclenche la séquence d'évitement (Reculade puis Rotation)
            self.temps_reculade = self.TEMPS_RECULADE
            self.temps_rotation = 0.0 # Reset de la rotation pour forcer la reculade d'abord
        else:
            # Voie libre : on applique la nouvelle position
            self.pos = pos_suiv

        # Normaliser l'orientation dans [-pi, +pi] 
        self.pos.orientation = (self.pos.orientation + math.pi) % (2 * math.pi) - math.pi

        return vitesse_avant # utiliser le v pour calculer acceleration