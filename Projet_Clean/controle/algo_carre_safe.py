from controle.algo_base import AlgoBase
from controle.algo_carre import AlgoCarre
from controle.primitives import ReculerDistance, TournerAngle
from controle.composition import Sequence, Condition
from controle.primitives import ReculerDistance, TournerAngle
import math

class AlgoCarreSafe(AlgoBase):
    """
    Carré + réaction aux collisions
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=0.5):
        super().__init__(traducteur, name="CarreSafe", type="Strategie")
        self.vitesse = vitesse_roues
        self.strategie = None
    
    def start(self):

        eviter = Sequence(self.trad, [ReculerDistance(self.trad, self.vitesse, 0.3), TournerAngle(self.trad, self.vitesse, math.pi/3)])
        carre = AlgoCarre(self.trad, self.vitesse)

        self.strategie = Condition(self.trad,
                                   condition_switch = lambda t: t.est_en_collision(),
                                   si_vrai = eviter,
                                   si_faux = carre,
                                   condition_stop = lambda: carre.stop())

        self.strategie.start()
    
    def step(self):
        super().step()
        if self.strategie is not None:
            self.strategie.step()
    
    def stop(self):
        if self.strategie is not None:
            return self.strategie.stop()
        return True  # Pas de stratégie donc on considère que c'est fini