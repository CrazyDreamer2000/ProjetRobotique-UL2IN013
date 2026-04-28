import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, TournerAngle
from controle.composition import Sequence, Boucle


class AlgoCarre(AlgoBase):
    """
    Controleur carré construit à partir de primitives réutilisables
    """
    def __init__(self, traducteur, vitesse_roues, longueur_cote=0.5):
        super().__init__(traducteur, name="Carre", type="Strategie")
        self.vitesse = vitesse_roues
        self.longueur_cote = longueur_cote
        self.strategie = None

    def start(self):
        super().start()

        etapes = [
                    AvancerDistance(self.trad, self.vitesse, self.longueur_cote),
                    TournerAngle(self.trad, self.vitesse, math.pi / 2)
                 ]
        
        self.strategie = Boucle(self.trad, Sequence(self.trad, etapes), 4)
        self.strategie.start()

    def step(self):
        super().step()
        if self.strategie is not None:
            self.strategie.step()
    
    def stop(self):
        if self.strategie is not None:
            return self.strategie.stop()
        return True  # Pas de stratégie donc on considère que c'est fini
