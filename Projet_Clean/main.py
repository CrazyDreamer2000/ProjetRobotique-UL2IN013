import pygame
import argparse
import config as cfg
from core.robot import Robot
from monde import Obstacle, Monde
from controle.AlgoCarre import AlgoCarre
from controle.AlgoTournerSurPlace import AlgoTournerSurPlace
from affichage.pygame_view import dessiner_robot, dessiner_obstacles

parser = argparse.ArgumentParser()

parser.add_argument(
    "--algo",
    type=str,
    default="carre",
    choices=["carre", "tourner"],
    help="Nom de l'algorithme (carre, tourner)"
)
parser.add_argument(
    "--vitesse_roues",
    type=float,
    default=4.0,
    help="Vitesse des roues en rad/s"
)
parser.add_argument(
    "--orientation",
    type=str,
    default="droite",
    choices=["droite", "haut", "gauche", "bas"],
    help="Orientation initiale du robot (gauche, droite, haut, bas)"
)
args = parser.parse_args()

# Algorithmes
ALGOS = {
            "tourner" : AlgoTournerSurPlace,
            "carre" : AlgoCarre
        }

pygame.init()
screen = pygame.display.set_mode((cfg.LONGUEUR_MONDE * cfg.SCALE, cfg.LARGEUR_MONDE * cfg.SCALE))
clock = pygame.time.Clock()

robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, args.orientation)
robot.pos.x = cfg.LONGUEUR_MONDE / 2 # metres
robot.pos.y = cfg.LARGEUR_MONDE / 2 #

monde = Monde()
algo = ALGOS[args.algo](args.vitesse_roues)

running = True
while running:
    dt = clock.tick(60) / 1000.0 # on divise par 1000 pour avoir la valeur en secondes (milisecondes -> secondes)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            obs_mousex,obs_mousey= pygame.mouse.get_pos()
            monde.ajouter_obstacle(obs_mousex,obs_mousey)

    robot.maj_capteurs()     
                
    # Calculer la commande SEULEMENT si le robot n'est pas en collision
    if not robot.en_collision:
        v_r_g, v_r_d = algo.calculer_commande(robot, dt)
        robot.definir_commande_roues(v_r_g, v_r_d)

    robot.step(dt, monde)

    screen.fill((240, 240, 240))
    dessiner_robot(screen, robot)
    dessiner_obstacles(screen, monde)
    pygame.display.flip()

pygame.quit()
