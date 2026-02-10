import pygame
import math
import config as cfg

def transformer_point(x, y, cx, cy, angle):
    """Transforme position des points du robot en points sur le repère
    x, y: Coordonnées d'un point dans le repère du robot en pixels (ex: (x=20, y=10) = 20 pixels devant le robot, 10 pixels à gauche)
    cx, cy: Coordonnées du centre du robot dans le monde (pixels)
    xr, yr: x et y après rotation (pixels)"""
    xr = x * math.cos(angle) - y * math.sin(angle) # Formule de rotation de points en maths
    yr = x * math.sin(angle) + y * math.cos(angle) #
    return cx + xr, cy + yr

def dessiner_robot(screen, robot):
    """Affiche le robot sur pygame"""
    cx = robot.pos.x * cfg.SCALE # pixels (mètres -> pixels avec *SCALE)
    cy = robot.pos.y * cfg.SCALE # pixels
    ori = robot.pos.orientation

    L = cfg.ROBOT_LONGUEUR * cfg.SCALE / 2 # pixels (mètres -> pixels avec *SCALE), puis /2 pour ensuite définir les coins
    l = cfg.ROBOT_LARGEUR * cfg.SCALE / 2 #

    coins = [(-L, -l), (L, -l), (L, l), (-L, l)] # pixels (repère robot)
    points = [transformer_point(x, y, cx, cy, ori) for x, y in coins]  # pixels (repère écran)

    pygame.draw.polygon(screen, (80, 130, 200), points) # pour dessiner le robot sur pygame
                                                        # on utilise polygon et pas rect pour afficher un rectangle pas forcemment aligné à l'écran
    # direction avant
    fx, fy = transformer_point(L, 0, cx, cy, ori) # pixels (devant du robot)
    pygame.draw.line(screen, (255, 0, 0), (cx, cy), (fx, fy), 2) # dessiner la direction de l'ecran

def dessiner_obstacles(screen, obstacles, couleur=cfg.COULEUR_OBSTACLE):
    # Dessine tous les obstacles sur l'écran
    corners=[]
    for obs in obstacles:
        corners.append(obs.get_corners())
    for obs_corners in corners:
        pygame.draw.polygon(screen,cfg.COULEUR_OBSTACLE,obs_corners)