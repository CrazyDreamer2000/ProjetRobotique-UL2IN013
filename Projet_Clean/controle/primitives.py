import math
from controle.algo_base import AlgoBase
from core.geom import normaliser_angle


class Stop(AlgoBase):
    """
    Arrête l'algorithme
    """
    def __init__(self, traducteur):
        super().__init__(traducteur)
    
    def start(self):
        return
    
    def step(self):
        self.trad.set_vitesse_roues(0.0, 0.0)
    
    def stop():
        return False


class Avancer(AlgoBase):
    """
    Avance indéfiniment
    """
    def __init__(self, traducteur, vitesse_roues):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
    
    def start(self):
        print("J'avance")
        return

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(self.vitesse, self.vitesse)
    
    def stop(self):
        return False


class AvancerDistance(AlgoBase):
    """
    Avance en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, vitesse_roues, distance_cm):
        super().__init__(traducteur)
        self.vitesse = vitesse_roues
        self.distance_cm = distance_cm
    
    def start(self):
        print("J'avance de ",self.distance_cm," cm")
        self.trad.reset_distance_parcourue()

    def step(self):
        super().step()
        self.trad.set_vitesse_roues(self.vitesse, self.vitesse)
    
    def stop(self):
        return self.trad.get_distance_parcourue() >= self.distance_cm
    

class AvancerProche(AlgoBase):
    def __init__(self, traducteur, vitesse_max, dist_securite = 150):
        super().__init__(traducteur)
        self.vitesse_max = vitesse_max
        self.dist_securite = dist_securite # Distance du mur à partir duquel on ralentit
        self.min_securite = 30 # Distance minimale du mur à tout moment
        self.vitesse = 0
   
    def start(self):
        print("Je m'approche")
        self.vitesse = 0

    def step(self):
        if self.stop():
            self.trad.set_vitesse_roues(0.0, 0.0)
            return

        dist_devant = self.trad.get_distance_devant() # sécurité
        if dist_devant > self.dist_securite: # pas aller trop vite
            dist_devant = self.dist_securite
        if dist_devant < self.min_securite: # pas aller trop lentement
            dist_devant = 0

        self.vitesse = (dist_devant / self.dist_securite) * self.vitesse_max
        print(self.vitesse)
        self.trad.set_vitesse_roues(self.vitesse, self.vitesse)

    
    def stop(self):
        return self.trad.get_distance_devant() < self.min_securite


class ReculerDistance(AlgoBase):
    """
    Recule en ligne droite jusqu'à avoir parcouru une distance donnée
    """
    def __init__(self, traducteur, vitesse_roues, distance_m):
        super().__init__(traducteur)
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
        super().__init__(traducteur)
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
