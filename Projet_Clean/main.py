import pygame
import config as cfg
from core.robot import Robot
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

running = True
while running:
    dt = clock.tick(60) / 1000.0 # on divise par 1000 pour avoir la valeur en secondes (milisecondes -> secondes)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    vg, vd = algo.calculer_commande(robot, dt)
    robot.definir_commande_roues(vg, vd)

    robot.step(dt)

    screen.fill((240, 240, 240))
    dessiner_robot(screen, robot)
    pygame.display.flip()

pygame.quit()
