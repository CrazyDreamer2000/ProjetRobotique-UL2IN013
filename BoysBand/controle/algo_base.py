
class AlgoBase:
    """
    Classe de base pour toutes les stratégies / primitives
    """
    def __init__(self, traducteur, name:str, type:str, modeDebug:bool=True):
        # Le traducteur est injecté à l'initialisation.
        self.trad = traducteur
        self.name = name
        self.type = type
        self.modeDebug = modeDebug

    def start(self):
        """
        Initialise ou réinitialise la stratégie et les variables d'instance.
        """
        if self.modeDebug:
            print(f"Start {self.name}  ({self.type})")
        pass

    def step(self):
        """
        Exécute une étape de controle.
        Cette méthode envoie directement les commandes au robot.
        """
        if self.modeDebug:
            print(f"Step {self.name} ({self.type})")

        if self.stop():
            self.trad.set_vitesse_roues(0.0, 0.0)
            return
    
    def stop(self)-> bool:
        """
        Retourne True si la stratégie doit s'arrêter / est terminée, False sinon.
        """
        if self.modeDebug:
            print(f"Check stop {self.name} ({self.type})")
        return False 

    def __str__(self):
        return f"{self.name} ({self.type})"
    
    def __repr__(self):
        return self.__str__()