import math
import pygame
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
    
    
    def move(self, dt):
        # Met à jour la position et l'angle du robot en fonction des vitesses et du temps`
        self.angle = self.v_angular * dt + self.angle

        self.x = self.v_linear * dt * math.cos(self.angle) + self.x
        self.y = self.v_linear * dt * math.sin(self.angle) + self.y

    def draw(self, screen):
        "dessine le robot sur l'écran pygame"
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, 30, 30))

        


    
    



