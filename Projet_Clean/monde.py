# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc

class Obstacle:
    def __init__(self,x,y,largeur,longueur):
        self.x= x
        self.y= y
        self.largeur = largeur // 2
        self.longueur = longueur // 2  