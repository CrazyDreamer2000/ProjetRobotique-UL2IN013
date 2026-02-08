import math

class Obstacle:
    def __init__(self, x, y, taille):
        """Définit un obstacle carré par son centre et sa taille"""
        self.x = x - taille // 2
        self.y = y - taille // 2
        self.w = taille
        self.h = taille

    def calculer_distance(self, robot_x, robot_y):
        """Calcule la distance entre le robot et cet obstacle (point le plus proche)"""
        closest_x = max(self.x, min(robot_x, self.x + self.w))
        closest_y = max(self.y, min(robot_y, self.y + self.h))
        
        distance_x = robot_x - closest_x
        distance_y = robot_y - closest_y
        return math.sqrt(distance_x**2 + distance_y**2)