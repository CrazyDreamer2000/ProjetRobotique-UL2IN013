import math

def normaliser_angle(a: float) -> float:
    return (a + math.pi) % (2 * math.pi) - math.pi

def erreur_angle(cible: float, actuel: float) -> float:
    return normaliser_angle(cible - actuel)

def coins_rectangle(longueur_m: float, largeur_m: float):
    L = longueur_m / 2
    l = largeur_m / 2
    # repère robot: x avant, y gauche
    return [(-L, -l), (L, -l), (L, l), (-L, l)]

def transformer_point_local_vers_monde(x: float, y: float, cx: float, cy: float, ori: float) -> tuple[float, float]:
    """
    Prend en paramètre une coordonnée (x,y) locale par rapport à une position (cx, cy, ori) et renvoie la coordonnée dans le monde par rapport à la position (en mètres).
    """
    import math
    xr = x * math.cos(ori) - y * math.sin(ori)
    yr = x * math.sin(ori) + y * math.cos(ori)
    return cx + xr, cy + yr

def coins_rect_dans_monde(cx: float, cy: float, ori: float, longueur_m: float, largeur_m: float):
    """
    Prend en paramètre la position d'un rectangle et renvoie la position de ses coins dans le monde (en mètres).
    """
    coins = coins_rectangle(longueur_m, largeur_m)
    return [transformer_point_local_vers_monde(x, y, cx, cy, ori) for x, y in coins]