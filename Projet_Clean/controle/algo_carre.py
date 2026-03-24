import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, TournerAngle
from controle.composition import Sequence


class AlgoCarre(AlgoBase):
    """
    Controleur carré construit à partir de primitives réutilisables
    """
    def __init__(self, vitesse_roues, longueur_cote=0.5):
        self.vitesse = vitesse_roues
        self.longueur_cote = longueur_cote
        self.strategie = None

    def start(self, robot, monde):
        etapes = []

        for _ in range(4):
            etapes.append(AvancerDistance(self.longueur_cote, self.vitesse))
            etapes.append(TournerAngle(math.pi / 2, self.vitesse, sens="gauche"))

        self.strategie = Sequence(etapes)
        self.strategie.start(robot, monde)

    def step(self, robot, monde, dt):
        return self.strategie.step(robot, monde, dt)
    
    def stop(self, robot, monde):
        return 0.0, 0.0
