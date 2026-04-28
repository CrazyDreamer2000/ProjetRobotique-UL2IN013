import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, ReculerDistance, TournerAngle
from controle.composition import Sequence, Condition, Boucle

class AlgoPolygoneSafe(AlgoBase):
    """
    Polygone + réaction aux collisions
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=500, nb_cotes = 4):
        super().__init__(traducteur, name="PolygoneSafe", type="Strategie")
        self.vitesse = vitesse_roues
        self.nb_cotes = nb_cotes
        self.longueur_cote = longueur_cote
        self.strategie = None
    
    def start(self):
        super().start()
        eviter = Sequence(  self.trad,
                            [ ReculerDistance(self.trad, self.vitesse, 30),
                              TournerAngle(self.trad, self.vitesse, math.pi/3) ]
                         )
        
        polygone = Boucle( self.trad,
                        Sequence( self.trad,
                                  [ AvancerDistance(self.trad, self.vitesse, self.longueur_cote),
                                    TournerAngle(self.trad, self.vitesse, 2*math.pi/self.nb_cotes) ]  ),
                        self.nb_cotes
                         )

        self.strategie = Condition(self.trad,
                                   condition_switch = lambda t: t.est_en_collision(),
                                   si_vrai = eviter,
                                   si_faux = polygone,
                                   condition_stop = lambda: polygone.stop())

        self.strategie.start()
    
    def step(self):
        super().step()
        if self.strategie is not None:
            self.strategie.step()
    
    def stop(self):
        #super().stop()
        if self.strategie is not None:
            return self.strategie.stop()
        return True  # Pas de stratégie donc on considère que c'est fini