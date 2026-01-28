from classrobot import Robot
import pygame
import math

# Initialisation de Pygame
#Resolution global var approx
resX,resY=1600,900

pygame.init()
screen = pygame.display.set_mode((resX, resY)) # taille de la fenêtre

#pygame_rect_object = pygame.Rect(50, 50, 100, 100) Pas fonctionnel, peut être créer un objet obstacle ou rectangle
#pygame.draw.rect(screen, 'black', pygame_rect_object)

clock = pygame.time.Clock() # pour gérer le temps

robot = Robot('best_robot', resX/2, resY/2)
running = True
frame_counter = -1


while running:
    "Acquisition d'intervalle de temps"
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    v_lin = 0   
    v_ang = 0

    #PRINT DEBUG
    #print(keys[pygame.K_UP],keys[pygame.K_DOWN],keys[pygame.K_LEFT],keys[pygame.K_RIGHT])
    #print(robot.x,robot.y)
    #print(v_lin,robot.v_linear)
    #print(v_ang,robot.v_angular)
   

    if keys[pygame.K_UP]:       #Configurer les données de base
        v_lin = resX/8
        robot.update_velocity(v_lin, v_ang)
    if keys[pygame.K_DOWN]:
        v_lin = -resX/8
        robot.update_velocity(v_lin, v_ang)
    if keys[pygame.K_LEFT]:
        v_ang = resY/150
        robot.update_velocity(v_lin, v_ang)
    if keys[pygame.K_RIGHT]:
        v_ang = -resY/150
        robot.update_velocity(v_lin, v_ang)
    
    if  frame_counter >= 0:
        frame_counter += 1
        stage = frame_counter // 40

        if stage in [0, 2, 4, 6]:
            v_lin = 200
        if stage in [1, 3 ,5]:
            v_ang = (math.pi / 2) / (40 * dt)
        if frame_counter == 280:
            frame_counter = -1
    
    robot.update_velocity(v_lin, v_ang)  

    robot.move(dt)

    screen.fill((255, 255, 255))
    robot.draw(screen)
    pygame.display.flip()


pygame.quit()
    
    
    

