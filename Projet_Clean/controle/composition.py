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


class Condition(AlgoBase):
    """
    Execute la stratégie si_faux.
    Si la condition est vérifiée, la stratégie si_vrai est lancée et dure jusqu'à sa fin.
    """
    def __init__(self, trad, condition, si_vrai, si_faux):
        super().__init__(trad)
        self.condition = condition
        self.si_vrai = si_vrai
        self.si_faux = si_faux
        self.si_vrai_en_cours = False # True si la stratégie actuelle est si_vrai, False sinon
    
    def start(self):
        self.si_faux.start()

    def step(self):
        if self.stop():
            return
        
        if self.si_vrai_en_cours:   # Si si_vrai est en cours
            if self.si_vrai.stop():     # mais qu'il doit s'arrêter
                self.si_vrai_en_cours = False # on indique qu'il n'est plus en cours 
                self.si_faux.step()           # et on continue si_faux
            else:
                self.si_vrai.step()     # Sinon, on continue si_vrai
        
        else:                       # SINON (si_vrai n'est pas en cours)
            if self.condition(self.trad): # Si la condition est vérifiée
                self.si_vrai_en_cours = True   # on indique qu'il est en cours
                self.si_vrai.start()           # on le démarre
                self.si_vrai.step()
            else:
                self.si_faux.step()       # Sinon, on continue si_faux
    
    def stop(self):
        return self.si_faux.stop()
    

class Boucle(AlgoBase):
    def __init__(self, trad, strategie, n):
        super().__init__(trad)
        self.strategie = strategie
        self.n = n # itérations restantes
        self.i = 0

    def start(self):
        self.i = 0

    def step(self):
        if self.stop():
            return
        if self.strategie.stop():
            print('incrémentation boucle')
            self.i += 1
            self.strategie.start()
        self.strategie.step()

    def stop(self):
        if self.i >= self.n:
            print('boucle finie')
        return self.i >= self.n
