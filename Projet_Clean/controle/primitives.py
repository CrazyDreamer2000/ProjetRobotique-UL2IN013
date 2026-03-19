import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class Stop(AlgoBase):
    def __init__(self):
        self.fini = False

    def start(self, robot, monde):
        self.fini = False

    def step(self, robot, monde, dt):
        self.fini = True
        return 0.0, 0.0
    

class AvancerDistance(AlgoBase):
    """
    Avance en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, distance_m, vitesse_roues):
        self.distance_m = distance_m
        self.vitesse = vitesse_roues
        self.fini = False

        self.x_depart = None
        self.y_depart = None
    
    def start(self, robot, monde):
        self.fini = False
        self.x_depart = robot.pos.x
        self.y_depart = robot.pos.y

    def step(self, robot, monde, dt):
        if self.fini:
            return 0.0, 0.0
        
        dx = robot.pos.x - self.x_depart
        dy = robot.pos.y - self.y_depart
        distance = math.hypot(dx, dy)

        if distance >= self.distance_m:
            self.fini = True
            return 0.0, 0.0
        
        return self.vitesse, self.vitesse


class TournerAngle(AlgoBase):
    """
    Tourne sur place jusqu'à atteindre un angle relatif.
    sens = "gauche" ou "droite"
    """
    def __init__(self, angle_rad, vitesse_roues, sens="gauche"):
        self.angle_rad = angle_rad
        self.vitesse = vitesse_roues
        self.sens = sens
        self.fini = False
        
        self.orientation_depart = None
    
    def start(self, robot, monde):
        self.fini = False
        self.orientation_depart = robot.pos.orientation

    def step(self, robot, monde, dt):
        if self.fini:
            return 0.0, 0.0
        
        angle_parcouru = normaliser_angle(robot.pos.orientation - self.orientation_depart)

        if abs(angle_parcouru) >= self.angle_rad:
            self.fini = True
            return 0.0, 0.0
        
        # ralentissement simple à l'accroche
        angle_restant = self.angle_rad - abs(angle_parcouru)
        v = self.vitesse * (angle_restant / self.angle_rad)
        v = max(v, 0.5)

        if self.sens == "gauche":
            return -v, v
        else:
            return v, -v