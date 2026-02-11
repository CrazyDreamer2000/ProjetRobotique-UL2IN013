# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc

class Obstacle:
    def __init__(self,x,y,largeur,longueur):
        self.x= x # pixels
        self.y= y # pixels
        self.largeur = largeur # mètres
        self.longueur = longueur # mètres
        