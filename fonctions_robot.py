import pygame
import math


def generer_obstacle(mouse_x, mouse_y, taille):
    # Crée un obstacle carré centré sur la position donnée
    return pygame.Rect(mouse_x - taille // 2, 
                       mouse_y - taille // 2,
                       taille, 
                       taille)


def tracer_trajectoire(screen, trajectoire, couleur=(0, 255, 0), epaisseur=3):
    # Dessine la trajectoire du robot sur l'écran
    if len(trajectoire) > 1:
        pygame.draw.lines(screen, couleur, False, trajectoire, epaisseur)


def dessiner_obstacles(screen, obstacles, couleur=(100, 50, 100)):
    # Dessine tous les obstacles sur l'écran
    for obstacle in obstacles:
        pygame.draw.rect(screen, couleur, obstacle)


def effacer_obstacles(obstacles):
    # Efface tous les obstacles
    obstacles.clear()


def calculer_distance_obstacle(robot, obstacle):
    # Calcule la distance entre le robot et un obstacle
    closest_x = max(obstacle.left, min(robot.x, obstacle.right))
    closest_y = max(obstacle.top, min(robot.y, obstacle.bottom))
    
    distance_x = robot.x - closest_x
    distance_y = robot.y - closest_y
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    return distance


