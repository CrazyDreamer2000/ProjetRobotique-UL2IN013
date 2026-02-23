class AlgoArretDevantObstacle:
    """
    Avance tout droit.
    S'arrête si un obstacle est détecté devant le robot.
    """

    def __init__(self, vitesse_roues=7.0, distance_securite=0.2):
        self.v = float(vitesse_roues)
        self.distance_securite = float(distance_securite)

    def calculer_commande(self, robot, dt, monde):
        if monde.arreter_avant_obstacle(robot.pos, self.distance_securite):
            return 0.0, 0.0
        return self.v, self.v
