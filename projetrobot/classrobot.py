import math
class Robot:
    def __init__(self, name, x=0, y=0, angle=0):
        # Initialisation des attributs du robot
        self.name = name
        self.x = x
        self.y = y
        self.angle = math.radians(angle)

        self.v_linear = 0   # regler une vitesse linéaire initiale à 0
        self.v_angular = 0  # regler un vitesse angulaire initiale à 0

    
    def update_velocity(self, v_linear, v_angular):
        # Met à jour les vitesses linéaire et angulaire du robot
        self.v_linear = v_linear
        self.v_angular = v_angular
    
    
    def move(self, duree):
        self.angle = self.angle

        new_x = vitesse * duree * self.angle
        new_y = vitesse * duree * self.angle

        self.y += new_y
        self.x += new_x
        self.x = round(new_x,5)
        self.y = round(new_y,5)
    
    
    def get_position(self):
        return (self.x, self.y, self.angle)


print ("-------------test class Robot-----------------")
robot1 = Robot("best_robot")
robot1.move(10, 2, 90)
position = robot1.get_position()
print(f"Robot Position: x={position[0]}, y={position[1]}, angle={position[2]}")