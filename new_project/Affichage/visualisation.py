import pygame
import math

def dessiner_scene(screen, robot, obstacles, trajectoire, env):
    """Fonction principale d'affichage pour toute la simulation"""
    screen.fill((255, 255, 255))
    
    # Dessiner les obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, env.COULEUR_OBSTACLE, (obs.x, obs.y, obs.w, obs.h))
    
    # Dessiner la trajectoire
    if len(trajectoire) > 1:
        pygame.draw.lines(screen, env.COULEUR_TRAJECTOIRE, False, trajectoire, env.EPAISSEUR_TRAJECTOIRE)
    
    # Dessiner le robot
    pygame.draw.circle(screen, env.ROBOT_COULEUR, (int(robot.x), int(robot.y)), robot.rayon)
    head_x = robot.x + 25 * math.cos(robot.angle)
    head_y = robot.y + 25 * math.sin(robot.angle)
    pygame.draw.line(screen, env.ROBOT_TETE_COULEUR, (robot.x, robot.y), (head_x, head_y), 3)