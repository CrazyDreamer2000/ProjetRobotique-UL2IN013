# SIMULATION

from dataclasses import dataclass
import config as cfg
import math
import random  # Pour générer des positions aléatoires
from core.geom import (
    coins_rectangle,
    coins_rect_dans_monde,
    polygone_local_vers_monde,
)
from core.types import Pos2D


def _creer_forme_robot_locale(forme, longueur, largeur):
    demi_longueur = longueur / 2
    demi_largeur = largeur / 2

    if forme == "triangle":
        return [
            (demi_longueur, 0.0),
            (-demi_longueur, demi_largeur),
            (-demi_longueur, -demi_largeur),
        ]

    if forme == "cercle":
        rayon = (demi_longueur + demi_largeur) / 2
        points_cercle = []
        nombre_points = 16

        for indice in range(nombre_points):
            angle = 2 * math.pi * indice / nombre_points
            x = rayon * math.cos(angle)
            y = rayon * math.sin(angle)
            points_cercle.append((x, y))

        return points_cercle

    return coins_rectangle(longueur, largeur)


def _point_sur_segment(px, py, ax, ay, bx, by):
    eps = 1e-9
    det = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
    if abs(det) > eps:
        return False
    return (
        min(ax, bx) - eps <= px <= max(ax, bx) + eps
        and min(ay, by) - eps <= py <= max(ay, by) + eps
    )


def _orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2


def _segments_se_coupent(a1, a2, b1, b2):
    o1 = _orientation(a1, a2, b1)
    o2 = _orientation(a1, a2, b2)
    o3 = _orientation(b1, b2, a1)
    o4 = _orientation(b1, b2, a2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and _point_sur_segment(b1[0], b1[1], a1[0], a1[1], a2[0], a2[1]):
        return True
    if o2 == 0 and _point_sur_segment(b2[0], b2[1], a1[0], a1[1], a2[0], a2[1]):
        return True
    if o3 == 0 and _point_sur_segment(a1[0], a1[1], b1[0], b1[1], b2[0], b2[1]):
        return True
    if o4 == 0 and _point_sur_segment(a2[0], a2[1], b1[0], b1[1], b2[0], b2[1]):
        return True

    return False


def _point_dans_polygone(point, polygone):
    point_x, point_y = point
    est_dedans = False

    for indice in range(len(polygone)):
        x1, y1 = polygone[indice]
        x2, y2 = polygone[(indice + 1) % len(polygone)]

        if _point_sur_segment(point_x, point_y, x1, y1, x2, y2):
            return True

        segment_coupe_le_rayon = (y1 > point_y) != (y2 > point_y)
        if segment_coupe_le_rayon:
            x_intersection = x1 + (point_y - y1) * (x2 - x1) / (y2 - y1)
            if x_intersection >= point_x:
                est_dedans = not est_dedans

    return est_dedans


def _polygones_en_collision(polygone_a, polygone_b):
    for indice_a in range(len(polygone_a)):
        a1 = polygone_a[indice_a]
        a2 = polygone_a[(indice_a + 1) % len(polygone_a)]

        for indice_b in range(len(polygone_b)):
            b1 = polygone_b[indice_b]
            b2 = polygone_b[(indice_b + 1) % len(polygone_b)]

            if _segments_se_coupent(a1, a2, b1, b2):
                return True

    if _point_dans_polygone(polygone_a[0], polygone_b):
        return True
    if _point_dans_polygone(polygone_b[0], polygone_a):
        return True

    return False

@dataclass
class Obstacle:
    """
    Classe qui représente un obstacle rectangulaire.
    """
    pos: Pos2D
    largeur: float # Largeur en mètres
    longueur: float # Longueur en mètres

class Monde:
    """
    Simulation de l'environnement réel du robot.
    """
    def __init__(self):
        self.liste_obstacles = []

        # Zone de collision du robot (forme invisible utilisée pour détecter les contacts)
        # Modifiable depuis main.py (rectangle, triangle, cercle + taille).
        self.robot_forme_locale = _creer_forme_robot_locale(
            "rectangle",
            cfg.ROBOT_LONGUEUR,
            cfg.ROBOT_LARGEUR,
        )

        # Créer des obstacles aléatoires dès le départ
        self.creer_obstacles_aleatoires()

    def definir_collision_robot(self, forme="rectangle", longueur=cfg.ROBOT_LONGUEUR, largeur=cfg.ROBOT_LARGEUR):
        """Configure la zone de collision du robot selon la forme et la taille."""
        self.robot_forme_locale = _creer_forme_robot_locale(forme, longueur, largeur)

    def definir_collision_robot_polygone(self, points_locaux):
        """Configure une zone de collision polygonale du robot dans son repère local."""
        self.robot_forme_locale = list(points_locaux)
    
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
            obstacle = Obstacle(Pos2D(x,y,orientation), largeur, longueur)
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

    def _point_hors_monde(self, x, y):
        return x < 0 or x > cfg.LONGUEUR_MONDE or y < 0 or y > cfg.LARGEUR_MONDE

    def _point_dans_obstacle(self, x, y, obstacle):
        cos_obs = math.cos(obstacle.pos.orientation)
        sin_obs = math.sin(obstacle.pos.orientation)

        dx = x - obstacle.pos.x
        dy = y - obstacle.pos.y

        local_x = dx * cos_obs + dy * sin_obs
        local_y = -dx * sin_obs + dy * cos_obs

        return (
            abs(local_x) <= obstacle.longueur / 2
            and abs(local_y) <= obstacle.largeur / 2
        )

    def collision(self, x, y):
        if self._point_hors_monde(x, y):
            return True

        for obs in self.liste_obstacles:
            if self._point_dans_obstacle(x, y, obs):
                return True

        return False
    
    def collision_robot(self, pos):
        """
        Detecte collision du robot avec :
        - obstacles
        - bordures du monde
        """
        forme_robot_monde = polygone_local_vers_monde(
            self.robot_forme_locale,
            pos.x,
            pos.y,
            pos.orientation,
        )

        for point_x, point_y in forme_robot_monde:
            if self._point_hors_monde(point_x, point_y):
                return True

        for obstacle in self.liste_obstacles:
            forme_obstacle_monde = coins_rect_dans_monde(
                obstacle.pos.x,
                obstacle.pos.y,
                obstacle.pos.orientation,
                obstacle.longueur,
                obstacle.largeur,
            )

            if _polygones_en_collision(forme_robot_monde, forme_obstacle_monde):
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
        pas = 0.02
        dist_head = portee_max
        dist_tail = 0
        while dist_head - dist_tail > pas:
            mid = (dist_tail + dist_head) / 2
            # Position du point de test
            test_x = x + (mid + cfg.ROBOT_LONGUEUR / 2) * math.cos(angle)
            test_y = y + (mid + cfg.ROBOT_LARGEUR / 2) * math.sin(angle)
            
            if self.collision(test_x, test_y):
                dist_head = mid
            else:
                dist_tail = mid
        return dist_head  

    
    def arreter_avant_obstacle(self, pos_robot, distance_securite=0.3):
        """
        Vérifie si le robot doit s'arrêter avant un obstacle

        """
        distance_devant = self.lire_distance_devant(pos_robot, portee_max=2.0)
        
        # Arrêter si la distance jusqu'à l'obstacle est inférieure à la distance de sécurité
        if distance_devant <= distance_securite:
            return True
        
        return False

