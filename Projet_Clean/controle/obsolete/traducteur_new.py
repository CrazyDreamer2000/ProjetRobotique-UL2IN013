from core.types import Pos2D
from core.robot import Robot
from monde.monde import Monde
import math
from core.geom import normaliser_angle

class Traducteur:
    """
    Interface servant de pont entre les algorithmes de contrôle 
    et le robot (qu'il soit simulé ou réel).
    """

    def __init__(self):
        pass
    
    def set_vitesse(self, v_gauche:float, v_droit:float):
        """Envoie les commandes de vitesse aux roues."""
        pass

    def get_distance_delta(self)-> float:
        """Retourne la distance parcourue (m) depuis le dernier appel."""

        return 0.0
    
    def get_angle_delta(self) -> float:
        """Retourne l'angle tourné (rad) depuis le dernier appel."""
        return 0.0
        pass

    def reset(self):
        """Réinitialise les accumulateurs ou les positions de référence."""
        pass

    def est_en_collision(self) -> bool:
        """Indique si le robot est actuellement en collision."""    
        return  False
    
    def get_distance(self) -> float:
        return 0.0
class TraducteurSimu(Traducteur):
    """
    Adaptateur spécifique pour la simulation.
    Calcule les déplacements (deltas) à partir des coordonnées du monde.
    """
    def __init__(self, robot, monde):
        super().__init__()
        self.robot = robot
        self.monde = monde

        "memoriser les etat precedents pour calcul des deltas"
        self.old_x = robot.pos.x
        self.old_y = robot.pos.y
        self.old_ori = robot.pos.orientation

    def set_vitesse(self, v_gauche, v_droit):
        self.robot.definir_commande_roues(v_gauche, v_droit)

    def get_distance_delta(self) -> float:
        dx = self.robot.pos.x - self.old_x
        dy = self.robot.pos.y - self.old_y
        delta = math.hypot(dx, dy)

        #mise a jour les x et y
        self.old_x = self.robot.pos.x
        self.old_y = self.robot.pos.y
        return delta
    
    def get_angle_delta(self) -> float:
        #calculer le angle 
        delta = normaliser_angle(self.robot.pos.orientation - self.old_ori)
        self.old_ori = self.robot.pos.orientation
        return delta
    
    def est_en_collision(self) -> bool:
        return self.robot.en_collision

    def reset(self):
        
        self.old_ori= self.robot.pos.orientation
        self.old_x = self.robot.pos.x
        self.old_y = self.robot.pos.y
    