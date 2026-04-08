#1.1

@dataclass
class Obstacle:
    """
    Classe qui représente un obstacle rectangulaire.
    """
    pos: Pos2D
    longueur: float # Longueur en mètres
    largeur: float # Largeur en mètres
    poly_local: list # Liste des coins

class Monde:
    """
    Simulation de l'environnement réel du robot.
    """
    def __init__(self):
        self.liste_obstacles = []

        # Zone de collision du robot (forme invisible utilisée pour détecter les contacts)
        # Modifiable depuis main.py (rectangle, triangle, cercle + taille).
        self.poly_robot_local = polygone_rectangle_local(cfg.ROBOT_LONGUEUR, cfg.ROBOT_LARGEUR)
        # Créer des obstacles aléatoires dès le départ
        self.ajouter_obstacle(450,300)
        self.ajouter_obstacle(450,575)
        self.ajouter_obstacle(450,50)
       # self.creer_obstacles_aleatoires()
    
    def ajouter_obstacle(self, x, y, longueur=cfg.TAILLE_OBSTACLE, largeur=cfg.TAILLE_OBSTACLE):
        """
        Ajoute un obstacle au monde aux coordonnées (x,y)

        Paramètres:
            x : abscisse du nouvel obstacle (pixels)
            y : ordonnée du nouvel obstacle (pixels)
        """
        self.liste_obstacles.append(Obstacle(
            Pos2D(x/cfg.SCALE, y/cfg.SCALE, orientation=random.uniform(0, 2 * math.pi)),
            longueur, 
            largeur,
            polygone_rectangle_local(longueur, largeur)
        ))

    def creer_obstacles_aleatoires(self):
        """
        Creation de 5 obstacles dans le monde
        """
        # ici 5 zones (4 coins + 1 bord) 
        zones = [
            # (x_min, x_max, y_min, y_max, nom)
            (1.0, 1.0, 1.0, 1.0, "Coin milieu"),      # Zone 2  
            (2.0, 2.0, 3.5, 4, "Coin haut-milieu"),     # Zone 4
            (2.0, 3.0, 0.3, 1, "Bord bas-centre")       # Zone 5
        ]
        
        # un obstacle à la fois
        for i, (x_min, x_max, y_min, y_max, nom) in enumerate(zones):
            
            # Position aléatoire DANS la zone
            x = (x_max)
            y = (y_max)
            
            # Orientation aléatoire (0 à 360°)
            orientation = random.uniform(0, 2 * math.pi)
            
            # Dimensions aléatoires
            longueur = random.uniform(0.3, 0.6)  # 30-60 cm
            largeur = random.uniform(0.15, 0.25) # 15-25 cm
            
            # Créer l'obstacle
            self.ajouter_obstacle(x * cfg.SCALE, y * cfg.SCALE, longueur, largeur) # multiplication par scale est temporaire
            
            print(f" Obstacle {i+1} : {nom} ({x:.2f}, {y:.2f}) angle={math.degrees(orientation):.0f}°")
