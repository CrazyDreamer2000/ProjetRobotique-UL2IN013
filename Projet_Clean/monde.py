# SIMULATION

from dataclasses import dataclass
import config as cfg
import math
import random  # Pour générer des positions aléatoires
from core.geom import coins_rectangle_dans_monde
from core.types import Pos2D

@dataclass
class Obstacle:
    """
    Classe qui représente un obstacle rectangulaire.
    """
    pos: Pos2D()
    largeur: float # Largeur en mètres
    longueur: float # Longueur en mètres

class Monde:
    """
    Simulation de l'environnement réel du robot.
    """
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
        """
        Ajoute un obstacle au monde aux coordonnées (x,y)

        Paramètres:
            x : abscisse du nouvel obstacle (pixels)
            y : ordonnée du nouvel obstacle (pixels)
        """
        self.liste_obstacles.append(Obstacle(
            Pos2D(x/cfg.SCALE, y/cfg.SCALE, orientation=0.0),
            cfg.TAILLE_OBSTACLE, 
            cfg.TAILLE_OBSTACLE,
        ))

    def collision(self, x, y):
        # Collision avec bordures
        if (x < 0 or x > cfg.LONGUEUR_MONDE or
            y < 0 or y > cfg.LARGEUR_MONDE):
            return True

        # Collision avec obstacles
        for obs in self.liste_obstacles:

            cos_obs = math.cos(obs.orientation)
            sin_obs = math.sin(obs.orientation)

            dx = x - obs.x
            dy = y - obs.y

            # transformation dans le repère obstacle
            local_x = dx * cos_obs + dy * sin_obs
            local_y = -dx * sin_obs + dy * cos_obs

            if (abs(local_x) <= obs.longueur / 2 and
                abs(local_y) <= obs.largeur / 2):
                return True

        return False
    
    def collision_robot(self, pos):
        """
        Detecte collision du robot avec :
        - obstacles
        - bordures du monde
        """
        for coin_x, coin_y in coins_rectangle_dans_monde(pos.x, pos.y, pos.orientation, cfg.ROBOT_LONGUEUR, cfg.ROBOT_LARGEUR):
            if self.collision(coin_x, coin_y):
                return True
        return False
  
    def lire_distance_devant(self, pos_robot, portee_max=2.0):
        """
        Mesure la distance jusqu'au premier obstacle devant le robot.
        -> Teste des points tous les 2cm devant le robot et renvoie la distance si le point est sur un obstacle
        """
        x, y = pos_robot.x, pos_robot.y
        angle = pos_robot.orientation
        
        # Tester tous les 2cm
        for distance in range(1, int(portee_max / 0.02)):
            d = distance * 0.02  # Distance actuelle
            
            # Position du point de test
            test_x = x + d * math.cos(angle)
            test_y = y + d * math.sin(angle)
            
            if self.collision(test_x, test_y):
                return d
        
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

