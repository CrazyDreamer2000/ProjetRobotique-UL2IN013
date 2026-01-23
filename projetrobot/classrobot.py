import math
class Robot:
    def __init__(self, name, x=0, y=0, angle=0):
        self.name = name
        self.x = x
        self.y = y
        self.angle = angle
    def move(self, vitesse, duree, angle):
        self.angle = angle
        radian_angle = math.radians(self.angle)
        self.x += vitesse * duree * math.cos(radian_angle)
        self.y += vitesse * duree * math.sin(radian_angle)