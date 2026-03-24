# SIMULATION

import pygame
import argparse
import config as cfg
from controle import ALGOS
from controle.traducteur import TraducteurSimu
from core.robot import Robot
from monde.monde import Obstacle, Monde

# RLock = verrou partage entre le thread principal et l'affichage.
from threading import RLock
# Classe du thread qui gere la fenetre et le rendu.
from affichage.Affichage import Affichage # Ta nouvelle classe threadée

parser = argparse.ArgumentParser()

parser.add_argument(
    "--algo",
    type=str,
    default="carresafe",
    choices=["carre", "carresafe", "tourner", "eviter", "arret", "contact"],
    help="Nom de l'algorithme (carre, carresafe, tourner, eviter, arret, contact)"
)
# Argument: vitesse des roues
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


# Creation du robot au centre du monde.
robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, args.orientation, cfg.LONGUEUR_MONDE / 2, cfg.LARGEUR_MONDE / 2)
# Creation de l'environnement (obstacles, collisions)
monde = Monde() 

trad = TraducteurSimu(robot, monde)

algo = ALGOS[args.algo](trad, 10, 0.5) # Algo choisi par defaut dans code actuel.
algo.start() # Init de l'algo avant la boucle principale.

lock = RLock() # Verrou partage entre simulation (main) et rendu (thread affichage).

vue = Affichage(robot, monde, lock) # On cree l'affichage en lui donnant robot/monde/lock.
vue.start() # Demarre le thread d'affichage en parallele du main.

clock = pygame.time.Clock()

running = True # Flag principal pour continuer/arreter la simulation.

etait_en_collision = False # Variable pour gerer les colisions ).

# Boucle principale de simulation.
while running:    

    dt = clock.tick(60) / 1000.0

    if not vue.running:     # Si l'utilisateur ferme la fenetre dans le thread affichage, on stoppe ici aussi.
        running = False

    # on protege l'acces aux donnees partagees.
    with lock:
        algo.step()
        robot.step(dt, monde)  # On avance la physique du robot de dt secondes.
        robot.maj_capteurs(dt, monde, robot.vitesse_linaire_actuellement) # On met a jour les capteurs pour le cycle suivant.


# Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.running = False
# Puis on attend sa fin pour une fermeture propre.
vue.join(timeout=1.0)

# Ferme pygame proprement.
pygame.quit()
