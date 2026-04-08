from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, TournerAngle
from controle.composition import Sequence
import math

class AlgoHexagone(AlgoBase):
    """
    Controleur hexagone du tme solo qui affiche aussi une trace de couleurs différentes
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=0.3):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
        self.longueur_cote = longueur_cote
        self.strategie = None

    def start(self):
        etapes = []

        # Cette partie des algorithmes sera améliorée dans le futur

        self.trad.dessine(True)

        for _ in range(6):
            etapes.append(AvancerDistance(self.trad, self.longueur_cote, self.vitesse))
            etapes.append(TournerAngle(self.trad, 2*math.pi / 6, self.vitesse, sens="gauche"))

        self.strategie = Sequence(self.trad, etapes)
        self.strategie.start()

    def step(self):
        super().step()

        self.strategie.step()
    
    def stop(self):
        return self.strategie.stop()
