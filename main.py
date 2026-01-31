from classrobot import Robot
from fonctions_robot import generer_obstacle, tracer_trajectoire, dessiner_obstacles, effacer_obstacles
import pygame
import math

# Initialisation de Pygame
pygame.init()
largeur_ecran = 800
hauteur_ecran = 600
screen = pygame.display.set_mode((largeur_ecran, hauteur_ecran)) # taille de la fenêtre
clock = pygame.time.Clock() # pour gérer le temps

robot = Robot('best_robot', largeur_ecran // 2, hauteur_ecran // 2) #Position du robot : milieu de la carte

# Liste pour stocker la trajectoire du robot
trajectoire = []

# Liste pour stocker les obstacles créés par clic de souris
obstacles = []
taille_obstacle = 60  # Taille des obstacles carrés

running = True
frame_counter = -1


#Gestion des evenements 

while running:

    #Acquisition d'intervalle de temps
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                frame_counter = 0
                trajectoire.clear()  # Efface l'ancienne trajectoire
            if event.key == pygame.K_e:
                trajectoire.clear()  # Efface la trace du robot
        
        # Créer un obstacle au clic de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            obstacle = generer_obstacle(mouse_x, mouse_y, taille_obstacle)
            obstacles.append(obstacle)
    
    #Gestion des touches 
    keys = pygame.key.get_pressed()
    v_lin = 0
    v_ang = 0


    #Definir une action pour chaque touche (UP / DOWN / RIGHT / LEFT)
    if keys[pygame.K_UP]:
        v_lin = 150
    if keys[pygame.K_DOWN]:
        v_lin = -150
    if keys[pygame.K_LEFT]:
        v_ang = -8
    if keys[pygame.K_RIGHT]:
        v_ang = 8
    
    if  frame_counter >= 0:
        frame_counter += 1
        stage = frame_counter // 40

        if stage in [0, 2, 4, 6]:
            v_lin = 250
        if stage in [1, 3 ,5]:
            v_ang = (math.pi / 2) / (40 * dt)
        if frame_counter == 280:
            frame_counter = -1
    
    robot.update_velocity(v_lin, v_ang)  

    robot.move(dt, obstacles)  # On passe la liste des obstacles
    robot.control_depassement(screen)
    
    # Ajouter la position actuelle à la trajectoire
    trajectoire.append((int(robot.x), int(robot.y)))

    screen.fill((255, 255, 255))
    
    # Dessiner les obstacles
    dessiner_obstacles(screen, obstacles)
    
    # Dessiner la trajectoire du robot
    tracer_trajectoire(screen, trajectoire)
    
    robot.draw(screen)
    pygame.display.flip()

pygame.quit()
    

    

