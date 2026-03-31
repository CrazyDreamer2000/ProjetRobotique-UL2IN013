# controle/algo_base.py

class AlgoBase:
    """
    Classe de base pour toutes les stratégies / primitives
    """
    def __init__(self, traducteur):
        # Le traducteur est injecté à l'initialisation.
        self.trad = traducteur

    def start(self):
        """
        Initialise ou réinitialise la stratégie
        """
        pass

    def step(self):
        """
        Exécute une étape de controle.
        Cette méthode envoie directement les commandes au robot.
        """
        if self.stop():
            self.trad.set_vitesse_roues(0.0, 0.0)
            return
    
    def stop(self):
        """
        Retourne True si la stratégie doit s'arrêter / est terminée, False sinon (?)
        """
        pass