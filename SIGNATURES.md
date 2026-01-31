# Signatures des Fonctions - ProjetRobot

## 1. GÉNÉRER OBSTACLES

### Fonction: `generer_obstacle`
```python
def generer_obstacle(mouse_x: int, mouse_y: int, taille: int) -> pygame.Rect
```

**Description:**
Crée un obstacle carré centré sur la position donnée.

**Paramètres:**
- `mouse_x` (int) : Coordonnée X du centre de l'obstacle
- `mouse_y` (int) : Coordonnée Y du centre de l'obstacle
- `taille` (int) : Taille du carré en pixels

**Retour:**
- `pygame.Rect` : Rectangle représentant l'obstacle

**Exemple d'utilisation:**
```python
obstacle = generer_obstacle(400, 300, 60)
obstacles.append(obstacle)
```

**Localisation:** `utils.py`

---

## 2. CONTRÔLER COLLISIONS

### Méthode: `check_collision` (classe Robot)
```python
def check_collision(self, obstacles) -> bool
```

**Description:**
Vérifie si le robot (cercle) entre en collision avec un obstacle (rectangle).
Utilise la détection de collision cercle-rectangle en trouvant le point le plus proche du centre du robot sur chaque rectangle.

**Paramètres:**
- `obstacles` (list) : Liste des pygame.Rect représentant les obstacles

**Retour:**
- `bool` : `True` s'il y a collision, `False` sinon

**Exemple d'utilisation:**
```python
if robot.check_collision(obstacles):
    print("Collision détectée!")
```

**Localisation:** `classrobot.py`

---

### Fonction auxiliaire: `calculer_distance_obstacle`
```python
def calculer_distance_obstacle(robot, obstacle: pygame.Rect) -> float
```

**Description:**
Calcule la distance entre le robot et un obstacle spécifique.
Distance mesurée entre le centre du robot et le point le plus proche de l'obstacle.

**Paramètres:**
- `robot` (Robot) : Instance du robot
- `obstacle` (pygame.Rect) : Un obstacle

**Retour:**
- `float` : Distance en pixels

**Localisation:** À ajouter dans `utils.py`

---

## 3. TRACER

### Fonction: `tracer_trajectoire`
```python
def tracer_trajectoire(screen: pygame.Surface, trajectoire: list, 
                       couleur: tuple = (0, 255, 0), epaisseur: int = 3) -> None
```

**Description:**
Dessine la trajectoire du robot sur l'écran sous forme de ligne continue.

**Paramètres:**
- `screen` (pygame.Surface) : Surface pygame pour dessiner
- `trajectoire` (list) : Liste des positions (x, y) du robot
- `couleur` (tuple) : Tuple RGB de la couleur (par défaut vert)
- `epaisseur` (int) : Épaisseur de la ligne en pixels (par défaut 3)

**Retour:**
- `None`

**Exemple d'utilisation:**
```python
tracer_trajectoire(screen, trajectoire)
tracer_trajectoire(screen, trajectoire, couleur=(255, 0, 0), epaisseur=5)
```

**Localisation:** `utils.py`

---

### Fonction: `dessiner_obstacles`
```python
def dessiner_obstacles(screen: pygame.Surface, obstacles: list, 
                       couleur: tuple = (100, 100, 100)) -> None
```

**Description:**
Dessine tous les obstacles sur l'écran sous forme de rectangles.

**Paramètres:**
- `screen` (pygame.Surface) : Surface pygame pour dessiner
- `obstacles` (list) : Liste des pygame.Rect représentant les obstacles
- `couleur` (tuple) : Tuple RGB de la couleur (par défaut gris)

**Retour:**
- `None`

**Exemple d'utilisation:**
```python
dessiner_obstacles(screen, obstacles)
dessiner_obstacles(screen, obstacles, couleur=(255, 0, 0))
```

**Localisation:** `utils.py`

---

### Méthode: `draw` (classe Robot)
```python
def draw(self, screen)
```

**Description:**
Dessine le robot sur l'écran. Le robot est représenté par un cercle bleu avec une ligne rouge indiquant sa direction.

**Paramètres:**
- `screen` (pygame.Surface) : Surface pygame pour dessiner

**Retour:**
- `None`

**Exemple d'utilisation:**
```python
robot.draw(screen)
```

**Localisation:** `classrobot.py`

---

## RÉSUMÉ DES FICHIERS

| Fichier | Fonctions/Méthodes |
|---------|------------------|
| `classrobot.py` | `check_collision()`, `draw()` |
| `utils.py` | `generer_obstacle()`, `tracer_trajectoire()`, `dessiner_obstacles()` |
| `main.py` | Boucle de jeu principale |
