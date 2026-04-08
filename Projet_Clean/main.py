# SIMULATION

import pygame
from parser import parse_args
import config as cfg
from controle import ALGOS
from controle.traducteur import TraducteurSimu
from core.robot import Robot
from monde.monde import Obstacle, Monde
from controle.algo_carre import AlgoCarre
from controle.algo_aller_retour import AlgoAllerRetour
import time

# RLock = verrou partage entre le thread principal et l'affichage.
from threading import RLock
# Classe du thread qui gere la fenetre et le rendu.
from affichage.Affichage import Affichage # Ta nouvelle classe threadée

# Lit les arguments de la ligne de commande et renvoie un Namespace , un contenuer avec les valeurs lit
parseArgs = parse_args()


# Creation du robot au centre du monde.
robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, 0.5, 2.0)
# Creation de l'environnement (obstacles, collisions)
monde = Monde() 

trad = TraducteurSimu(robot, monde)

algo = ALGOS[parseArgs.algo](trad, 10, 0.5) # Algo choisi par defaut dans code actuel.
algo.start() # Init de l'algo avant la boucle principale.

# Q2.1

robot_g = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, "droite", 1.0, 1.5)

robot_d = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, "droite", 3.5, 1.5)

trad_g = TraducteurSimu(robot_g, monde)
trad_d = TraducteurSimu(robot_d, monde)

# Q2.2 : Définition des algos (on verra le détail juste après)
algo_g = AlgoCarre(trad_g, parseArgs.vitesse_roues) 
algo_d = AlgoAllerRetour(trad_d, parseArgs.vitesse_roues) # Nouvel algo à créer

algo_g.start()
algo_d.start()

mes_robots = [robot, robot_g, robot_d]
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
        algo_g.step()
        algo_d.step()
        robot.step(monde)  # On avance la physique du robot de dt secondes.
        robot_g.step(monde)
        robot_d.step(monde)
        robot.maj_capteurs(monde, robot.vitesse_linaire_actuellement) # On met a jour les capteurs pour le cycle suivant.
    
    time.sleep(1/60)

# Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.running = False
# Puis on attend sa fin pour une fermeture propre.
vue.join(timeout=1.0)

# Ferme pygame proprement.
pygame.quit()
