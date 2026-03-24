# controle/algo_base.py

class AlgoBase:
    """
    Contrat minimal de toute stratégie / controleur
    """
    def __init__(self, traducteur):
        # Le traducteur est injecté à l'initialisation.
        self.trad = traducteur
        self.fini = False

    def start(self):
        """Initialisation avant le premier step"""
        self.fini = False

    def step(self, dt: float):
        """Retourne (vg, vd), vitesses de rotation des roues en rad/s"""
        pass
    
    def stop(self):
        """Commande d'arrêt / nettoyage"""
        self.trad.set_vitesse(0.0, 0.0)