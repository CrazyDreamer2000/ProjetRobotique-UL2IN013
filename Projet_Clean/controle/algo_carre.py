import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, TournerAngle
from controle.composition import Sequence


class AlgoCarre(AlgoBase):
    """
    Controleur carré construit à partir de primitives réutilisables
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=0.5):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
        self.longueur_cote = longueur_cote
        self.strategie = None

    def start(self):
        super().start()

        etapes = []
        for _ in range(4):
            etapes.append(AvancerDistance(self.trad, self.longueur_cote, self.vitesse))
            etapes.append(TournerAngle(self.trad, math.pi / 2, self.vitesse, sens="gauche"))

        self.strategie = Sequence(self.trad, etapes)
        self.strategie.start()

    def step(self):
        if self.stop():
            self.trad.set_vitesse(0.0, 0.0)

        self.strategie.step()
    
    def stop(self):
        if self.fini:
            return True
        self.fini = self.strategie.stop()
        return self.fini
