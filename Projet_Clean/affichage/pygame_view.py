# SIMULATION

import pygame
import math
import config as cfg
from core.geom import transformer_point_local_vers_monde, transformer_polygone_local_vers_monde, polygone_rectangle_local

def affichage(screen, robot, monde):
    dessiner_robot(screen, robot, monde)
    dessiner_obstacles(screen, monde)

def dessiner_robot(screen, robot, monde):
    """
    Affiche le robot sur la fenêtre pygame
    """
    points_monde = [
        (x * cfg.SCALE, y * cfg.SCALE)
        for x, y in transformer_polygone_local_vers_monde(monde.poly_robot_local, robot.pos)
    ]

    # Corps du robot (même forme que la hitbox de collision)
    pygame.draw.polygon(screen, (80, 130, 200), points_monde)

    longueur_fleche = max(px for px, _ in monde.poly_robot_local) * cfg.SCALE
    # "Fleche" du robot
    cx, cy, ori = robot.pos.x * cfg.SCALE, robot.pos.y * cfg.SCALE, robot.pos.orientation
    pygame.draw.line(screen, (255, 0, 0), (cx, cy), transformer_point_local_vers_monde(longueur_fleche, 0, cx, cy, ori), 2)

def dessiner_obstacles(screen, monde):
    """
    Affiche tous les obstacles sur la fenêtre pygame
    """
    for obs in monde.liste_obstacles:
        points = [
            (x * cfg.SCALE, y * cfg.SCALE)
            for x, y in transformer_polygone_local_vers_monde(obs.poly_local, obs.pos)
        ]

        pygame.draw.polygon(screen, cfg.COULEUR_OBSTACLE, points)