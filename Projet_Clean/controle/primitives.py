import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class AvancerDistance(AlgoBase):
    """
    Avance en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, vitesse_roues, distance_cm):
        super().__init__(traducteur, name="AvancerDistance", type="Primitive")
        self.vitesse = vitesse_roues
        self.distance_cm = distance_cm
        #Pourquoi on utilise distance cm ?
        # a changer en metre plus tard pour etre cohérent avec les autres primitives et la simulation
    def start(self):
        print("J'avance de ",self.distance_cm," cm")
        self.trad.reset_distance_parcourue()

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(self.vitesse, self.vitesse)
    
    def stop(self):
        return self.trad.get_distance_parcourue() >= self.distance_cm
    
 
class ReculerDistance(AlgoBase):
    """
    Recule en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, vitesse_roues, distance_m):
        super().__init__(traducteur, name="ReculerDistance", type="Primitive")
        self.vitesse = vitesse_roues
        self.distance_m = distance_m
    
    def start(self):
        self.trad.reset_distance_parcourue()

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(-self.vitesse, -self.vitesse)
    
    def stop(self):
        return self.trad.get_distance_parcourue() >= self.distance_m


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
