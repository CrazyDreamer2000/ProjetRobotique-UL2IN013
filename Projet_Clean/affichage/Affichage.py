# SIMULATION

import pygame
import config as cfg
import threading
from core.geom import transformer_point_local_vers_monde, transformer_polygone_local_vers_monde
import time

class Affichage(threading.Thread):
    # Ici on prepare notre thread d'affichage.
    # En gros: on recupere le robot, le monde et le lock pour pouvoir dessiner ce qu'il se passe sans se battre avec le thread principal.
    def __init__(self, robot, monde, lock):
        super().__init__()
        self.robot = robot
        self.monde = monde
        self.running = True
        self.fps = 60
        # On laisse le thread en non-daemon pour pouvoir faire un arret propre
        # avec join() dans le main.
        self.daemon = False
        self.lock = lock

    # Cette methode est executee automatiquement quand on fait vue.start().
    # Elle cree la fenetre puis lance la boucle qui tourne en continu.
    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.LONGUEUR_MONDE * cfg.SCALE, cfg.LARGEUR_MONDE * cfg.SCALE))

        while self.running:
            # A chaque tour, on fait une frame complete.
            self.update()
            # Petite pause pour garder un rythme stable et eviter de saturer le CPU.
            time.sleep(1.0 / self.fps)

        pygame.quit()
        
    def stop(self):
        self.running = False

    # ici on lit les actions utilisateur et on desine dessiner a l'ecran et on update 
    def update(self):
        self.gerer_evenements()
        self.dessiner_frame()


    #=========== GESTION DES EVENTS : ACTIONS DE UTILISATEUR==================

    # Gestion des evenements : ici on regarde ce que l'utilisateur fait:
    # - fermer la fenetre
    # - cliquer pour ajouter un obstacle
    # - appuyer sur R pour reset
    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Stop propre de la boucle d'affichage
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                # On verrouille avant de modifier le monde partage.
                # Comme ca, pas de conflit avec le thread principal.
                with self.lock:
                    self.monde.ajouter_obstacle(x, y)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset visuel rapide pour repartir proprement.
                self.reset_affichage()


    # Cette methode fait le rendu de la frame en zone protegee:
    # on prend le lock pour eviter que le thread principal modifie robot/monde pendant qu'on est en train de dessiner.

    def updateAffichage(self):   # elle gère quoi dessiner, avec protection lock
        with self.lock:
            self.dessiner_robot()
            self.dessiner_obstacles() 

    # Cette methode dessine tout ce qu'on veut voir sur la fenetre.
    def dessiner_frame(self):    #elle gère le cycle pygame (clear -> draw -> show) 
        
        self.screen.fill((240, 240, 240))        # On efface l'ancienne image
        self.updateAffichage()        # Puis on redessine scene complete
        pygame.display.flip()         # Et on affiche le nouveau resultat

    #========== RESET DE LA CARTE ==========================

    # Quand on appuie sur R:
    # - robot revient au centre
    # - orientation remise a zero
    # - obstacles regeneres
    # Tout est sous lock pour eviter les soucis de concurrence.

    def reset_affichage(self):
        """Reset visuel: robot au centre + nouveaux obstacles."""
        with self.lock:
            self.robot.pos.x = cfg.LONGUEUR_MONDE / 2
            self.robot.pos.y = cfg.LARGEUR_MONDE / 2
            self.robot.pos.orientation = 0.0
            self.robot.en_collision = False
            self.monde.liste_obstacles.clear()
            self.monde.creer_obstacles_aleatoires()


    #===============FONCTIONS DE DESSINS===================

    # Dessin du robot:
    # - on lit les donnees sous lock
    # - on dessine ensuite hors lock
    # Cette separation garde le lock le moins longtemps possible.
    def dessiner_robot(self):
            # Points du robot transformes en coordonnees ecran
        points_monde = [
            (x * cfg.SCALE, y * cfg.SCALE)
            for x, y in transformer_polygone_local_vers_monde(self.monde.poly_robot_local, self.robot.pos)
            ]

            # Centre du robot + orientation actuelle
        cx, cy = self.robot.pos.x * cfg.SCALE, self.robot.pos.y * cfg.SCALE
        ori = self.robot.pos.orientation

        # Corps du robot
        pygame.draw.polygon(self.screen, (80, 130, 200), points_monde)

        # Petite fleche rouge pour montrer la direction du robot
        longueur = max(px for px, _ in self.monde.poly_robot_local) * cfg.SCALE
        cible = transformer_point_local_vers_monde(longueur, 0, cx, cy, ori)
        pygame.draw.line(self.screen, (255, 0, 0), (cx, cy), cible, 2)

    # Dessin des obstacles:
    def dessiner_obstacles(self):

        obstacles = self.monde.liste_obstacles

        for obs in obstacles:
            # On convertit le polygone obstacle en coordonnees ecran
            points = [
                (x * cfg.SCALE, y * cfg.SCALE)
                for x, y in transformer_polygone_local_vers_monde(obs.poly_local, obs.pos)
            ]
            # Puis on dessine l'obstacle
            pygame.draw.polygon(self.screen, cfg.COULEUR_OBSTACLE, points)
