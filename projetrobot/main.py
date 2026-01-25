from classrobot import Robot
import pygame

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600)) # taille de la fenêtre
clock = pygame.time.Clock() # pour gérer le temps

robot = Robot('best_robot', 400, 300)
running = True

while running:
    "Acquisition d'intervalle de temps"
    dt = clock.tick(60) / 500.0

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    v_lin = 0
    v_ang = 0

    if keys[pygame.K_UP]:              #Configurer les données de base
        v_lin = 100
    if keys[pygame.K_DOWN]:
        v_lin = -100
    if keys[pygame.K_LEFT]:
        v_ang = -5
    if keys[pygame.K_RIGHT]:
        v_ang = 5
    
    robot.update_velocity(v_lin, v_ang)  

    robot.move(dt)

    screen.fill((255, 255, 255))
    robot.draw(screen)
    pygame.display.flip()

pygame.quit()
    
    
    

