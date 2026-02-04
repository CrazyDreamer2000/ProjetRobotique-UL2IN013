from Class_robot import Robot
from Fonctions_Robot import *
import variables_environnement as env

import pygame
import math
import numpy as np

# Initialisation de Pygame
pygame.init()

screen = pygame.display.set_mode((env.LARGEUR_ECRAN, env.HAUTEUR_ECRAN)) # taille de la fenêtre
clock = pygame.time.Clock() # pour gérer le temps

robot = Robot('best_robot', env.LARGEUR_ECRAN // 2, hauteur_ecran // 2) #Position du robot : milieu de la carte

# Liste pour stocker la trajectoire du robot
trajectoire = []

# Liste pour stocker les obstacles créés par clic de souris
obstacles = []
taille_obstacle = env.TAILLE_OBSTACLE  # Taille des obstacles carrés

running = True
frame_counter = -1
forest_mode = False  # Toggle pour le mode forêt

#Gestion des evenements 

while running:

    #Acquisition d'intervalle de temps
    dt = clock.tick(env.FPS) / 1000.0

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                frame_counter = 0
                trajectoire.clear()  # Efface l'ancienne trajectoire
            if event.key == pygame.K_f:
                forest_mode = not forest_mode  # Toggle le mode forêt
        
        # Créer un obstacle au clic de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            obstacle = generer_obstacle(mouse_x, mouse_y, taille_obstacle)
            obstacles.append(obstacle)  

    mods = pygame.key.get_mods()
    if mods & pygame.KMOD_CTRL:
        env.MODE_CTRL = True
    else:
        env.MODE_CTRL = False

    #Gestion des touches 
    keys = pygame.key.get_pressed()
    v_lin = 0
    v_ang = 0

    #Definir une action pour chaque touche (UP / DOWN / RIGHT / LEFT)
    if keys[pygame.K_UP]:
        v_lin = env.VITESSE_LIN
    if keys[pygame.K_DOWN]:
        v_lin = -env.VITESSE_LIN
    if keys[pygame.K_LEFT]:
        v_ang = -env.VITESSE_ANG
    if keys[pygame.K_RIGHT]:
        v_ang = env.VITESSE_ANG
    
    if  frame_counter >= 0:
        frame_counter += 1
        stage = frame_counter // 40

        if stage in [0, 2, 4, 6]:
            v_lin = env.VITESSE_LIN_AUTO
        if stage in [1, 3 ,5]:
            v_ang = (math.pi / 2) / (40 * dt)
        if frame_counter == 280:
            frame_counter = -1
    
    robot.update_velocity(v_lin, v_ang)
    v_lin , v_ang = control_vitesse_robot(v_lin, v_ang)
    robot.update_velocity(v_lin, v_ang)
    robot.move(dt, obstacles)  # On passe la liste des obstacles
    robot.control_depassement(screen)

    # Ajouter la position actuelle à la trajectoire seulement si le robot bouge
    if robot.v_linear != 0 or robot.v_angular != 0:
        trajectoire.append((int(robot.x), int(robot.y)))
    else:
        # Si le robot est immobile, réinitialiser la trajectoire
        trajectoire.clear()
    
    # Remplir le fond blanc
    screen.fill((255, 255, 255))
    
    # Dessiner les obstacles
    dessiner_obstacles(screen, obstacles)
    
    # Dessiner la trajectoire du robot
    #tracer_trajectoire(screen, trajectoire)
    if len(trajectoire) > 1:
        if robot.v_linear != 0 or robot.v_angular != 0:
            pygame.draw.lines(screen, env.COULEUR_TRAJECTOIRE, False, trajectoire, env.EPAISSEUR_TRAJECTOIRE)
            
    robot.draw(screen)
    pygame.display.flip()

pygame.quit()
    
    
    
