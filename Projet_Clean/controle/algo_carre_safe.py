from controle.algo_base import AlgoBase
from controle.algo_carre import AlgoCarre
from controle.composition import Sequence, Condition


class AlgoCarreSafe(AlgoBase):
    """
    Carré + réaction aux collisions
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=0.5):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
        self.strategie = None
    
    def start(self):

        self.strategie = Condition(self.trad,
                                   condition = lambda t: t.est_en_collision(),
                                   si_vrai = Sequence(self.trad, [ReculerDistance(self.trad, self.vitesse, 0.3), TournerAngle(self.trad, self.vitesse, math.pi/3)]),
                                   si_faux = AlgoCarre(self.trad, self.vitesse))

        self.strategie.start()
    
    def step(self):
        super().step()
        self.strategie.step()
    
    def stop(self):
        return self.strategie.stop()