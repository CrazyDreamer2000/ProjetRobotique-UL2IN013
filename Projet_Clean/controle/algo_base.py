# controle/algo_base.py

class AlgoBase:
    """
    Classe de base pour toutes les stratégies / primitives
    """
    def __init__(self, traducteur):
        # Le traducteur est injecté à l'initialisation.
        self.trad = traducteur
        self.fini = False

    def start(self):
        """
        Initialise ou réinitialise la stratégie
        """
        self.fini = False

    def step(self):
        """
        Exécute une étape de controle.
        Cette méthode envoie directement les commandes au robot.
        """
        pass
    
    def stop(self):
        """
        Retourne True si la stratégie doit s'arrêter / est terminée, False sinon (?)
        """
        return self.fini