import math

class Robot:
    def __init__(self, name, x=0, y=0, angle=0):
        """Initialisation des attributs du robot sans dépendance graphique"""
        self.name = name
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.v_linear = 0   
        self.v_angular = 0  
        self.taille_x = 100
        self.taille_y = 100
        self.rayon = 50

    def update_velocity(self, v_linear, v_angular):
        """Met à jour les vitesses linéaire et angulaire"""
        self.v_linear = v_linear
        self.v_angular = v_angular

    def move(self, dt, obstacles=None):
        """Met à jour la position et gère la collision physique"""

        # ÉTAPE 1: Sauvegarder la position actuelle avant de bouger
        old_x, old_y = self.x, self.y
        # ÉTAPE 2: Calculer la nouvelle position
        self.angle += self.v_angular * dt
        self.x += self.v_linear * dt * math.cos(self.angle)
        self.y += self.v_linear * dt * math.sin(self.angle)
        # ÉTAPE 3: Vérifier s'il y a collision avec les obstacles
        if obstacles and self.check_collision(obstacles):
            self.x, self.y = old_x, old_y

    def check_collision(self, obstacles):
        """Vérifie si le robot touche un des obstacles"""
        for obstacle in obstacles:
            if obstacle.calculer_distance(self.x, self.y) < self.rayon:
                return True
        return False

    def control_depassement(self, width, height):
        """Contrôle que le robot reste dans les limites de l'arène"""
        self.x = max(self.rayon, min(self.x, width - self.rayon))
        self.y = max(self.rayon, min(self.y, height - self.rayon))