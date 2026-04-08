
import math
from controle.algo_base import AlgoBase
from controle.primitives import AvancerDistance, TournerAngle
from controle.composition import Sequence

class AlgoHexagone(AlgoBase):
    def __init__(self, traducteur, robot, vitesse, cote=0.5):
        super().__init__(traducteur)
        self.robot = robot
        self.vitesse = vitesse
        self.cote = cote
        self.strategie = None
        
        # Q1.5 : Liste de 6 couleurs différentes (RGB)
        self.couleurs = [
            (255, 0, 0),   # Rouge
            (0, 255, 0),   # Vert
            (0, 0, 255),   # Bleu
            (255, 255, 0), # Jaune
            (255, 0, 255), # Magenta
            (0, 255, 255)  # Cyan
        ]

    def start(self):
        """ Initialise la séquence de mouvements du hexagone. """
        etapes = []
        for _ in range(6):
            # Une étape = Avancer + Tourner de 60 degrés (pi/3)
            etapes.append(AvancerDistance(self.trad, self.cote, self.vitesse))
            etapes.append(TournerAngle(self.trad, math.pi / 3, self.vitesse))
        
        self.strategie = Sequence(self.trad, etapes)
        self.strategie.start()
        self.last_index = -1

    def step(self):
        """ Exécute l'étape et change la couleur au début de chaque côté. """
        if self.stop():
            return
            
        # Déterminer le côté actuel (chaque côté a 2 étapes : avance + tourne)
        current_side = self.strategie.index // 2
        
        # Si on commence un nouveau côté, on change la couleur
        if current_side != self.last_index and current_side < 6:
            self.robot.change_couleur(self.couleurs[current_side])
            self.last_index = current_side
            
        self.strategie.step()

    def stop(self):
        return self.strategie.stop()