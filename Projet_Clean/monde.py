# On pourrait mettre ici tout ce qui concerne l'interface, les obstacles, etc

class Obstacle:
    def __init__(self,x,y,largeur,longueur):
        self.x= x
        self.y= y
        self.largeur = largeur
        self.longueur = longueur

    def get_corners(self):
        #Permet d'obtenir la position des 4 coins de l'obstacle
        bottom_left=(self.x-self.longueur/2,self.y-self.largeur/2)
        bottom_right=(self.x+self.longueur/2,self.y-self.largeur/2)
        upper_left=(self.x-self.longueur/2,self.y+self.largeur/2)
        upper_right=(self.x+self.longueur/2,self.y+self.largeur/2)
        return bottom_left,bottom_right,upper_left,upper_right