# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc

class Obstacle:
    def __init__(self,x,y,largeur,longueur):
        self.x= x
        self.y= y
        self.largeur = largeur
        self.longueur = longueur
        self.corners = [
                            (self.x - self.longueur/2, self.y - self.largeur/2), # coin arrière-gauche
                            (self.x + self.longueur/2, self.y - self.largeur/2), # coin avant-gauche
                            (self.x + self.longueur/2, self.y + self.largeur/2), # coin avant-droit
                            (self.x - self.longueur/2, self.y + self.largeur/2) # coin arrière-droit
                        ]

    def get_corners(self):
        """Méthode getter pour les coins de l'obstacle"""
        return self.corners