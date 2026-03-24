from controle.algo_base import AlgoBase

class Sequence(AlgoBase):
    """
    Exécute plusieurs stratégies l'une après l'autre
    """
    def __init__(self, etapes):
        self.etapes = etapes
        self.index = 0
        self.fini = False

    def start(self, robot, monde):
        self.index = 0
        self.fini = False

        if len(self.etapes) == 0:
            self.fini = True
        else:
            self.etapes[0].start(robot, monde)
    
    def step(self, robot, monde, dt):
        if self.fini:
            return 0.0, 0.0
        
        etape = self.etapes[self.index]
        vg, vd = etape.step(robot, monde, dt)

        if getattr(etape, "fini", False):
            self.index += 1

            if self.index >= len(self.etapes):
                self.fini = True
                return 0.0, 0.0
            
            self.etapes[self.index].start(robot, monde)
        
        return vg, vd


class InterruptionCollision(AlgoBase):
    """
    Exécute la stratégie normale.
    Si collision, lance une stratégie d'évitement et la garde jusqu'à ce qu'elle soit terminée
    """

    def __init__(self, strategie_normale, strategie_collision):
        self.normale = strategie_normale
        self.collision = strategie_collision
        self.mode = "normal"

    def start(self, robot, monde):
        self.mode = "normal"
        self.normale.start(robot, monde)

    def step(self, robot, monde, dt):
        if self.mode == "normal":
            if robot.en_collision:
                self.mode = "collision"
                self.collision.start(robot, monde)
                return self.collision.step(robot, monde, dt)

            return self.normale.step(robot, monde, dt)

        elif self.mode == "collision":
            vg, vd = self.collision.step(robot, monde, dt)

            if getattr(self.collision, "fini", False):
                self.mode = "normal"

            return vg, vd

        return 0.0, 0.0

    def stop(self, robot, monde):
        return 0.0, 0.0