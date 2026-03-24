from controle.algo_base import AlgoBase
from controle.algo_carre import AlgoCarre
from controle.primitives import EviterCollision
from controle.composition import InterruptionCollision


class AlgoCarreSafe(AlgoBase):
    """
    Carré + réaction aux collisions
    """
    def __init__(self, vitesse_roues, longueur_cote=0.5):
        self.vitesse = vitesse_roues
        self.strategie = None
    
    def start(self, robot, monde):
        carre = AlgoCarre(self.vitesse)
        eviter = EviterCollision(self.vitesse)

        self.strategie = InterruptionCollision(carre, eviter)

        self.strategie.start(robot, monde)
    
    def step(self, robot, monde, dt):
        return self.strategie.step(robot, monde, dt)
    
    def stop(self, robot, monde):
        return 0.0, 0.0