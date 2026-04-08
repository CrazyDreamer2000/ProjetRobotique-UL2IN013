# SIMULATION

from dataclasses import dataclass
import config as cfg
import math
import random  # Pour générer des positions aléatoires
from core.geom import polygone_rectangle_local, transformer_polygone_local_vers_monde
from core.types import Pos2D
from .collisions import collision_sat, point_dans_polygone_convexe

@dataclass
class Obstacle:
    """
    Classe qui représente un obstacle rectangulaire.
    """
    pos: Pos2D
    longueur: float # Longueur en mètres
    largeur: float # Largeur en mètres
    poly_local: list # Liste des coins

class Monde:
    """
    Simulation de l'environnement réel du robot.
    """
    def __init__(self):
        self.liste_obstacles = []

        # Zone de collision du robot (forme invisible utilisée pour détecter les contacts)
        # Modifiable depuis main.py (rectangle, triangle, cercle + taille).
        self.poly_robot_local = polygone_rectangle_local(cfg.ROBOT_LONGUEUR, cfg.ROBOT_LARGEUR)
        # Créer des obstacles aléatoires dès le départ
        self.creer_obstacles()
    
    def ajouter_obstacle(self, x, y, longueur=cfg.TAILLE_OBSTACLE, largeur=cfg.TAILLE_OBSTACLE):
        """
        Ajoute un obstacle au monde aux coordonnées (x,y)

        Paramètres:
            x : abscisse du nouvel obstacle (pixels)
            y : ordonnée du nouvel obstacle (pixels)
        """
        self.liste_obstacles.append(Obstacle(
            Pos2D(x/cfg.SCALE, y/cfg.SCALE, 0),
            longueur, 
            largeur,
            polygone_rectangle_local(longueur, largeur)
        ))

    def creer_obstacles(self):
        """
        Creation de 3 obstacles dans le monde
        """
        self.ajouter_obstacle(cfg.LONGUEUR_MONDE/2*cfg.SCALE, cfg.LARGEUR_MONDE/2*cfg.SCALE) # milieu
        print(cfg.LONGUEUR_MONDE/2*cfg.SCALE, cfg.LARGEUR_MONDE/2*cfg.SCALE)
        self.ajouter_obstacle(cfg.LONGUEUR_MONDE/2*cfg.SCALE, cfg.TAILLE_OBSTACLE/2 * cfg.SCALE)  # milieu haut
        print(cfg.LONGUEUR_MONDE/2*cfg.SCALE, cfg.TAILLE_OBSTACLE/2 * cfg.SCALE)
        self.ajouter_obstacle(cfg.LONGUEUR_MONDE/2*cfg.SCALE, (cfg.LARGEUR_MONDE - (cfg.TAILLE_OBSTACLE/2)) * cfg.SCALE) # milieu bas
        print(cfg.LONGUEUR_MONDE/2*cfg.SCALE, (cfg.LARGEUR_MONDE - (cfg.TAILLE_OBSTACLE/2)) * cfg.SCALE)
        
    def _point_hors_monde(self, x: float, y: float) -> bool:
        return (
            x < 0.0
            or x > cfg.LONGUEUR_MONDE
            or y < 0.0
            or y > cfg.LARGEUR_MONDE
        )

    def collision(self, pos_robot: Pos2D) -> bool:
        # Polygone robot en monde
        robot_poly = transformer_polygone_local_vers_monde(self.poly_robot_local, pos_robot)

        # bordures: si un coin sort
        for x, y in robot_poly:
            if self._point_hors_monde(x,y):
                return True

        # obstacles
        for obs in self.liste_obstacles:
            obs_poly = transformer_polygone_local_vers_monde(obs.poly_local, obs.pos)
            if collision_sat(robot_poly, obs_poly):
                return True

        return False

    def collision_point(self, x: float, y: float) -> bool:
        """
        Retourne True si le point (x,y) est :
        - hors du monde
        - ou dans un obstacle
        """
        if self._point_hors_monde(x, y):
            return True

        for obs in self.liste_obstacles:
            obs_poly = transformer_polygone_local_vers_monde(obs.poly_local, obs.pos)

            if point_dans_polygone_convexe(x, y, obs_poly):
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
            
            if self.collision_point(test_x, test_y):
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
