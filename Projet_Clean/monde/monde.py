# SIMULATION

from dataclasses import dataclass
import config as cfg
import math
import random  # Pour générer des positions aléatoires
from core.robot import Robot
from core.geom import polygone_rectangle_local, transformer_polygone_local_vers_monde, normaliser_angle
from core.types import Pos2D
from core.cinematique import CinematiqueDeuxRoues
from .collisions import collision_sat, point_dans_polygone_convexe
import time

@dataclass
class Obstacle:
    """
    Classe qui représente un obstacle rectangulaire.
    """
    pos: Pos2D
    longueur: float # Longueur en millimètres
    largeur: float # Largeur en millimètres
    poly_local: list # Liste des coins

class Monde:
    """
    Simulation de l'environnement réel du robot.
    """
    def __init__(self):
        self.liste_obstacles = []
        
        self.robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, 0, cfg.LONGUEUR_MONDE / 2, cfg.LARGEUR_MONDE / 2)

        self.cinematique = CinematiqueDeuxRoues(self.robot.rayon_roue, self.robot.ecartement_roues)
        
        self.last_step_time = None
        self.last_capteurs_time = None

        self.poly_robot_local = polygone_rectangle_local(cfg.ROBOT_LONGUEUR, cfg.ROBOT_LARGEUR)

        self.creer_obstacles_aleatoires() # Création d'obstacles aléatoires

        print("Monde créé")
    
    def ajouter_obstacle(self, x, y, longueur=cfg.TAILLE_OBSTACLE, largeur=cfg.TAILLE_OBSTACLE):
        """
        Ajoute un obstacle au monde aux coordonnées (x,y)

        Paramètres:
            x : abscisse du nouvel obstacle (pixels)
            y : ordonnée du nouvel obstacle (pixels)
        """
        self.liste_obstacles.append(Obstacle(
            Pos2D(x/cfg.SCALE, y/cfg.SCALE, orientation=random.uniform(0, 2 * math.pi)),
            longueur, 
            largeur,
            polygone_rectangle_local(longueur, largeur)
        ))

    def creer_obstacles_aleatoires(self):
        """
        Creation de 5 obstacles dans le monde
        """
        # ici 5 zones (4 coins + 1 bord) 
        zones = [
            # (x_min, x_max, y_min, y_max, nom)
            (500, 1500, 500, 1000, "Coin bas-gauche"),      # Zone 1
            (3000, 4000, 500, 1000, "Coin bas-droite"),      # Zone 2  
            (500, 1500, 2000, 2500, "Coin haut-gauche"),     # Zone 3
            (3000, 4000, 2000, 2500, "Coin haut-droite"),     # Zone 4
            (2000, 2500, 300, 700, "Bord bas-centre")       # Zone 5
        ]
        
        # un obstacle à la fois
        for i, (x_min, x_max, y_min, y_max, nom) in enumerate(zones):
            
            # Position aléatoire DANS la zone
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            
            # Orientation aléatoire (0 à 360°)
            orientation = random.uniform(0, 2 * math.pi)
            
            # Dimensions aléatoires
            longueur = int(random.uniform(300, 600))  # 30-60 cm
            largeur = int(random.uniform(150, 250)) # 15-25 cm
            
            # Créer l'obstacle
            self.ajouter_obstacle(x * cfg.SCALE, y * cfg.SCALE, longueur, largeur) # multiplication par scale est temporaire
            
            print(f" Obstacle {i+1} : {nom} ({x:.2f}, {y:.2f}) angle={math.degrees(orientation):.0f}°")

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
  
    def lire_distance_devant(self, pos_robot, portee=(0.5, 8000.0)):
        """
        Mesure la distance jusqu'au premier obstacle devant le robot.
        -> Teste des points tous les 2cm devant le robot et renvoie la distance si le point est sur un obstacle
        """
        min = portee[0]
        max = portee[1]

        dist = None

        while (max - min) > 1: # On prend la valeur au milimètre près
            dist = (min + max) // 2

            # Position du point de test
            test_x = pos_robot.x + (cfg.ROBOT_LONGUEUR / 2 + dist) * math.cos(pos_robot.orientation)
            test_y = pos_robot.y + (cfg.ROBOT_LONGUEUR / 2 + dist) * math.sin(pos_robot.orientation)

            if self.collision_point(test_x, test_y):
                max = dist
            else:
                min = dist
        
        return dist

    
    def calcul_dt(self, last_time):
        now = time.perf_counter() #on lit l’heure actuelle
        
        if last_time is None: #c’est le tout premier appel, on n’a pas encore d’ancienne heure
            return 0.0, now
        
        dt = now - last_time #on calcule le temps écoulé depuis le dernier appel
        return dt, now # le nouveau temps actuel now qui va remplacer last-time dans robot

    def maj_capteurs(self, vitesse_actuelle):
        """
        Mettre à jour l'état du capteur du robot
        (a = Δv / Δt)
        """

        # La mise à jour de dt et le temps écoulé depuis le dernier appel
        dt, self.last_capteurs_time = self.calcul_dt(self.last_capteurs_time)

        accel = 0.0 # Initialiser l'accélération
        if dt > 0:
           accel = (vitesse_actuelle - self.robot.vitesse_precedante) / dt
        self.robot.vitesse_precedante = vitesse_actuelle

        self.robot.dist_obstacle = self.lire_distance_devant(self.robot.pos)
        dist = self.robot.dist_obstacle
        #print(dist)  #pour tester
        self.robot.capteurs.accelerometre = accel
        self.robot.capteurs.capteur_distance = dist

    def step(self):
        """
        Avance la simulation de dt secondes
        - met à jour les roues
        - calcule le mouvement
        - met à jour la pos (avec vérification des collisions)
        - gère la reculade après collision
        """

        # La mise à jour de dt et le temps écoulé depuis le dernier appel
        dt, self.last_step_time = self.calcul_dt(self.last_step_time)

        if dt<0:
            return
        
        self.maj_capteurs(self.robot.vitesse_linaire_actuellement)

        # Mise a jour de la rotation totale des roues
        self.robot.roue_gauche.rotation_totale += self.robot.roue_gauche.vitesse_rotation * dt
        self.robot.roue_droite.rotation_totale += self.robot.roue_droite.vitesse_rotation * dt

        # Calcul de la nouvelle position possible
        vitesse_avant, vitesse_rotation = self.cinematique.vitesses_robot_depuis_roues(self.robot.roue_gauche.vitesse_rotation, self.robot.roue_droite.vitesse_rotation)
        pos_suiv = self.cinematique.avance_pos(self.robot.pos, vitesse_avant, vitesse_rotation, dt)
        
        self.robot.en_collision = self.collision(pos_suiv)
        if not self.robot.en_collision:
            self.robot.pos = pos_suiv

        # Normaliser l'orientation dans [-pi, +pi] 
        self.robot.pos.orientation = normaliser_angle(self.robot.pos.orientation)

        self.robot.vitesse_linaire_actuellement = vitesse_avant # utiliser le v pour calculer acceleration
