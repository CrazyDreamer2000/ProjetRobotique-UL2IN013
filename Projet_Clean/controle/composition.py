from controle.algo_base import AlgoBase

class Sequence(AlgoBase):
    """
    Exécute plusieurs stratégies/primitives l'une après l'autre
    """
    def __init__(self, traducteur, etapes, dt=0.05):
        super().__init__(traducteur, name="Sequence", type="Composition")
        self.etapes = etapes
        self.index = 0
        self.dt = dt

    def start(self):
        #super().start()
        print("Sequence")
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
    def __init__(self, trad, condition_switch, si_vrai, si_faux, condition_stop):
        super().__init__(trad, name="Condition", type="Composition")
        self.condition_switch = condition_switch
        self.si_vrai = si_vrai
        self.si_faux = si_faux
        self.condition_stop = condition_stop
        self.si_vrai_en_cours = False # True si la stratégie actuelle est si_vrai, False sinon
    
    def start(self):
        #super().start()
        print("start Condition")

        if self.condition_switch(self.trad):
            print(" switch True")
            self.si_vrai_en_cours = True
            self.si_vrai.start()
        else:
            print(" switch False")
            self.si_vrai_en_cours = False
            self.si_faux.start()
        
    def step(self):
        print("   step Condition: switch=",self.condition_switch(self.trad),"stop=",self.stop())
        #print(self.trad.get_distance_devant())
        if self.stop():
            self.trad.set_vitesse_roues(0.0, 0.0)
            return
        
        if self.si_vrai_en_cours:   # Si si_vrai est en cours
            print("si_vrai en cours")
            if self.si_vrai.stop():     # mais qu'il doit s'arrêter
                self.si_vrai_en_cours = False # on indique qu'il n'est plus en cours 
                self.si_faux.step()           # et on continue si_faux
            else:
                self.si_vrai.step()     # Sinon, on continue si_vrai
        
        else:                       # SINON (si_vrai n'est pas en cours)
            print("si_faux en cours")
            if self.condition_switch(self.trad): # Si la condition est vérifiée
                self.si_vrai_en_cours = True   # on indique qu'il est en cours
                self.si_vrai.start()           # on le démarre
                self.si_vrai.step()
            else:
                self.si_faux.step()       # Sinon, on continue si_faux
    
    def stop(self):
        return self.condition_stop()
    

class Boucle(AlgoBase):
    def __init__(self, trad, strategie, n):
        super().__init__(trad, name="Boucle", type="Composition")
        self.strategie = strategie
        self.n = n # itérations restantes
        self.i = 0

    def start(self):
        #super().start()
        print("start Boucle")
        self.i = 0

    def step(self):
        if self.stop():
            return
        if self.strategie.stop():
            self.i += 1
            self.strategie.start()
        self.strategie.step()

    def stop(self):
        return self.i >= self.n
