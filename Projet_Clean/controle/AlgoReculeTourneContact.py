class AlgoReculeTourneContact:
    """
    robot avance tout droit.
    Si le robot touche un obstacle : dabord recule un peu , puis tourne sur place repart en avant , continue son chemin
    """

    def __init__(self, vitesse_roues=7.0, temps_recule=0.8, temps_tourne=0.6, sens="gauche"):
        self.v = float(vitesse_roues)
        self.temps_recule = float(temps_recule)
        self.temps_tourne = float(temps_tourne)
        self.sens = sens

        self.etat = "avance"
        self.timer = 0.0

    def calculer_commande(self, robot, dt, monde):
        if self.etat == "avance" and robot.en_collision:
            self.etat = "recule"
            self.timer = self.temps_recule

        if self.etat == "recule":
            self.timer -= dt
            if self.timer <= 0:
                self.etat = "tourne"
                self.timer = self.temps_tourne
            return -self.v, -self.v

        if self.etat == "tourne":
            self.timer -= dt
            if self.timer <= 0:
                self.etat = "avance"
                return 0.0, 0.0

            if self.sens == "gauche":
                return -self.v, self.v
            return self.v, -self.v

        return self.v, self.v
