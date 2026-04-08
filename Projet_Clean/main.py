import time
import pygame
from parser import parse_args
import config as cfg
from controle import ALGOS
from controle.traducteur import TraducteurSimu
from core.robot import Robot
from monde.monde import Obstacle, Monde
from threading import RLock # RLock = verrou partage entre le thread principal et l'affichage.
from affichage.Affichage import Affichage # Classe du thread qui gere la fenetre et le rendu.

parseArgs = parse_args() # Lit les arguments de la ligne de commande et renvoie un Namespace , un contenuer avec les valeurs lit

robot = Robot(cfg.RAYON_ROUE, cfg.ECARTEMENT_ROUES, parseArgs.orientation, cfg.LONGUEUR_MONDE / 2, cfg.LARGEUR_MONDE / 2)
monde = Monde(robot) 
trad = TraducteurSimu(robot, monde)

algo = ALGOS[parseArgs.algo](trad, 10, 0.5) # Algo choisi par defaut dans code actuel.
algo.start()

lock = RLock() # Verrou partage entre simulation (main) et rendu (thread affichage).
vue = Affichage(robot, monde, lock) # On cree l'affichage en lui donnant robot/monde/lock.
vue.start() # Demarre le thread d'affichage en parallele du main.

running = True 

while running:    
    
    if not vue.running:   # Si l'utilisateur ferme la fenetre dans le thread affichage, on stoppe ici aussi.
        running = False

    # on protege l'acces aux donnees partagees.
    with lock:
        algo.step()
        monde.step()  # On avance la physique du robot de dt secondes.
    
    time.sleep(1/60)

vue.running = False # Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.join(timeout=1.0) # Puis on attend sa fin pour une fermeture propre.

pygame.quit()
