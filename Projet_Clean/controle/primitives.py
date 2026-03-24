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
        self.x_depart = None
        self.y_depart = None
    
    def start(self):
        super().start()
        pos = self.trad.get_position()
        self.x_depart = pos.x
        self.y_depart = pos.y

    def step(self):
        if self.stop():
            self.trad.set_vitesse(0.0, 0.0)

        self.trad.set_vitesse(self.vitesse, self.vitesse)
    
    def stop(self):
        if self.fini:
            return True
        
        pos = self.trad.get_position()
        dx = pos.x - self.x_depart
        dy = pos.y - self.y_depart
        distance = math.hypot(dx, dy)

        if distance >= self.distance_m:
            self.fini = True
        
        return self.fini

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
        self.orientation_depart = None
    
    def start(self):
        super().start()
        pos = self.trad.get_position()
        self.orientation_depart = pos.orientation

    def step(self):
        if self.stop():
            self.trad.set_vitesse(0.0, 0.0)
        
        pos = self.trad.get_position()
        angle_parcouru = normaliser_angle(pos.orientation - self.orientation_depart)
        
        # ralentissement simple à l'accroche
        angle_restant = self.angle_rad - abs(angle_parcouru)
        v = self.vitesse * (angle_restant / self.angle_rad)
        v = max(v, 0.5)

        if self.sens == "gauche":
            self.trad.set_vitesse(-v, v)
        else:
            self.trad.set_vitesse(v, -v)
    
    def stop(self):
        if self.fini:
            return True

        pos = self.trad.get_position()
        angle_parcouru = normaliser_angle(pos.orientation - self.orientation_depart)
        if abs(angle_parcouru) >= self.angle_rad:
            self.fini = True

        return self.fini

        
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
        super().start()
        self.timer = 0.0
        self.phase = "recule"
    
    def step(self):
        if self.stop():
            self.trad.set_vitesse(0.0, 0.0)

        self.timer += self.dt

        if self.phase == "recule":
            if self.timer > 1:
                self.phase = "tourne"
                self.timer = 0.0
            self.trad.set_vitesse(-self.v, -self.v)
        
        elif self.phase == "tourne":
            if self.stop():
                self.trad.set_vitesse(0.0, 0.0)
            self.trad.set_vitesse(-0.5*self.v, 0.5*self.v)
            
    def stop(self):
        if self.fini:
            return True

        if self.phase == "tourne" and self.timer > 1:
            self.fini = True
        
        return self.fini
