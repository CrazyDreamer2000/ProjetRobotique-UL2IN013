class AlgoEviter:
    """
    Algo temporaire:
    - avance tout droit
    - si collision: recule pendant T_recule
    - puis tourne sur place pendant T_tourne
    """

    def __init__(
        self,
        vitesse_roues: float,
        temps_recule_s: float = 1.0,
        temps_tourne_s: float = 0.5,
        sens: str = "gauche",
    ):
        self.v = float(vitesse_roues)
        self.T_recule = float(temps_recule_s)
        self.T_tourne = float(temps_tourne_s)
        self.sens = sens

        self.etat = "avance"
        self.timer = 0.0

    def calculer_commande(self, robot, dt):
        # Detection collision -> declenchement evitement
        if self.etat == "avance" and robot.en_collision:
            self.etat = "recule"
            self.timer = self.T_recule

        if self.etat == "recule":
            self.timer -= dt
            if self.timer <= 0:
                self.etat = "tourne"
                self.timer = self.T_tourne
            return -self.v, -self.v

        if self.etat == "tourne":
            self.timer -= dt
            if self.timer <= 0:
                self.etat = "avance"
                return 0.0, 0.0

            if self.sens == "gauche":
                return -self.v, self.v
            else:
                return self.v, -self.v

        # avance
        return self.v, self.v
