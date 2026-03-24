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
        super().start()
        self.index = 0

        if len(self.etapes) == 0:
            self.fini = True
        else:
            self.etapes[0].start()
    
    def step(self):
        if self.stop():
            self.trad.set_vitesse(0.0, 0.0)
        
        etape = self.etapes[self.index]
        etape.step()

        if etape.stop():
            self.index += 1

            if self.stop():
                self.trad.set_vitesse(0.0, 0.0)
            
            self.etapes[self.index].start()
        
    def stop(self):
        if self.fini:
            return True
        
        if self.index >= len(self.etapes):
            self.fini = True
        
        return self.fini


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
        super().start()
        self.mode = "normal"
        self.normale.start()

    def step(self):
        if self.stop():
            self.trad.set_vitesse(0.0, 0.0)

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
        if self.fini:
            return True