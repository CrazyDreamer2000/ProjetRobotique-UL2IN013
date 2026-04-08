# SIMULATION

import pygame
from parser import parse_args
import config as cfg
from controle import ALGOS
from controle.traducteur import TraducteurSimu
from core.robot import Robot
from monde.monde import Obstacle, Monde
import time

# RLock = verrou partage entre le thread principal et l'affichage.
from threading import RLock
# Classe du thread qui gere la fenetre et le rendu.
from affichage.Affichage import Affichage # Ta nouvelle classe threadee

# Lit les arguments de la ligne de commande et renvoie un Namespace , un contenuer avec les valeurs lit
parseArgs = parse_args()

# Creation robots
robotdroite = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, (cfg.LONGUEUR_MONDE / 2)+1, cfg.LARGEUR_MONDE / 2)
robotgauche = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, (cfg.LONGUEUR_MONDE / 2)-1, cfg.LARGEUR_MONDE / 2)

# Creation de l'environnement (obstacles, collisions)
monde = Monde() 

tradgauche = TraducteurSimu(robotgauche, monde)
traddroite = TraducteurSimu(robotdroite, monde)


algogauche = ALGOS[parseArgs.algo](tradgauche, 10, 0.5) # Algo choisi par defaut dans code actuel.
algodroite = ALGOS[parseArgs.algo](traddroite, 10, 0.5)
algogauche.start() # Init de l'algo avant la boucle principale.
algodroite.start()

lock = RLock() # Verrou partage entre simulation (main) et rendu (thread affichage).

vue = Affichage(robotgauche, robotdroite, monde, lock) # On cree l'affichage en lui donnant robot/monde/lock.
vue.start() # Demarre le thread d'affichage en parallele du main.

running = True # Flag principal pour continuer/arreter la simulation.

# Boucle principale de simulation.
while running:    
    
    if not vue.running:     # Si l'utilisateur ferme la fenetre dans le thread affichage, on stoppe ici aussi.
        running = False

    # on protege l'acces aux donnees partagees.
    with lock:
        algogauche.step()
        algodroite.step()
        robotgauche.step(monde)  # On avance la physique du robot de dt secondes.
        robotdroite.step(monde)
        robotgauche.maj_capteurs(monde, robot.vitesse_linaire_actuellement) # On met a jour les capteurs pour le cycle suivant.
        robotdroite.maj_capteurs(monde, robot.vitesse_linaire_actuellement)
    
    time.sleep(1/60)

# Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.running = False
# Puis on attend sa fin pour une fermeture propre.
vue.join(timeout=1.0)

# Ferme pygame proprement.
pygame.quit()
