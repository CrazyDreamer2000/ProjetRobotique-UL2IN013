import time
from parser import parse_args
import config as cfg
from controle import ALGOS

Simu = False

monde = None
trad = None

parseArgs = parse_args() # Lit les arguments de la ligne de commande et renvoie un Namespace , un contenuer avec les valeurs lit

if Simu:
    from monde.monde import Monde
    from threading import RLock # RLock = verrou partage entre le thread principal et l'affichage.
    from affichage.Affichage import Affichage # Classe du thread qui gere la fenetre et le rendu.
    from traducteur import TraducteurSimu

    monde = Monde() 
    trad = TraducteurSimu(monde)

    lock = RLock() # Verrou partage entre simulation (main) et rendu (thread affichage).
    vue = Affichage(monde, lock) # On cree l'affichage en lui donnant robot/monde/lock.
    vue.start() # Demarre le thread d'affichage en parallele du main.

else:
    from robot2I013.robot2I013 import Robot2IN013
    from traducteur import TraducteurReel
    robot = Robot2IN013()
    trad = TraducteurReel(robot)

algo = ALGOS[parseArgs.algo](trad, 2.0, 500) # Algo choisi par defaut dans code actuel.

algo.start()

running = True 

while running:    
    
    if Simu:
        if not vue.running:   # Si l'utilisateur ferme la fenetre dans le thread affichage, on stoppe ici aussi.
            running = False

        with lock:  # on protege l'acces aux donnees partagees.
            algo.step()
            monde.step()  # On avance la physique du robot de dt secondes.
    else:
        algo.step()

    time.sleep(1/60)

vue.stop()  # Fin de boucle: on demande au thread d'affichage de s'arreter.
vue.join(timeout=1.0) # Puis on attend sa fin pour une fermeture propre.
