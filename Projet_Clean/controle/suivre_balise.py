import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, ReculerDistance, TournerAngle
from controle.composition import Sequence, Condition, Boucle

class AlgoSuivreBalise(AlgoBase):
    """
    Suivre une balise avec le robot réel en évitant les collisions
    """
    def __init__(self, traducteur):
        super().__init__(traducteur, name="SuivreBalise", type="Strategie")
        
    
    def start(self):
        super().start()
        
    def step(self):
        super().step()
    
    def stop(self):
        super().stop()
