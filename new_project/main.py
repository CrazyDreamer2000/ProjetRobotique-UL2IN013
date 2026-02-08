import pygame
from Core.robot import Robot
from Core.obstacle import Obstacle
from Affichage.visualisation import dessiner_scene
import variables_environnement as env

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((env.LARGEUR_ECRAN, env.HAUTEUR_ECRAN))# taille de la fenêtre
clock = pygame.time.Clock()# pour gérer le temps

robot = Robot('best_robot', env.LARGEUR_ECRAN // 2, env.HAUTEUR_ECRAN // 2) #Position du robot : milieu de la carte
# Liste pour stocker les obstacles créés par clic de souris
obstacles = []
# Liste pour stocker la trajectoire du robot
trajectoire = []

frame_counter = -1
running = True

while running:
    dt = clock.tick(env.FPS) / 1000.0
    v_lin, v_ang = 0, 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            obstacles.append(Obstacle(event.pos[0], event.pos[1], env.TAILLE_OBSTACLE))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            frame_counter = 0

    # Logique de contrôle (Clavier)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: v_lin = env.VITESSE_LIN
    if keys[pygame.K_DOWN]: v_lin = -env.VITESSE_LIN
    if keys[pygame.K_LEFT]: v_ang = -env.VITESSE_ANG
    if keys[pygame.K_RIGHT]: v_ang = env.VITESSE_ANG

    # Logique Auto (Carré)
    if frame_counter >= 0:
        frame_counter += 1
        stage = (frame_counter // 40) % 8
        if stage % 2 == 0: v_lin = env.VITESSE_LIN_AUTO
        else: v_ang = 1.57 / (40 * dt)
        if frame_counter >= 320: frame_counter = -1

    # Mise à jour du Modèle (Core)
    robot.update_velocity(v_lin, v_ang)
    robot.move(dt, obstacles)
    robot.control_depassement(env.LARGEUR_ECRAN, env.HAUTEUR_ECRAN)

    # Mise à jour de la trajectoire
    if v_lin != 0 or v_ang != 0:
        trajectoire.append((int(robot.x), int(robot.y)))


    # Affichage (View)
    dessiner_scene(screen, robot, obstacles, trajectoire, env)
    pygame.display.flip()

pygame.quit()