
"""
Deux moteurs encodeurs pour le controle des roues (-> sorties: )
3 senseurs :
- une camera                (-> entrée: ?)
- un capteur de distance    (-> entrée: distance d'objet le plus proche)
- un accelerometre          (-> entrée: vitesse du robot)
"""

class Robot:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle_rg = 90          # 0 (gaughe) à 180 (droite) en degrés
        self.angle_rd = 90
        self.vitesse_rg = 0
        self.vitesse_rd = 0
        self.accelleration = 0      # valeur de sortie de l'acceleromètre
        self.distance_au_mur = 0    # valeur (en cm?) de distance à l'objet le plus proche
        # Pour simplifier la simulation de l'input du clavier
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

    def update(self):
        """
        Fonction qui tourne à chaque tick.
        Met à jour les valeurs des attributs du robot en prenant les valeurs des différents capteurs.
        """

        if self.forward:
            self.vitesse_rg += 1
            self.vitesse_rd += 1

        if self.backward:
            self.vitesse_rg -= 1
            self.vitesse_rd -= 1

        # Comment faire pour que soit ca tourne les roues, soit ca fait tourner le robot sur place?
        # Soit: - les deux roues tournent dans le meme sens (pour tourner en avancant / reculant)
        #       - le robot tourne sur place
        if self.left:
            if self.accelleration > 0:
                # tourner les deux roues
                pass
            else:
                # tourner sur place (ici, roue gauche recule et roue droite avance)
                pass
        
        if self.right:
            #etc
            pass


        self.updatePos()
        self.updateAngle()
        self.updateAcceleration()
        self.updateDistance()


    def updatePos(self):
        pass

    def updateAngle(self): # obsolete?
        if self.left:
            self.angle -= 1
        if self.right:
            self.angle += 1

        if self.angle < -90:
            self.angle = -90
        if self.angle > 90:
            self.angle = 90

    def updateAcceleration(self):
        if self.forward:
            pass
            # probleme : pygame fonctionne en updatant x et y, alors quand machine avance avec degré, il faut formule trigo pour updater x et y (qui seront donc flottants)

    def updateDistance(self):
        pass