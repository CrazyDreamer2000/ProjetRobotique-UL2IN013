# SIMULATION

import pygame
from parser import parse_args
import config as cfg
from controle import ALGOS
from controle.traducteur import TraducteurSimu
from core.robot import Robot
from monde.monde import Obstacle, Monde
import time

# test
from controle.algo_polygone_safe import AlgoPolygoneSafe

# RLock = verrou partage entre le thread principal et l'affichage.
from threading import RLock
# Classe du thread qui gere la fenetre et le rendu.
from affichage.Affichage import Affichage # Ta nouvelle classe threadée

# Lit les arguments de la ligne de commande et renvoie un Namespace , un contenuer avec les valeurs lit
parseArgs = parse_args()

# Creation du robot au centre du monde.
robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, cfg.LONGUEUR_MONDE / 2, cfg.LARGEUR_MONDE / 2)
# Creation de l'environnement (obstacles, collisions)
monde = Monde(robot) 

trad = TraducteurSimu(robot, monde)

#algo = ALGOS[parseArgs.algo](trad, 10, 0.5) # Algo choisi par defaut dans code actuel.
algo = AlgoPolygoneSafe(trad, 10, 6)
algo.start() # Init de l'algo avant la boucle principale.

lock = RLock() # Verrou partage entre simulation (main) et rendu (thread affichage).

vue = Affichage(robot, monde, lock) # On cree l'affichage en lui donnant robot/monde/lock.
vue.start() # Demarre le thread d'affichage en parallele du main.

running = True # Flag principal pour continuer/arreter la simulation.

# Boucle principale de simulation.
while running:    
    
    if not vue.running:     # Si l'utilisateur ferme la fenetre dans le thread affichage, on stoppe ici aussi.
        running = False

    # on protege l'acces aux donnees partagees.
    with lock:
        algo.step()
        monde.step()  # On avance la physique du robot de dt secondes.
        #robot.maj_capteurs(monde, robot.vitesse_linaire_actuellement) # On met a jour les capteurs pour le cycle suivant.
    
    time.sleep(1/60)

# Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.running = False
# Puis on attend sa fin pour une fermeture propre.
vue.join(timeout=1.0)

# Ferme pygame proprement.
pygame.quit()
