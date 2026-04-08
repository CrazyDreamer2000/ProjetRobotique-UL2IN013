import math

# Géométrie des angles

def normaliser_angle(a: float) -> float:
    """ramener un angle dans l'intervalle [-pi, pi]."""
    # On replie l'angle sur un tour complet (2*pi), puis on recentre autour de 0.
    return (a + math.pi) % (2 * math.pi) - math.pi

def erreur_angle(cible: float, actuel: float) -> float:
    """l'écart angle cible - angle actuel, normalisé."""
    return normaliser_angle(cible - actuel)


# Transformations repère local -> monde

def transformer_point_local_vers_monde(x: float, y: float, cx: float, cy: float, ori: float) -> tuple[float, float]:
    """
    Transforme un point (x, y) défini dans le repère local en coordonnées monde selon le centre (cx, cy) et l'orientation ori (en radians).
    """
    # Rotation du point local autour de l'origine locale
    xr = x * math.cos(ori) - y * math.sin(ori)
    yr = x * math.sin(ori) + y * math.cos(ori)

    # Translation vers la position réelle du robot/objet dans le monde
    return cx + xr, cy + yr

def transformer_polygone_local_vers_monde(points_locaux, pos):
    """
    Transforme un polygone défini (par ses coins dans coins_locaux) dans le repère local vers le repère monde par pos.
    """
    return [
        transformer_point_local_vers_monde(local_x, local_y, pos.x, pos.y, pos.orientation)
        for local_x, local_y in points_locaux
    ]


# Generation de formes locales

def polygone_rectangle_local(longueur_m: float, largeur_m: float):
    """
    Construit les 4 coins d'un rectangle centré en (0,0) dans le repère local.
    """
    L = longueur_m / 2
    l = largeur_m / 2

    # Les coins sont donnés en ordre autour du rectangle
    return [(-L, -l), (L, -l), (L, l), (-L, l)]
