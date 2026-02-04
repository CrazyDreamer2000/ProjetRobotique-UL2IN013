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
        
        # Taille du robot pour le contrôle de dépassement (basé sur le rayon de 50)
        self.taille_x = 100
        self.taille_y = 100

    
    def update_velocity(self, v_linear, v_angular):
        # Met à jour les vitesses linéaire et angulaire du robot
        self.v_linear = v_linear
        self.v_angular = v_angular
    
    
    def move(self, dt, obstacles=None):
        # Met à jour la position et l'angle du robot en fonction des vitesses et du temps
        
        # ÉTAPE 1: Sauvegarder la position actuelle avant de bouger
        old_x = self.x
        old_y = self.y
        
        # ÉTAPE 2: Calculer la nouvelle position
        self.angle = self.v_angular * dt + self.angle
        self.x = self.v_linear * dt * math.cos(self.angle) + self.x
        self.y = self.v_linear * dt * math.sin(self.angle) + self.y
        
        # ÉTAPE 3: Vérifier s'il y a collision avec les obstacles
        if obstacles and self.check_collision(obstacles):
            # ÉTAPE 4: Si collision, annuler le déplacement
            self.x = old_x
            self.y = old_y

    def draw(self, screen):
        "dessine le robot sur l'écran pygame"
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 50)
        head_x = self.x + 25 * math.cos(self.angle)
        head_y = self.y + 25 * math.sin(self.angle)
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (head_x, head_y), 3 )
    
    def check_collision(self, obstacles):
        rayon = 50  # Rayon du robot (cercle)
        
        for obstacle in obstacles:
            # Trouver le point le plus proche du rectangle
            
            # Vérifier X
            if self.x < obstacle.left:
                closest_x = obstacle.left  # Robot à gauche
            elif self.x > obstacle.right:
                closest_x = obstacle.right  # Robot à droite
            else:
                closest_x = self.x  # Robot dedans
            
            # Vérifier Y
            if self.y < obstacle.top:
                closest_y = obstacle.top  # Robot au-dessus
            elif self.y > obstacle.bottom:
                closest_y = obstacle.bottom  # Robot au-dessous
            else:
                closest_y = self.y  # Robot dedans
            
            # Calculer la distance entre le centre du robot et ce point le plus proche
            distance_x = self.x - closest_x
            distance_y = self.y - closest_y
            distance = math.sqrt(distance_x**2 + distance_y**2)
            
            # Si la distance est inférieure au rayon, il y a collision
            if distance < rayon:
                return True  # Collision détectée
        
        return False  # Aucune collision
    
    def control_depassement(self, surface):
        "Contrôle que le robot reste dans les limites de la surface"
        demi_taille_x = self.taille_x / 2
        demi_taille_y = self.taille_y / 2

        largeur = surface.get_width()
        hauteur = surface.get_height()

        x_min = demi_taille_x
        x_max = largeur - demi_taille_x

        y_min = demi_taille_y
        y_max = hauteur - demi_taille_y

        if self.x < x_min:
            self.x = x_min
        if self.x > x_max:
            self.x = x_max
        
        if self.y < y_min:
            self.y = y_min
        if self.y > y_max:
            self.y = y_max
    

    



