# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc
from dataclasses import dataclass
import config as cfg
import math

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
        # On travaille tout en MÈTRES pour éviter les erreurs d'unités
        rx, ry, theta = pos_robot.x, pos_robot.y, pos_robot.orientation
        
        # Demi-dimensions du robot
        rw = cfg.ROBOT_LONGUEUR / 2
        rh = cfg.ROBOT_LARGEUR / 2
        
        # Calcul des 4 coins du robot en fonction de son orientation (formule de rotation)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        
        # Liste des décalages des 4 coins par rapport au centre du robot
        # (Largeur/2, Longueur/2)
        offsets = [(rw, rh), (rw, -rh), (-rw, rh), (-rw, -rh)]
        
        robot_coins = []
        for dx, dy in offsets:
            # Application de la matrice de rotation 2D : x' = x*cos(t) - y*sin(t)
            cx = rx + dx * cos_t - dy * sin_t 
            cy = ry + dx * sin_t + dy * cos_t
            robot_coins.append((cx, cy))
            
        for obs in self.liste_obstacles:
            # 1. Vérifie si un des coins du ROBOT est à l'intérieur de l'OBSTACLE
            for cx, cy in robot_coins:
                if (obs.x - obs.longueur/2 <= cx <= obs.x + obs.longueur/2 and 
                    obs.y - obs.largeur/2 <= cy <= obs.y + obs.largeur/2):
                    return True  # Collision détectée
            
            # 2. Vérifie si un des coins de l'OBSTACLE est à l'intérieur du ROBOT
            # (Nécessaire si l'obstacle est petit ou tape le milieu du robot)
            obs_coins = [
                (obs.x - obs.longueur/2, obs.y - obs.largeur/2),
                (obs.x + obs.longueur/2, obs.y - obs.largeur/2),
                (obs.x + obs.longueur/2, obs.y + obs.largeur/2),
                (obs.x - obs.longueur/2, obs.y + obs.largeur/2)
            ]
            
            for ox, oy in obs_coins:
                # On transforme le point de l'obstacle dans le repère local du robot
                dx = ox - rx
                dy = oy - ry
                # Rotation inverse (-theta) pour aligner avec le robot
                local_x = dx * cos_t + dy * sin_t
                local_y = -dx * sin_t + dy * cos_t
                
                # Vérification simple AABB dans le repère du robot
                if -rw <= local_x <= rw and -rh <= local_y <= rh:
                    return True
        
        return False  # Pas de collision
        
