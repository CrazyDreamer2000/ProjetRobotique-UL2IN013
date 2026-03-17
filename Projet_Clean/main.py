# SIMULATION

import pygame
import argparse
import config as cfg
from core.robot import Robot
from monde.monde import Obstacle, Monde
from controle.AlgoCarre import AlgoCarre
from controle.AlgoTournerSurPlace import AlgoTournerSurPlace
from controle.AlgoArretDevantObstacle import AlgoArretDevantObstacle
from controle.AlgoReculeTourneContact import AlgoReculeTourneContact
from controle.AlgoEviter import AlgoEviter
from affichage.pygame_view import affichage

parser = argparse.ArgumentParser()

parser.add_argument(
    "--algo",
    type=str,
    default="eviter",
    choices=["carre", "tourner", "eviter", "arret", "contact"],
    help="Nom de l'algorithme (carre, tourner, eviter, arret, contact)"
)
parser.add_argument(
    "--vitesse_roues",
    type=float,
    default=7.0,
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
            "carre" : AlgoCarre,
            "tourner" : AlgoTournerSurPlace,
            "eviter" : AlgoEviter,
            "arret" : AlgoArretDevantObstacle,
            "contact" : AlgoReculeTourneContact
        }

pygame.init()
screen = pygame.display.set_mode((cfg.LONGUEUR_MONDE * cfg.SCALE, cfg.LARGEUR_MONDE * cfg.SCALE))
clock = pygame.time.Clock()

robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, args.orientation, cfg.LONGUEUR_MONDE / 2, cfg.LARGEUR_MONDE / 2)
monde = Monde()
algo = ALGOS[args.algo](args.vitesse_roues)

etait_en_collision = False # Pour détecter le début d'un choc
running = True
while running:
    dt = clock.tick(60) / 1000.0 # on divise par 1000 pour avoir la valeur en secondes (milisecondes -> secondes)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            obs_mousex,obs_mousey= pygame.mouse.get_pos()
            monde.ajouter_obstacle(obs_mousex,obs_mousey)

        # Réinitialisation avec la touche R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, args.orientation, cfg.LONGUEUR_MONDE / 2, cfg.LARGEUR_MONDE / 2)
                monde = Monde() # On vide aussi les obstacles pour repartir à zéro
                algo = ALGOS[args.algo](args.vitesse_roues)
        
    v_r_g, v_r_d = algo.calculer_commande(robot, dt)
 
    robot.definir_commande_roues(v_r_g, v_r_d)

    robot.step(dt, monde)

    robot.maj_capteurs(dt, monde, robot.vitesse_linaire_actuellement)  

    screen.fill((240, 240, 240))

    affichage(screen, robot, monde)

    pygame.display.flip()

pygame.quit()
