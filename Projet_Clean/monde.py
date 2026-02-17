# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc
import config as cfg
import math

class Obstacle:
    def __init__(self,x,y,largeur,longueur):
        self.x= x # pixels
        self.y= y # pixels
        self.largeur = largeur # mètres
        self.longueur = longueur # mètres


class Monde:
    """Représente l'environnement avec les obstacles"""
    
    def __init__(self):
        self.obstacles = []
    
    def ajouter_obstacle(self, obstacle):
        """Ajoute un obstacle au monde"""
        self.obstacles.append(obstacle)
    
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
        for obs in self.obstacles:
            # Dimensions de l'obstacle en pixels
            obs_L = obs.longueur * cfg.SCALE / 2
            obs_l = obs.largeur * cfg.SCALE / 2
            
            # Collision simple AABB (Axis-Aligned Bounding Box)
            #Avec ça , On vérifie si les rectangles se chevauchent
            if (abs(robot_x_px - obs.x) < robot_L + obs_L and
                abs(robot_y_px - obs.y) < robot_l + obs_l):
                return True  # Collision détectée
        
        return False  # Pas de collision
        
   

    def lire_distance_devant(self, pos_robot, portee_max=2.0):
        """
        Capteur radar ultrasonique analogique
        """
        x_m, y_m = pos_robot.x, pos_robot.y 
        ori = pos_robot.orientation 
        
        # check pour chaque 0.05 metre
        pas = 0.02 
        for d in range(1, int(portee_max / pas)):
            dist_test = d * pas 
            
             # Calculer les coordonnées (en mètres) du point de détection.
            test_x_m = x_m + (dist_test + cfg.ROBOT_LONGUEUR / 2)* math.cos(ori)
            test_y_m = y_m + (dist_test + cfg.ROBOT_LONGUEUR / 2)* math.sin(ori)
            
            # Convertir en coordonnées pixel pour correspondre à la position de l'obstacle
            test_x_px = test_x_m * cfg.SCALE
            test_y_px = test_y_m * cfg.SCALE
            
            for obs in self.obstacles:
                # 
                obs_L = obs.longueur * cfg.SCALE / 2
                obs_l = obs.largeur * cfg.SCALE / 2
                
                # Détection de collision
                if (abs(test_x_px - obs.x) < obs_L and 
                    abs(test_y_px - obs.y) < obs_l):
                    print(dist_test)
                    return dist_test
                    
        return portee_max # Si aucun obstacle n'est détecté, revenir à la pleine échelle.