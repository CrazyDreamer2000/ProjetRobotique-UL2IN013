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

        new_x = vitesse * duree * math.cos(radian_angle)
        new_y = vitesse * duree * math.sin(radian_angle)
        self.x = round(new_x,5)
        self.y = round(new_y,5)
    def get_position(self):
        return (self.x, self.y, self.angle)
print ("-------------test class Robot-----------------")
robot1 = Robot("best_robot")
robot1.move(10, 2, 90)
position = robot1.get_position()
print(f"Robot Position: x={position[0]}, y={position[1]}, angle={position[2]}")