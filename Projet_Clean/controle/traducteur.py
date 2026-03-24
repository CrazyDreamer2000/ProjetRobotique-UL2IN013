# controle/traducteur.py

from core.types import Pos2D
from core.robot import Robot
from monde.monde import Monde

class Traducteur:
    """
    Classe abstraite définissant l'interface entre l'algorithme et le robot.
    """
    def set_vitesse(self, v_gauche: float, v_droite: float):
        pass

    def get_distance(self) -> float:
        return 0.0

    def get_position(self) -> Pos2D:
        return None

class TraducteurSimu(Traducteur):
    """
    Implémentation du traducteur pour la simulation.
    Fait le lien entre les commandes de l'algo et les objets Robot/Monde.
    """
    def __init__(self, robot: Robot, monde: Monde):
        self.robot = robot
        self.monde = monde

    def set_vitesse(self, v_gauche: float, v_droite: float):
        """
        Paramètres:
            - v_gauche : float
              Vitesse de rotation de la roue gauche (rad/s)
            - v_droite : float
              Vitesse de rotation de la roue droite (rad/s)
        """
        # Envoie directement les commandes au robot simulé
        self.robot.definir_commande_roues(v_gauche, v_droite)

    def get_distance(self) -> float:
        """
        Sortie:
            - monde.lire_distance_devant(robot.pos) : float
              Valeur du capteur de distance (distance en mètres : 2m max)
        """
        # Utilise le monde pour calculer de distance
        return self.monde.lire_distance_devant(self.robot.pos)

    def get_position(self) -> Pos2D:
        """
        Sortie:
            - robot.pos : Pos2D
              Position du robot sous forme de la classe Pos2D
        """
        # Retourne la position réelle du robot dans la simulation
        return self.robot.pos
    
    def est_en_collision(self) -> bool:
        """
        Renvoie True si le robot simulé est en collision, False sinon
        """
        return self.robot.en_collision
    
class TraducteurReel(Traducteur):
    """pour le robot reel""" 
    def __init__(self, robot: Robot, monde: Monde):
        self.robot = robot
        self.monde = monde