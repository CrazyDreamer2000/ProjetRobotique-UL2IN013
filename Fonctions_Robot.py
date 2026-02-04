import pygame
import math
import variables_environnement as env


#Fichier dediée a l'affichage des fonctions de robot suivants : 

# - creation des obstacles et gestion de collisions 
# - controle de depassement du robot de l'ecran 

def generer_obstacle(mouse_x, mouse_y, taille):
    # Crée un obstacle carré centré sur la position donnée
    return pygame.Rect(mouse_x - taille // 2, 
                       mouse_y - taille // 2,
                       taille, 
                       taille)

def est_ctrl_presse():
    mods = pygame.key.get_mods()
    return mods & pygame.KMOD_CTRL

def control_vitesse_robot(vitesse_lin , vitesse_ang):
    
    if (env.MODE_CTRL):
        vitesse_lin = vitesse_lin * env.MULTI_VITESSE_LIN
        vitesse_ang = vitesse_ang * env.MULTI_VITESSE_ANG
    return vitesse_lin , vitesse_ang


def dessiner_obstacles(screen, obstacles, couleur=env.COULEUR_OBSTACLE):
    # Dessine tous les obstacles sur l'écran
    for obstacle in obstacles:
        pygame.draw.rect(screen, couleur, obstacle)


def effacer_obstacles(obstacles):
    # Efface tous les obstacles
    obstacles.clear()


def calculer_distance_obstacle(robot, obstacle):
    # Calcule la distance entre le robot et un obstacle 
    # Trouver le point du rectangle le plus proche du robot
    closest_x = obstacle.left
    if robot.x > obstacle.left:
        closest_x = robot.x
    if robot.x > obstacle.right:
        closest_x = obstacle.right

    closest_y = obstacle.top
    if robot.y > obstacle.top:
        closest_y = robot.y
    if robot.y > obstacle.bottom:
        closest_y = obstacle.bottom
    
    # Distance entre le robot et ce point
    distance_x = robot.x - closest_x
    distance_y = robot.y - closest_y
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    return distance


