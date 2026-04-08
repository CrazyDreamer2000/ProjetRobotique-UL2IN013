import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class AvancerDistance(AlgoBase):
    """
    Avance en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, distance_m, vitesse_roues):
        super().__init__(traducteur)
        self.distance_m = distance_m
        self.vitesse = vitesse_roues
    
    def start(self):
        self.trad.reset_distance_parcourue()

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(self.vitesse, self.vitesse)
    
    def stop(self):
        return self.trad.get_distance_parcourue() >= self.distance_m


class TournerAngle(AlgoBase):
    """
    Tourne sur place jusqu'à atteindre un angle relatif.
    sens = "gauche" ou "droite"
    """
    def __init__(self, traducteur, angle_rad, vitesse_roues, sens="gauche"):
        super().__init__(traducteur)
        self.angle_rad = angle_rad
        self.vitesse = vitesse_roues
        self.sens = sens        
    
    def start(self):
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
        return abs(self.trad.get_angle_parcouru()) >= self.angle_rad

        
class EviterCollision(AlgoBase):
    """
    Réagit à une collision:
    - recule
    - tourne
    """
    def __init__(self, traducteur, vitesse, dt = 0.05):
        super().__init__(traducteur)
        self.v = vitesse
        self.timer = 0.0
        self.phase = "recule"
        self.dt = dt

    def start(self):
        self.timer = 0.0
        self.phase = "recule"
    
    def step(self):
        if self.stop():
            self.trad.set_vitesse_roues(0.0, 0.0)

        self.timer += self.dt

        if self.phase == "recule":
            if self.timer > 1:
                self.phase = "tourne"
                self.timer = 0.0
            self.trad.set_vitesse_roues(-self.v, -self.v)
        
        elif self.phase == "tourne":
            if self.stop():
                self.trad.set_vitesse_roues(0.0, 0.0)
            self.trad.set_vitesse_roues(-0.5*self.v, 0.5*self.v)
            
    def stop(self):
        return self.phase == "tourne" and self.timer > 1