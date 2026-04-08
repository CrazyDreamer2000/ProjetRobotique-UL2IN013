import argparse
import math
import time
from threading import RLock

import pygame

import config as cfg
from affichage.Affichage import Affichage
from controle.algo_base import AlgoBase
from controle.composition import Sequence
from controle.primitives import AvancerDistance, TournerAngle
from controle.traducteur import TraducteurSimu
from core.geom import polygone_rectangle_local
from core.robot import Robot
from core.types import Pos2D
from monde.monde import Monde, Obstacle


class AffichageTMESolo(Affichage):
    """Affichage simple: trace active/non active + couleur de trace."""

    def __init__(self, robot, monde, lock):
        super().__init__(robot, monde, lock)
        self.trace_segments = []
        self.trace_last_point = None
   
    def updateAffichage(self):
        with self.lock:
            self.mettre_a_jour_trace()
            self.dessiner_obstacles()
            self.dessiner_trace()
            self.dessiner_robot()

    def mettre_a_jour_trace(self):
        # Ajoute un point seulement si le robot s'est suffisamment deplace
        point = (self.robot.pos.x * cfg.SCALE, self.robot.pos.y * cfg.SCALE)

        if not self.trace_points:
            self.trace_points.append(point)
            return

        last_x, last_y = self.trace_points[-1]
        dx = point[0] - last_x
        dy = point[1] - last_y

        if (dx * dx + dy * dy) ** 0.5 >= self.trace_min_distance_px:
            self.trace_points.append(point)

    def dessiner_trace(self):
        if len(self.trace_points) >= 2:
            pygame.draw.lines(self.screen, COULEURS_TRACE["noir"], False, self.trace_points, 2)


    def reset_affichage(self):
        super().reset_affichage()
        self.trace_segments = []
        self.trace_last_point = None


class Action(AlgoBase):
    """Action instantanee reutilisable dans Sequence."""

    def __init__(self, traducteur, action):
        super().__init__(traducteur)
        self.action = action
        self.done = False

    def start(self):
        self.done = False

    def step(self):
        if self.done:
            return
        self.action()
        self.done = True

    def stop(self):
        return self.done


class Immobile(AlgoBase):
    """Strategie qui garde le robot a l'arret."""

    def start(self):
        pass

    def step(self):
        self.trad.set_vitesse_roues(0.0, 0.0)

    def stop(self):
        return False
    

COULEURS_TRACE = {
    "bleu": (0, 90, 255),
    "vert": (0, 170, 80),
    "rouge": (220, 40, 40),
    "orange": (255, 140, 30),
    "jaune": (235, 190, 30),
    "violet": (140, 80, 210),
    "noir": (20, 20, 20),
}
    
def dessine(robot, b):
    """Active/desactive la trace du robot."""
    robot.trace_active = bool(b)

def change_couleur(robot, couleur):
    """Change la couleur de la trace du robot."""
    robot.trace_couleur = couleur
    return

def _equiper_robot_crayon(robot):
    """Ajoute dessine(bool) et change_couleur(couleur) directement sur robot."""

    robot.trace_active = False
    robot.trace_couleur = (0, 90, 255)
    
def _creer_monde_q1_1():
    """Q1.1: 3 obstacles alignes au milieu (bas, centre, haut)."""

    monde = Monde()
    monde.liste_obstacles.clear()

    x = cfg.LONGUEUR_MONDE / 2
    y_bas = 0.5
    y_centre = cfg.LARGEUR_MONDE / 2
    y_haut = cfg.LARGEUR_MONDE - 0.5

    specs = [
        (x, y_bas, 0.45, 0.25),
        (x, y_centre, 0.40, 0.40),
        (x, y_haut, 0.28, 0.52),
    ]

    for ox, oy, longueur, largeur in specs:
        monde.liste_obstacles.append(
            Obstacle(
                pos=Pos2D(ox, oy, 0.0),
                longueur=longueur,
                largeur=largeur,
                poly_local=polygone_rectangle_local(longueur, largeur),
            )
        )

    return monde

def _creer_robot_coin_bas_gauche():
    robot = Robot(
        cfg.RAYON_ROUE,
        cfg.ECARTEMENT_ROUES,
        ori_initiale="droite",
        x=0.50,
        y=0.50,
    )
    _equiper_robot_crayon(robot)
    return robot


def _simuler(robot, monde, strategie):
    lock = RLock()
    vue = AffichageTMESolo(robot, monde, lock)
    vue.start()

    strategie.start()

    running = True
    while running:
        if not vue.running:
            running = False
            continue

        with lock:
            strategie.step()
            robot.step(monde)

        time.sleep(1 / 60)

    vue.running = False
    vue.join(timeout=1.0)
    pygame.quit()


def _sequence(robot, monde, etapes):
    trad = TraducteurSimu(robot, monde)
    return Sequence(trad, etapes)


def _action(trad, fonction):
    return Action(trad, fonction)


def q1_1():
    monde = _creer_monde_q1_1()
    robot = _creer_robot_coin_bas_gauche()

    trad = TraducteurSimu(robot, monde)
    strategie = Immobile(trad)

    _simuler(robot, monde, strategie)


def q1_2():
    monde = _creer_monde_q1_1()
    robot = _creer_robot_coin_bas_gauche()

    trad = TraducteurSimu(robot, monde)
    etapes: list[AlgoBase] = [
        _action(trad, lambda: dessine(robot, True)),
        _action(trad, lambda: change_couleur(robot, "bleu")),
        AvancerDistance(trad, 0.8, 8.0),
        TournerAngle(trad, math.pi / 2, 8.0, sens="gauche"),
        AvancerDistance(trad, 0.6, 8.0),
    ]

    strategie = _sequence(robot, monde, etapes)
    _simuler(robot, monde, strategie)


def q1_3():
    monde = _creer_monde_q1_1()
    robot = _creer_robot_coin_bas_gauche()

    trad = TraducteurSimu(robot, monde)
    etapes: list[AlgoBase] = [
        _action(trad, lambda: dessine(robot, False)),
        AvancerDistance(trad, 0.35, 8.0),
        _action(trad, lambda: dessine(robot, True)),
        AvancerDistance(trad, 0.45, 8.0),
        TournerAngle(trad, math.pi / 2, 8.0, sens="gauche"),
        _action(trad, lambda: dessine(robot, False)),
        AvancerDistance(trad, 0.30, 8.0),
        _action(trad, lambda: dessine(robot, True)),
        AvancerDistance(trad, 0.30, 8.0),
    ]

    strategie = _sequence(robot, monde, etapes)
    _simuler(robot, monde, strategie)


def q1_4():
    monde = _creer_monde_q1_1()
    robot = _creer_robot_coin_bas_gauche()

    trad = TraducteurSimu(robot, monde)
    etapes: list[AlgoBase] = [
        _action(trad, lambda: dessine(robot, True)),
        _action(trad, lambda: change_couleur(robot, COULEURS_TRACE["bleu"])),
        AvancerDistance(trad, 0.55, 8.0),
        TournerAngle(trad, 2 * math.pi / 3, 8.0, sens="gauche"),
        _action(trad, lambda: change_couleur(robot, COULEURS_TRACE["vert"])),
        AvancerDistance(trad, 0.55, 8.0),
        TournerAngle(trad, 2 * math.pi / 3, 8.0, sens="gauche"),
        _action(trad, lambda: change_couleur(robot, COULEURS_TRACE["rouge"])),
        AvancerDistance(trad, 0.55, 8.0),
    ]

    strategie = _sequence(robot, monde, etapes)
    _simuler(robot, monde, strategie)


def q1_5():
    monde = _creer_monde_q1_1()
    robot = _creer_robot_coin_bas_gauche()

    trad = TraducteurSimu(robot, monde)
    couleurs = ["bleu", "vert", "rouge", "orange", "jaune", "violet"]
    etapes: list[AlgoBase] = [_action(trad, lambda: dessine(robot, True))]
    for couleur in couleurs:
        etapes.append(_action(trad, lambda : change_couleur(robot, couleur)))
        etapes.append(AvancerDistance(trad, 0.45, 8.0))
        etapes.append(TournerAngle(trad, math.pi / 3, 8.0, sens="gauche"))

    strategie = _sequence(robot, monde, etapes)
    _simuler(robot, monde, strategie)

def _build_parser():
    parser = argparse.ArgumentParser(description="Lance les questions du TME solo.")
    parser.add_argument(
        "--question",
        type=str,
        default="1.1",
        choices=["1.1", "1.2", "1.3", "1.4", "1.5"],
        help="Question a lancer (defaut: 1.1)",
    )
    
    return parser


def main():
    args = _build_parser().parse_args()

    mapping = {
        "1.1": q1_1,
        "1.2": q1_2,
        "1.3": q1_3,
        "1.4": q1_4,
        "1.5": q1_5,
    }

    mapping[args.question]()


if __name__ == "__main__":
    main()
