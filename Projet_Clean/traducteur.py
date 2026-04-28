# controle/traducteur.py

from abc import ABC, abstractmethod # Pour les classes abstraites
from core.robot import Robot
from monde.monde import Monde
from core.geom import normaliser_angle
import math

class Traducteur(ABC):
    """
    Classe abstraite définissant l'interface entre le controlleur et le robot
    """
    @abstractmethod
    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        pass
    
    @abstractmethod
    def get_distance_devant(self) -> float:
        pass

    @abstractmethod
    def reset_distance_parcourue(self):
        pass

    @abstractmethod
    def get_distance_parcourue(self) -> float:
        pass

    @abstractmethod
    def reset_angle_parcouru(self):
        pass

    @abstractmethod
    def get_angle_parcouru(self) -> float:
        pass

    @abstractmethod
    def est_en_collision(self) -> bool:
        pass
    
    @abstractmethod
    def reset_angle_tete_capteur(self):
        pass   

    @abstractmethod
    def tourner_tete_capteur(self, angle: float):
        pass

    @abstractmethod
    def get_angle_tete_capteur(self) -> float:
        pass

class TraducteurSimu(Traducteur):
    """
    Implémentation du traducteur pour la simulation.
    Fait le lien entre les commandes de l'algo et les objets Robot/Monde.
    """
    def __init__(self, monde: Monde):
        self.monde = monde

        # Références de départ pour les mesures relatives
        self._distance_depart_gauche = 0.0
        self._distance_depart_droite = 0.0
        self._orientation_depart = monde.robot.pos.orientation

    # COMMANDES

    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        """
        Paramètres:
            - v_gauche : float
              Vitesse de rotation de la roue gauche (rad/s)
            - v_droite : float
              Vitesse de rotation de la roue droite (rad/s)
        """
        # Envoie directement les commandes au robot simulé
        self.monde.robot.roue_gauche.vitesse_rotation = v_gauche
        self.monde.robot.roue_droite.vitesse_rotation = v_droite

    # DISTANCE PARCOURUE

    def reset_distance_parcourue(self):
        """ Réinitialise les références de distance pour le calcul de la distance parcourue."""
        self._distance_depart_gauche = self.monde.robot.roue_gauche.rotation_totale
        self._distance_depart_droite = self.monde.robot.roue_gauche.rotation_totale

    def get_distance_parcourue(self) -> float:
        """ Calcule la distance parcourue depuis le dernier reset en utilisant les rotations des roues."""
        rayon = self.monde.cinematique.rayon_roue
        delta_gauche = self.monde.robot.roue_gauche.rotation_totale - self._distance_depart_gauche
        delta_droite = self.monde.robot.roue_gauche.rotation_totale - self._distance_depart_droite

        distance_gauche = delta_gauche * rayon
        distance_droite = delta_droite * rayon

        return abs(distance_gauche + distance_droite) / 2

    def reset_angle_parcouru(self):
        """ Réinitialise la référence d'orientation pour le calcul de l'angle parcouru."""
        self._orientation_depart = self.monde.robot.pos.orientation

    def get_angle_parcouru(self) -> float:
        """ Calcule l'angle parcouru depuis le dernier reset en utilisant l'orientation du robot."""
        return normaliser_angle(self.monde.robot.pos.orientation - self._orientation_depart)

    # CAPTEURS / ETAT

    def get_distance_devant(self) -> float:
        """
        Sortie:
            - monde.lire_distance_devant(robot.pos) : float
              Valeur du capteur de distance (distance en millimètres : (0.5 -> 8000) )
        """
        # Utilise le monde pour calculer de distance
        return self.monde.lire_distance_devant(self.monde.robot.pos)
    
    def est_en_collision(self) -> bool:
        """
        Renvoie True si le robot simulé est en collision, False sinon
        """
        return self.monde.robot.en_collision
    
    def reset_angle_tete_capteur(self):
        """ Réinitialise la tête du capteur à la position centrale (90°).
        0 si tourné complètement à gauche, 180 si tourné complètement à droite.
        """
        pass

    def tourner_tete_capteur(self, angle: float):
        """ Tourne la tête du capteur à l'angle spécifié.
        Paramètre:
            - angle : float, angle de 0 à 180 degrés (90 = milieu)
            0 si tourné complètement à gauche, 180 si tourné complètement à droite.
        """
        pass

    def get_angle_tete_capteur(self) -> float:
        """ Retourne l'angle actuel de la tête du capteur (en degrés)."""
        pass  
    

class TraducteurReel(Traducteur):
    """
    Implémentation du traducteur pour le robot réel.
    Fait le lien entre les commandes de l'algo et les fonctions d'interface du robot réel.
    """
    def __init__(self, robot):
        self.robot = robot

        # Références de départ pour les mesures relatives, 

        self.dist_ref_gauche = 0.0
        self.dist_ref_droite = 0.0  

        self.angle_ref_gauche = 0.0
        self.angle_ref_droite = 0.0
        
        # Compteurs explicites
        self._distance_parcourue_depuis_reset = 0.0
        self._angle_parcouru_depuis_reset = 0.0
        
        # Degré du capteur de distance, default = 90 (milieu), 0 = complètement à gauche, 180 = complètement à droite
        self._angle_capteur = 90

    # COMMANDES

    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        """
        Paramètres:
            - v_gauche : float
              Vitesse de rotation de la roue gauche (rad/s)
            - v_droite : float
              Vitesse de rotation de la roue droite (rad/s)
        """
        # Conversion rad/s → deg/s
        deg_par_rad = 180 / math.pi
        dps_gauche = v_gauche * deg_par_rad
        dps_droite = v_droite * deg_par_rad

        # Application aux moteurs
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps_gauche)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps_droite)

    # DISTANCE PARCOURUE

    def reset_distance_parcourue(self):
        """Réinitialise les références de distance pour le calcul de la distance parcourue."""
        encodeurs = self.robot.get_motor_position()
        self.dist_ref_gauche = encodeurs[0]
        self.dist_ref_droite = encodeurs[1]
        self._distance_parcourue_depuis_reset = 0.0

    def get_distance_parcourue(self) -> float:
        """Calcule la distance parcourue depuis le dernier reset en utilisant les rotations des roues."""
        rayon = self.robot.WHEEL_DIAMETER / 2.0  # mm

        encodeurs = self.robot.get_motor_position()
        delta_gauche_deg = encodeurs[0] - self.dist_ref_gauche
        delta_droite_deg = encodeurs[1] - self.dist_ref_droite

        # Conversion degrés → radians
        delta_gauche_rad = delta_gauche_deg * (math.pi / 180)
        delta_droite_rad = delta_droite_deg * (math.pi / 180)

        distance_gauche = delta_gauche_rad * rayon  # mm
        distance_droite = delta_droite_rad * rayon  # mm
        self._distance_parcourue_depuis_reset = abs(distance_gauche + distance_droite) / 2
        return self._distance_parcourue_depuis_reset

    # ANGLE PARCOURU

    def reset_angle_parcouru(self):
        """Réinitialise la référence d'orientation pour le calcul de l'angle parcouru."""
        encodeurs = self.robot.get_motor_position()
        self.angle_ref_gauche = encodeurs[0]
        self.angle_ref_droite = encodeurs[1]
        self._angle_parcouru_depuis_reset = 0.0

    def get_angle_parcouru(self) -> float:
        """Calcule l'angle parcouru depuis le dernier reset en utilisant les encodeurs."""
        encodeurs = self.robot.get_motor_position()
        delta_gauche_deg = encodeurs[0] - self.angle_ref_gauche
        delta_droite_deg = encodeurs[1] - self.angle_ref_droite

        rayon = self.robot.WHEEL_DIAMETER / 2.0  # mm
        dist_entre_roues = self.robot.WHEEL_BASE_WIDTH  # mm

        # Formule de l'angle parcouru (en radians)
        angle_rad = (delta_droite_deg - delta_gauche_deg) * (rayon / dist_entre_roues) * (math.pi / 180)
        self._angle_parcouru_depuis_reset = angle_rad
        return self._angle_parcouru_depuis_reset

    # CAPTEURS / ETAT

    def get_distance_devant(self) -> float:
        """
        Sortie:
            - float : distance en millimètres (Intervalle du capteur: 5 → 8000 mm)
        """
        distance = self.robot.get_distance()
        if distance == 8190:  # Valeur spéciale indiquant que le capteur n'a rien détecté (au-delà de sa portée maximale, 5 - 8000mm)
            return 8000.0  # On considère qu'il n'y a rien
        return float(distance)

    def est_en_collision(self) -> bool:
        """
        Renvoie True si le robot est en collision, False sinon.
        Seuil à 200 mm (20 cm).
        """
        SEUIL_COLLISION = 200.0  # mm
        return self.get_distance_devant() < SEUIL_COLLISION


    def reset_angle_tete_capteur(self):
        """Réinitialise la tête du capteur à la position centrale (90°).
        0 si tourné complètement à gauche, 180 si tourné complètement à droite.
        """
        self._angle_capteur = 90
        self.robot.servo_rotate(self._angle_capteur)

    def tourner_tete_capteur(self, angle: float):
        """
        Tourne la tête du capteur à l'angle spécifié.
        Paramètre:
            - angle : float, angle de 0 à 180 degrés (90 = milieu)
            0 si tourné complètement à gauche, 180 si tourné complètement à droite.
        """
        if angle >= 0 and angle <= 180:
            self._angle_capteur = angle
            self.robot.servo_rotate(self._angle_capteur)
        else:
            print("Angle de tête de capteur invalide : doit être entre 0 et 180 degrés.")

    def get_angle_tete_capteur(self) -> float:
        """
        Retourne l'angle actuel de la tête du capteur (en degrés).
        """
        return self._angle_capteur
    
