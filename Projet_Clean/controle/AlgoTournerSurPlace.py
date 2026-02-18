# Pourquoi classes? Car algorithme = à chaque pas de temps, décide quelles vitesses envoyer aux deux roues. Plus facile et plus "clean" à coder avec des classes.

class AlgoTournerSurPlace:
    """Fait tourner le robot sur place en continu"""

    def __init__(self, vitesse=0.6, sens="gauche"):
        self.vitesse = vitesse
        self.sens = sens # "gauche" ou "droite"

    def calculer_commande(self, robot) -> tuple[float, float]: 
        """Prend en argument le robot et renvoie les vitesses de la roue gauche et droite"""
        if self.sens == "gauche":
            return -self.vitesse, self.vitesse # vitesse_gauche, vitesse_droite
        else:
            return self.vitesse, -self.vitesse # vitesse_gauche, vitesse_droite
