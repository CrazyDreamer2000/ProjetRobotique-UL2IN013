import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, ReculerDistance, TournerAngle
from controle.composition import Sequence, Condition, Boucle


class AlgoSuivreBaliseDistance(AlgoBase):
    """
    Test pas fonctionnel: suivre une balise avec le robot réel en évitant les collisions
    Distance entre robot et balise: 500mm
    Suivre une balise avec le robot réel en évitant les collisions
    """
    def __init__(self, traducteur,vitesse_roues=3.0):
        super().__init__(traducteur, name="SuivreBaliseDistance", type="Strategie")
        self.trad = traducteur
        self.vitesse = vitesse_roues
        self.distance_cible = 500  # Distance cible en mm
        self.margesafe_mm = 100  # Marge de sécurité pour éviter les collisions
        self.strategie = None
        self.recherche = False # pour savoir si on recherche activement balise ou on la suit deja
        
    
    def start(self):
        super().start()
        eviter = Sequence(self.trad,
                            [ ReculerDistance(self.trad, self.vitesse, 30),
                              TournerAngle(self.trad, self.vitesse, math.pi/3) ])
        suivre_balise = Sequence(self.trad,
                                [ AvancerDistance(self.trad, self.vitesse, self.distance_cible) ] )
        self.strategie = Condition(self.trad,
                                   condition = lambda t: t.est_en_collision(),
                                   si_vrai = eviter,
                                   si_faux = suivre_balise)

    def step(self):
        super().step()
        distance = self.trad.get_distance_devant() # on recupere la distance devant le robot (capteur de distance) float
        if distance < self.margesafe_mm:
            

        if self.strategie is not None:
            self.strategie.step()

    def stop(self):
        super().stop()
