from controle.algo_base import AlgoBase
from controle.algo_carre import AlgoCarre
from controle.primitives import EviterCollision
from controle.composition import Condition


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
                                   si_vrai = EviterCollision(self.trad, self.vitesse),
                                   si_faux = AlgoCarre(self.trad, self.vitesse))
        #self.strategie = InterruptionCollision(self.trad, AlgoCarre(self.trad, self.vitesse), EviterCollision(self.trad, self.vitesse))
        self.strategie.start()
    
    def step(self):
        super().step()
        self.strategie.step()
    
    def stop(self):
        return self.strategie.stop()