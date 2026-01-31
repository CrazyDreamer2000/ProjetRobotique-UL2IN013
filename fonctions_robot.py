import pygame


def generer_obstacle(mouse_x: int, mouse_y: int, taille: int) -> pygame.Rect:
    """
    Crée un obstacle carré centré sur la position donnée.
    
    Args:
        mouse_x: Coordonnée X du centre
        mouse_y: Coordonnée Y du centre
        taille: Taille du carré
        
    Returns:
        pygame.Rect représentant l'obstacle
    """
    return pygame.Rect(mouse_x - taille // 2, 
                       mouse_y - taille // 2,
                       taille, 
                       taille)


def tracer_trajectoire(screen: pygame.Surface, trajectoire: list, 
                       couleur: tuple = (0, 255, 0), epaisseur: int = 3) -> None:
    """
    Dessine la trajectoire du robot sur l'écran.
    
    Args:
        screen: Surface pygame pour dessiner
        trajectoire: Liste des positions (x, y) du robot
        couleur: Tuple RGB de la couleur (par défaut vert)
        epaisseur: Épaisseur de la ligne en pixels (par défaut 3)
    """
    if len(trajectoire) > 1:
        pygame.draw.lines(screen, couleur, False, trajectoire, epaisseur)


def dessiner_obstacles(screen: pygame.Surface, obstacles: list, 
                       couleur: tuple = (100, 100, 100)) -> None:
    """
    Dessine tous les obstacles sur l'écran.
    
    Args:
        screen: Surface pygame pour dessiner
        obstacles: Liste des pygame.Rect représentant les obstacles
        couleur: Tuple RGB de la couleur (par défaut gris)
    """
    for obstacle in obstacles:
        pygame.draw.rect(screen, couleur, obstacle)


def effacer_obstacles(obstacles: list) -> None:
    """
    Efface tous les obstacles.
    
    Args:
        obstacles: Liste des obstacles à vider
    """
    obstacles.clear()
