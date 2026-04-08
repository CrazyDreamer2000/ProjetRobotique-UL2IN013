from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, TournerAngle
from controle.composition import Sequence
import math

class AlgoAllerRetour(AlgoBase):
    """
    Controleur hexagone du tme solo qui affiche aussi une trace de couleurs différentes
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=1):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
        self.longueur_cote = longueur_cote
        self.strategie = None

    def start(self):
        etapes = []

        self.trad.dessine(True)

        etapes.append(AvancerDistance(self.trad, self.longueur_cote, self.vitesse))
        etapes.append(TournerAngle(self.trad, math.pi-0.001, self.vitesse, sens="gauche"))
        etapes.append(AvancerDistance(self.trad, self.longueur_cote, self.vitesse))

        self.strategie = Sequence(self.trad, etapes)
        self.strategie.start()

    def step(self):
        super().step()

        self.strategie.step()
    
    def stop(self):
        return self.strategie.stop()
