import math
import pygame
resX,resY=1600,900

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

        #Condition pour qu'il puisse pas sortir de la fenêtre en avançant et oblige le robot à reculer pour revenir dans le cadre (obstacle mur)
        if self.x>= resX:
            self.x = resX
        if self.x <= 0:
            self.x = 0

        if self.y>= resY:
            self.y = resY
        if self.y <= 0:
            self.y = 0
            

    def draw(self, screen):
        "dessine le robot sur l'écran pygame"
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 50)
        head_x = self.x + 25 * math.cos(self.angle)
        head_y = self.y + 25 * math.sin(self.angle)
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (head_x, head_y), 3 )
        


    
    



