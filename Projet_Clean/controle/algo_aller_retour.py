
import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class AlgoAllerRetour(AlgoBase):
    """ Q2.2 """
    def __init__(self, traducteur, vitesse):
        super().__init__(traducteur)
        self.v = vitesse
        self.phase = "haut"
        self.start_y = 0.0

    def start(self):
        self.trad.reset_distance_parcourue()
        self.phase = "haut"

    def step(self):
        
        dist = abs(self.trad.get_distance_parcourue())
        
        if dist > 1.0: 
            self.trad.reset_distance_parcourue()
          
            self.v = -self.v 
            
        self.trad.set_vitesse_roues(self.v, self.v)

    def stop(self):
        return False 