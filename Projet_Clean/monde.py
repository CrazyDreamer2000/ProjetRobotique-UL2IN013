# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc
from dataclasses import dataclass
import config as cfg
import math
import random  # Pour générer des positions aléatoires

@dataclass
class Obstacle:
    """
    Classe qui représente un obstacle rectangulaire
    """
    x: float # Position X en mètres
    y: float # Position Y en mètres
    largeur: float # Largeur en mètres
    longueur: float # Longueur en mètres
    orientation: float # Angle de rotation en radians (0 = horizontal)


class Monde:
    """Représente l'environnement avec les obstacles"""
    
    def __init__(self):
        self.liste_obstacles = []
        # Créer des obstacles aléatoires dès le départ
        self.creer_obstacles_aleatoires()
    
    def creer_obstacles_aleatoires(self):
        """
        Creation de 5 obstacles dans le monde
        """
        # ici 5 zones (4 coins + 1 bord) 
        zones = [
            # (x_min, x_max, y_min, y_max, nom)
            (0.5, 1.5, 0.5, 1.0, "Coin bas-gauche"),      # Zone 1
            (3.0, 4.0, 0.5, 1.0, "Coin bas-droite"),      # Zone 2  
            (0.5, 1.5, 2.0, 2.5, "Coin haut-gauche"),     # Zone 3
            (3.0, 4.0, 2.0, 2.5, "Coin haut-droite"),     # Zone 4
            (2.0, 2.5, 0.3, 0.7, "Bord bas-centre")       # Zone 5
        ]
        
        # un obstacle à la fois
        for i, (x_min, x_max, y_min, y_max, nom) in enumerate(zones):
            
            # Position aléatoire DANS la zone
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            
            # Orientation aléatoire (0 à 360°)
            orientation = random.uniform(0, 2 * math.pi)
            
            # Dimensions aléatoires
            longueur = random.uniform(0.3, 0.6)  # 30-60 cm
            largeur = random.uniform(0.15, 0.25) # 15-25 cm
            
            # Créer l'obstacle
            obstacle = Obstacle(x, y, largeur, longueur, orientation)
            self.liste_obstacles.append(obstacle)
            
            print(f"✅ Obstacle {i+1} : {nom} ({x:.2f}, {y:.2f}) angle={math.degrees(orientation):.0f}°")
    
    def ajouter_obstacle(self, x, y):
        """Ajoute un obstacle au monde (quand on clique avec la souris)"""
        self.liste_obstacles.append(Obstacle(
            x/cfg.SCALE, 
            y/cfg.SCALE, 
            cfg.TAILLE_OBSTACLE, 
            cfg.TAILLE_OBSTACLE,
            orientation=0.0  # Pas d'orientation pour les obstacles ajoutés manuellement
        ))
    
    def collision(self, pos_robot):
        """
        Detecte collision du robot avec :
        - obstacles
        - bordures du monde
        """

        rx, ry, theta = pos_robot.x, pos_robot.y, pos_robot.orientation

        demi_longueur = cfg.ROBOT_LONGUEUR / 2
        demi_largeur = cfg.ROBOT_LARGEUR / 2

        cos_robot = math.cos(theta)
        sin_robot = math.sin(theta)

        # Calcul des 4 coins du robot
        coins_robot = []

        for dx, dy in [
            ( demi_longueur,  demi_largeur),
            ( demi_longueur, -demi_largeur),
            (-demi_longueur,  demi_largeur),
            (-demi_longueur, -demi_largeur),
        ]:
            coin_x = rx + dx * cos_robot - dy * sin_robot
            coin_y = ry + dx * sin_robot + dy * cos_robot
            coins_robot.append((coin_x, coin_y))

        # Collision avec bordures
        for coin_x, coin_y in coins_robot:
            if (coin_x < 0 or coin_x > cfg.LONGUEUR_MONDE or
                coin_y < 0 or coin_y > cfg.LARGEUR_MONDE):
                return True

        # Collision avec obstacles
        for obs in self.liste_obstacles:

            cos_obs = math.cos(obs.orientation)
            sin_obs = math.sin(obs.orientation)

            for coin_x, coin_y in coins_robot:

                dx = coin_x - obs.x
                dy = coin_y - obs.y

                # transformation dans le repère obstacle
                local_x = dx * cos_obs + dy * sin_obs
                local_y = -dx * sin_obs + dy * cos_obs

                if (abs(local_x) <= obs.longueur / 2 and
                    abs(local_y) <= obs.largeur / 2):
                    return True

        return False
  
    def lire_distance_devant(self, pos_robot, portee_max=2.0):
        """
        Mesure la distance jusqu'au premier obstacle devant le robot
        
        MÉTHODE : On teste des points tous les 2cm devant le robot
        """
        x, y = pos_robot.x, pos_robot.y
        angle = pos_robot.orientation
        
        # Tester tous les 2cm
        for distance in range(1, int(portee_max / 0.02)):
            d = distance * 0.02  # Distance actuelle
            
            # Position du point de test
            test_x = x + d * math.cos(angle)
            test_y = y + d * math.sin(angle)
            
            # Vérifier si ce point touche un obstacle
            for obs in self.liste_obstacles:
                # Transformer dans le repère de l'obstacle
                dx = test_x - obs.x
                dy = test_y - obs.y
                
                cos_obs = math.cos(obs.orientation)
                sin_obs = math.sin(obs.orientation)
                
                local_x = dx * cos_obs + dy * sin_obs
                local_y = -dx * sin_obs + dy * cos_obs
                
                # Point dans l'obstacle ?
                if (abs(local_x) < obs.longueur/2 and 
                    abs(local_y) < obs.largeur/2):
                    return d  # Retourner la distance
        
        return portee_max  # Rien trouvé

    
    def arreter_avant_obstacle(self, pos_robot, distance_securite=0.3):
        """
        Vérifie si le robot doit s'arrêter avant un obstacle

        """
        distance_devant = self.lire_distance_devant(pos_robot, portee_max=2.0)
        
        # Arrêter si la distance jusqu'à l'obstacle est inférieure à la distance de sécurité
        if distance_devant <= distance_securite:
            return True
        
        return False

