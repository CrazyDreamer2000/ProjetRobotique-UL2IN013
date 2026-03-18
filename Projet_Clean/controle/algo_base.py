class AlgoBase:
    """
    Contrat minimal de toute stratégie / controleur
    """

    def start(self, robot, monde):
        """Initialisation avant le premier step"""
        pass

    def step(self, robot, monde, dt):
        """Retourne (vg, vd), vitesses de rotation des roues en rad/s"""
        return 0.0, 0.0
    
    def stop(self, robot, monde):
        """Commande d'arrêt / nettoyage"""
        return 0.0, 0.0