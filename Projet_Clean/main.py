import pygame
import config as cfg
from core.robot import Robot
from monde import Obstacle
from controle.AlgoCarre import AlgoCarre
from affichage.pygame_view import dessiner_robot

largeur, hauteur = 900, 600 # = 4.5 mètres * 3 mètres

pygame.init()
screen = pygame.display.set_mode((largeur, hauteur))
clock = pygame.time.Clock()

robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES)
robot.pos.x = (largeur / 2) / cfg.SCALE # pixels -> metres
robot.pos.y = (hauteur / 2) / cfg.SCALE #

algo = AlgoCarre()
obstacles=[]
corners=[]
running = True
while running:
    dt = clock.tick(60) / 1000.0 # on divise par 1000 pour avoir la valeur en secondes (milisecondes -> secondes)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            obs_mousex,obs_mousey= pygame.mouse.get_pos()
            obstacle = Obstacle(obs_mousex,obs_mousey,cfg.TAILLE_OBSTACLE,cfg.TAILLE_OBSTACLE)
            obstacles.append(obstacle)
            for obs in obstacles:       
                print(obs.x,obs.y,obs.longueur,obs.largeur)
                corners.append(obs.get_corners())
                print(corners)
                
    vg, vd = algo.calculer_commande(robot, dt)
    robot.definir_commande_roues(vg, vd)

    robot.step(dt)

    screen.fill((240, 240, 240))
    dessiner_robot(screen, robot)
    #dessiner_obstacles(screen, obstacles)
    pygame.display.flip()

pygame.quit()
