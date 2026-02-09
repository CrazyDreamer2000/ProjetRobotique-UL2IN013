import pygame
import math

SCALE = 200  # pixels par mètre

ROBOT_L = 0.30 # Longueur
ROBOT_l = 0.20 # largeur
ECARTEMENT_ROUES = 0.15

def transformer_point(x, y, cx, cy, angle):
    """Transforme position des points du robot en points sur le repère
    x, y: Coordonnées d'un point dans le repère du robot (ex: (x=20, y=10) = 20 pixels devant le robot, 10 pixels à gauche)
    cx, cy: Coordonnées du centre du robot dans le monde
    xr, yr: x et y après rotation"""
    xr = x * math.cos(angle) - y * math.sin(angle) # Formule de rotation de points en maths
    yr = x * math.sin(angle) + y * math.cos(angle) #
    return cx + xr, cy + yr

def dessiner_robot(screen, robot):
    cx = robot.pos.x * SCALE
    cy = robot.pos.y * SCALE
    ori = robot.pos.orientation

    L = ROBOT_L * SCALE / 2 # de mètres -> en pixels, puis /2 pour définir les coins
    l = ROBOT_l * SCALE / 2 #

    coins = [(-L, -l), (L, -l), (L, l), (-L, l)]
    points = [transformer_point(x, y, cx, cy, ori) for x, y in coins]

    pygame.draw.polygon(screen, (80, 130, 200), points)

    # direction avant
    fx, fy = transformer_point(L, 0, cx, cy, ori)
    pygame.draw.line(screen, (255, 0, 0), (cx, cy), (fx, fy), 2)
