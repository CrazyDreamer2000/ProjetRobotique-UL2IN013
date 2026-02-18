import math

def normaliser_angle(angle):
    """Ramène un angle dans [-pi, pi]"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

class AlgoAvancer:
    """
    Avance tout droit
    """
    def __init__(self, vitesse_roues):
        self.v = vitesse_roues

    def calculer_commande(self, robot, dt):
        return self.v, self.v
