# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc
from dataclasses import dataclass
import config as cfg

@dataclass
class Obstacle:
    x: float # mètres
    y: float # mètres
    largeur: float # mètres
    longueur: float # mètres


class Monde:
    """Représente l'environnement avec les obstacles"""
    
    def __init__(self):
        self.liste_obstacles = []
    
    def ajouter_obstacle(self, x, y):
        """Ajoute un obstacle au monde"""
        self.liste_obstacles.append(Obstacle(x/cfg.SCALE, y/cfg.SCALE, cfg.TAILLE_OBSTACLE, cfg.TAILLE_OBSTACLE))
    
    def collisions_robot(self, pos_robot):
        """
        La fonction vérifie s'il y a collision entre le robot et les obstacles
        """
        # Position du robot en pixels
        robot_x_px = pos_robot.x * cfg.SCALE
        robot_y_px = pos_robot.y * cfg.SCALE
        
        # Dimensions du robot en pixels
        robot_L = cfg.ROBOT_LONGUEUR * cfg.SCALE / 2
        robot_l = cfg.ROBOT_LARGEUR * cfg.SCALE / 2
        
        # Pour chaque obstacle
        for obs in self.liste_obstacles:
            # Dimensions de l'obstacle en pixels
            obs_L = obs.longueur * cfg.SCALE / 2
            obs_l = obs.largeur * cfg.SCALE / 2
            
            # Collision simple AABB (Axis-Aligned Bounding Box)
            #Avec ça , On vérifie si les rectangles se chevauchent
            if (abs(robot_x_px - obs.x) < robot_L + obs_L and
                abs(robot_y_px - obs.y) < robot_l + obs_l):
                return True  # Collision détectée
        
        return False  # Pas de collision
        
