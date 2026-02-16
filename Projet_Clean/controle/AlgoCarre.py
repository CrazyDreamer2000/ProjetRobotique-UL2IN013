import math

class AlgoCarre:
    """Algorithme pour tracer un carré"""

    def __init__(self, vitesse_roues=4, duree_avance=4, duree_tourne=0.97):
        self.vitesse = vitesse_roues
        self.duree_avance = duree_avance
        self.duree_tourne = duree_tourne

        self.etat = "avance"
        self.temps = 0.0
        self.cotes_faits = 0

        self.arret = False


    def calculer_commande(self, robot, dt):
        """Prend en argument le robot et un tick de temps et renvoie les vitesses de la roue gauche et droite"""
        
        if self.cotes_faits >= 4: # Conditions d'arrêt
            self.arret = True
        if self.arret:
            return 0,0
        
        self.temps += dt

        # Avance tout droit
        if self.etat == "avance":
            if self.temps >= self.duree_avance: # Si le temps pour avancer tout droit est dépassé, on réinitialise le timer et on active "tourner"
                self.temps = 0.0
                self.etat = "tourne"
            return self.vitesse, self.vitesse # Sinon on continue d'avancer tout droit

        # Tourne sur place
        if self.etat == "tourne":
            if self.temps >= self.duree_tourne: # Si le temps pour tourner sur place est dépassé, on réinitialise le timer et on active "avancer"
                self.temps = 0.0
                self.etat = "avance"
                self.cotes_faits += 1 # Un des cotés a été complété

            return -self.vitesse, self.vitesse # Sinon, on continue de tourner sur place
