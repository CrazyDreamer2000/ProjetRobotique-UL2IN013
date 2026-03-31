import math
import time
from core.geom import normaliser_angle

class Adaptateur:
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
        pass

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
    