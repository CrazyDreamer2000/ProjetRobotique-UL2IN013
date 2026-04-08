# SIMULATION

import pygame
from parser import parse_args
import config as cfg
from controle import ALGOS
from controle.traducteur import TraducteurSimu
from core.robot import Robot
from monde.monde import Obstacle, Monde
import time

import math

# RLock = verrou partage entre le thread principal et l'affichage.
from threading import RLock
# Classe du thread qui gere la fenetre et le rendu.
from affichage.Affichage import Affichage # Ta nouvelle classe threadée

# Lit les arguments de la ligne de commande et renvoie un Namespace , un contenuer avec les valeurs lit
parseArgs = parse_args()

# Creation du robot au centre du monde.

# EXERCICE 1:
# robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, 0+cfg.ROBOT_LONGUEUR/2 + 0.3, cfg.LARGEUR_MONDE - (cfg.ROBOT_LARGEUR)/ 2 - 0.1) # +0.3 et -0.1 pour une petite marge pour faire un hexagone
robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, 0+cfg.ROBOT_LONGUEUR/2 + 0.3, cfg.LARGEUR_MONDE / 2 ) # +0.3 pour une petite marge pour faire un hexagone
robot2 = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, "bas", cfg.LONGUEUR_MONDE - cfg.ROBOT_LONGUEUR/2 - 1, cfg.LARGEUR_MONDE / 2)
#print('robot : ',0+cfg.ROBOT_LONGUEUR/2 - 50, cfg.LARGEUR_MONDE - (cfg.ROBOT_LARGEUR)/ 2 - 50)

# Creation de l'environnement (obstacles, collisions)
monde = Monde() 

trad = TraducteurSimu(robot, monde)
trad2 = TraducteurSimu(robot2, monde)

algo = ALGOS['carre'](trad, 10, 0.5) # Algo choisi par defaut dans code actuel.
algo.start() # Init de l'algo avant la boucle principale.

algo2 = ALGOS['allerretour'](trad2, 10, 0.5)
algo2.start()

lock = RLock() # Verrou partage entre simulation (main) et rendu (thread affichage).

vue = Affichage([robot, robot2], monde, lock) # On cree l'affichage en lui donnant robot/monde/lock.
vue.start() # Demarre le thread d'affichage en parallele du main.

running = True # Flag principal pour continuer/arreter la simulation.

# Boucle principale de simulation.
while running:    
    
    if not vue.running:     # Si l'utilisateur ferme la fenetre dans le thread affichage, on stoppe ici aussi.
        running = False

    # on protege l'acces aux donnees partagees.
    with lock:
        algo.step()
        algo2.step()
        robot.step(monde)  # On avance la physique du robot de dt secondes.
        robot2.step(monde)
        robot.maj_capteurs(monde, robot.vitesse_linaire_actuellement) # On met a jour les capteurs pour le cycle suivant.
        robot2.maj_capteurs(monde, robot.vitesse_linaire_actuellement)
    
    time.sleep(1/60)

# Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.running = False
# Puis on attend sa fin pour une fermeture propre.
vue.join(timeout=1.0)

# Ferme pygame proprement.
pygame.quit()
