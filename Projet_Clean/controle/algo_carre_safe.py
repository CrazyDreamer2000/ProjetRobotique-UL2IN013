from controle.algo_base import AlgoBase
from controle.algo_carre import AlgoCarre
from controle.primitives import EviterCollision
from controle.composition import InterruptionCollision


class AlgoCarreSafe(AlgoBase):
    """
    Carré + réaction aux collisions
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=0.5):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
        self.strategie = None
    
    def start(self):
        carre = AlgoCarre(self.trad, self.vitesse)
        eviter = EviterCollision(self.trad, self.vitesse)

        self.strategie = InterruptionCollision(self.trad, carre, eviter)

        self.strategie.start()
    
    def step(self):
        super().step()
        self.strategie.step()
    
    def stop(self):
        return self.strategie.stop()