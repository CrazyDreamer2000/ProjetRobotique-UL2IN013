import math
from controle.algo_base import AlgoBase
from controle.primitives import Avancer, AvancerProche, Stop
from controle.composition import Condition

class AlgoFoncerDevant(AlgoBase):
    """
    Polygone + réaction aux collisions
    """
    def __init__(self, trad, vitesse_max, dist_securite = 300):
        super().__init__(trad, name="FoncerDevant", type="Algorithme")
        self.vitesse_max = vitesse_max
        self.dist_securite = dist_securite
        self.strategie = None
    
    def start(self):
        super().start()
        
        avancerproche = AvancerProche(self.trad, self.vitesse_max)
        avancer = Avancer(self.trad, self.vitesse_max)
        self.strategie = Condition( self.trad,
                                    condition_switch = lambda t: (t.get_distance_devant() < self.dist_securite),
                                    si_vrai = avancerproche,
                                    si_faux = avancer,
                                    condition_stop = lambda: avancerproche.stop() )
        self.strategie.start()
        

    def step(self):
        if self.stop():
            self.strategie = Stop(self.trad)
            self.strategie.start()

        self.strategie.step()
    
    def stop(self):
        return self.strategie.stop()
