# controle/traducteur.py

from abc import ABC, abstractmethod # Pour les classes abstraites
from core.robot import Robot
from monde.monde import Monde
from core.geom import normaliser_angle

class Traducteur(ABC):
    """
    Classe abstraite définissant l'interface entre le controlleur et le robot
    """
    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        pass

    def get_distance_devant(self) -> float:
        pass

    def reset_distance_parcourue(self):
        pass

    def get_distance_parcourue(self) -> float:
        pass

    def reset_angle_parcouru(self):
        pass

    def get_angle_parcouru(self) -> float:
        pass

    def est_en_collision(self) -> bool:
        pass

class TraducteurSimu(Traducteur):
    """
    Implémentation du traducteur pour la simulation.
    Fait le lien entre les commandes de l'algo et les objets Robot/Monde.
    """
    def __init__(self, robot: Robot, monde: Monde):
        self.robot = robot
        self.monde = monde

        # Références de départ pour les mesures relatives
        self._distance_depart_gauche = 0.0
        self._distance_depart_droite = 0.0
        self._orientation_depart = robot.pos.orientation

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
        self.robot.definir_commande_roues(v_gauche, v_droite)

    # DISTANCE PARCOURUE

    def reset_distance_parcourue(self):
        self._distance_depart_gauche = self.robot.roues.rotation_totale_gauche
        self._distance_depart_droite = self.robot.roues.rotation_totale_droite

    def get_distance_parcourue(self) -> float:
        rayon = self.monde.cinematique.rayon_roue

        delta_gauche = self.robot.roues.rotation_totale_gauche - self._distance_depart_gauche
        delta_droite = self.robot.roues.rotation_totale_droite - self._distance_depart_droite

        distance_gauche = delta_gauche * rayon
        distance_droite = delta_droite * rayon

        return (distance_gauche + distance_droite) / 2

    def reset_angle_parcouru(self):
        self._orientation_depart = self.robot.pos.orientation

    def get_angle_parcouru(self) -> float:
        return normaliser_angle(self.robot.pos.orientation - self._orientation_depart)

    # CAPTEURS / ETAT

    def get_distance_devant(self) -> float:
        """
        Sortie:
            - monde.lire_distance_devant(robot.pos) : float
              Valeur du capteur de distance (distance en mètres : 2m max)
        """
        # Utilise le monde pour calculer de distance
        return self.monde.lire_distance_devant(self.robot.pos)
    
    def est_en_collision(self) -> bool:
        """
        Renvoie True si le robot simulé est en collision, False sinon
        """
        return self.robot.en_collision
