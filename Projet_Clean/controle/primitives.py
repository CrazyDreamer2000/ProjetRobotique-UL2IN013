import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class Stop(AlgoBase):
    def __init__(self,traducteur):
        super().__init__(traducteur)

    def start(self, robot, monde):
        self.fini = False

    def step(self, robot, monde, dt):
        self.fini = True
        self.trad.set_vitesse(0.0, 0.0)
    

class AvancerDistance(AlgoBase):
    """
    Avance en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, distance_m, vitesse_roues):
        super().__init__(traducteur)
        self.distance_m = distance_m
        self.vitesse = vitesse_roues
        self.fini = False

        self.x_depart = None
        self.y_depart = None
    
    def start(self, robot, monde):
        self.fini = False
        pos = self.trad.get_position()
        self.x_depart = robot.pos.x
        self.y_depart = robot.pos.y

    def step(self, robot, monde, dt):
        if self.fini:
            self.trad.set_vitesse(0.0, 0.0)
            return 
        
        pos_actuelle = self.trad.get_position()
        dx = robot.pos.x - self.x_depart
        dy = robot.pos.y - self.y_depart
        distance = math.hypot(dx, dy)

        if distance >= self.distance_m:
            self.fini = True
            self.trad.set_vitesse(0.0, 0.0)
        else:
            self.trad.set_vitesse(self.vitesse, self.vitesse)


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
        self.fini = False
        
        self.orientation_depart = None
    
    def start(self, robot, monde):
        self.fini = False
        pos = self.trad.get_position()
        self.orientation_depart = pos.orientation

    def step(self, robot, monde, dt):
        if self.fini:
            self.trad.set_vitesse(0.0, 0.0)
            return 
        
        pos_actuelle = self.trad.get_position()
        angle_parcouru = normaliser_angle(pos_actuelle.orientation - self.orientation_depart)

        if abs(angle_parcouru) >= self.angle_rad:
            self.fini = True
            self.trad.set_vitesse(0.0, 0.0)
        
        # ralentissement simple à l'accroche
        angle_restant = self.angle_rad - abs(angle_parcouru)
        v = self.vitesse * (angle_restant / self.angle_rad)
        v = max(v, 0.5)

        if self.sens == "gauche":
            self.trad.set_vitesse(-v, v)
        else:
            self.trad.set_vitesse(v, -v)