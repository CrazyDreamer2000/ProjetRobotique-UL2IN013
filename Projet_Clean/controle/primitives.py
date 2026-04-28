import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class AvancerDistance(AlgoBase):
    """
    Avance en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, vitesse_roues, distance_mm):
        super().__init__(traducteur, name="AvancerDistance", type="Primitive")
        self.vitesse = vitesse_roues
        self.distance_mm = distance_mm
    def start(self):
        super().start()
        print("J'avance de ",self.distance_mm," mm")
        self.trad.reset_distance_parcourue()

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(self.vitesse, self.vitesse)
    
    def stop(self):
        return self.trad.get_distance_parcourue() >= self.distance_mm
    
 
class ReculerDistance(AlgoBase):
    """
    Recule en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, vitesse_roues, distance_mm):
        super().__init__(traducteur, name="ReculerDistance", type="Primitive")
        self.vitesse = vitesse_roues
        self.distance_mm = distance_mm
    
    def start(self):
        super().start()
        self.trad.reset_distance_parcourue()

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(-self.vitesse, -self.vitesse)
    
    def stop(self):
        return self.trad.get_distance_parcourue() >= self.distance_mm


class TournerAngle(AlgoBase):
    """
    Tourne sur place jusqu'à atteindre un angle relatif.
    sens = "gauche" ou "droite"
    """
    def __init__(self, traducteur, vitesse_roues, angle_rad, sens="gauche"):
        super().__init__(traducteur, name="TournerAngle", type="Primitive")
        self.vitesse = vitesse_roues
        self.angle_rad = angle_rad
        self.sens = sens        
    
    def start(self):
        super().start()
        print("Je tourne de",self.angle_rad," radians")
        self.trad.reset_angle_parcouru()

    def step(self):
        super().step()
        
        # ralentissement simple à l'accroche
        angle_restant = self.angle_rad - abs(self.trad.get_angle_parcouru())
        v = self.vitesse * (angle_restant / self.angle_rad)
        v = max(v, 0.5)

        if self.sens == "gauche":
            self.trad.set_vitesse_roues(-v, v)
        else:
            self.trad.set_vitesse_roues(v, -v)
    
    def stop(self):
        return self.trad.get_angle_parcouru() >= self.angle_rad
