from controle.algo_base import AlgoBase

class Sequence(AlgoBase):
    """
    Exécute plusieurs stratégies/primitives l'une après l'autre
    """
    def __init__(self, traducteur, etapes, dt=0.05):
        super().__init__(traducteur)
        self.etapes = etapes
        self.index = 0
        self.dt = dt

    def start(self):
        self.index = 0

        if len(self.etapes) > 0:
            self.etapes[0].start()
    
    def step(self):
        if self.stop():
            return

        self.etapes[self.index].step()

        if self.etapes[self.index].stop():
            self.index += 1
            if not self.stop():
                self.etapes[self.index].start()
        
    def stop(self):        
        return self.index >= len(self.etapes)


class InterruptionCollision(AlgoBase):
    """
    Exécute la stratégie normale.
    Si collision, lance une stratégie d'évitement et la garde jusqu'à ce qu'elle soit terminée
    """

    def __init__(self, traducteur, strategie_normale, strategie_collision):
        super().__init__(traducteur)
        self.normale = strategie_normale
        self.collision = strategie_collision
        self.mode = "normal"

    def start(self):
        self.mode = "normal"
        self.normale.start()

    def step(self):
        super().step()

        if self.mode == "normal":
            if self.trad.est_en_collision():
                self.mode = "collision"
                self.collision.start()
                self.collision.step()

            self.normale.step()

        elif self.mode == "collision":
            if self.collision.stop():
                self.mode = "normal"
                self.normale.start()
                self.normale.step()

            self.collision.step()

    def stop(self):
        return False