import math

def normaliser_angle(a: float) -> float:
    """ramener un angle dans l'intervalle [-pi, pi]."""
    # On replie l'angle sur un tour complet (2*pi), puis on recentre autour de 0.
    return (a + math.pi) % (2 * math.pi) - math.pi

def erreur_angle(cible: float, actuel: float) -> float:
    """l'écart angle cible - angle actuel, normalisé."""
    return normaliser_angle(cible - actuel)

def coins_rectangle(longueur_m: float, largeur_m: float):
    """Construit les 4 coins d'un rectangle centré en (0,0) dans le repère local."""
    # Demi-longueur et demi-largeur
    L = longueur_m / 2
    l = largeur_m / 2

    # repère robot: x avant, y gauche
    # Les coins sont donnés en ordre autour du rectangle.
    return [(-L, -l), (L, -l), (L, l), (-L, l)]

def transformer_point_local_vers_monde(x: float, y: float, cx: float, cy: float, ori: float) -> tuple[float, float]:
    """
    Convertit un point local (x, y) en point monde, selon le centre (cx, cy)
    et l'orientation ori (en radians).
    """
    #Rotation du point local autour de l'origine locale
    xr = x * math.cos(ori) - y * math.sin(ori)
    yr = x * math.sin(ori) + y * math.cos(ori)

    #Translation vers la position réelle du robot/objet dans le monde
    return cx + xr, cy + yr

def coins_rect_dans_monde(cx: float, cy: float, ori: float, longueur_m: float, largeur_m: float):
    """
    Retourne les coins d'un rectangle dans le repère monde.
    Le rectangle est défini par son centre (cx, cy), son orientation ori,
    sa longueur et sa largeur.
    """
    # Coins en local
    coins = coins_rectangle(longueur_m, largeur_m)

    # Conversion coin par coin vers le monde
    return [transformer_point_local_vers_monde(x, y, cx, cy, ori) for x, y in coins]


def polygone_local_vers_monde(points_locaux, x: float, y: float, orientation: float):
    """Transforme des points locaux vers le repère monde."""
    return [
        transformer_point_local_vers_monde(point_x_local, point_y_local, x, y, orientation)
        for point_x_local, point_y_local in points_locaux
    ]
