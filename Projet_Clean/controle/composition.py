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