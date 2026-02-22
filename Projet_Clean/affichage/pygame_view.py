# SIMULATION

import pygame
import math
import config as cfg
from core.geom import coins_rect_dans_monde, transformer_point_local_vers_monde

def affichage(screen, robot, monde):
    dessiner_robot(screen, robot)
    dessiner_obstacles(screen, monde)

def dessiner_robot(screen, robot):
    """
    Affiche le robot sur la fenêtre pygame
    """
    cx, cy, ori = robot.pos.x*cfg.SCALE, robot.pos.y*cfg.SCALE, robot.pos.orientation

    # Corps du robot
    pygame.draw.polygon(screen, (80, 130, 200), coins_rect_dans_monde(cx, cy, ori, cfg.ROBOT_LONGUEUR*cfg.SCALE, cfg.ROBOT_LARGEUR*cfg.SCALE))
    # "Fleche" du robot
    pygame.draw.line(screen, (255, 0, 0), (cx, cy), transformer_point_local_vers_monde(cfg.ROBOT_LONGUEUR/2*cfg.SCALE, 0, cx, cy, ori), 2)

def dessiner_obstacles(screen, monde, couleur=cfg.COULEUR_OBSTACLE):
    """
    Affiche tous les obstacles sur la fenêtre pygame
    """
    for obs in monde.liste_obstacles:
        pygame.draw.polygon(screen, couleur, coins_rect_dans_monde(obs.pos.x*cfg.SCALE, obs.pos.y*cfg.SCALE, obs.pos.orientation, cfg.TAILLE_OBSTACLE*cfg.SCALE, cfg.TAILLE_OBSTACLE*cfg.SCALE))
                