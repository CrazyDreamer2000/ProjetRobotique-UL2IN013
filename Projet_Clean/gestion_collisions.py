import math
from core.geom import coins_rect_dans_monde, transformer_point_local_vers_monde


def creer_forme_robot_locale(forme, longueur, largeur):
    """Crée les points de la forme du robot (dans son repère local)."""
    demi_longueur = longueur / 2
    demi_largeur = largeur / 2

    # Cas 1 : triangle
    if forme == "triangle":
        return [
            (demi_longueur, 0.0),
            (-demi_longueur, demi_largeur),
            (-demi_longueur, -demi_largeur),
        ]

    # Cas 2 : cercle (approché avec un polygone)
    if forme == "cercle":
        rayon = (demi_longueur + demi_largeur) / 2
        points_cercle = []
        nombre_points = 16

        for indice in range(nombre_points):
            angle = 2 * math.pi * indice / nombre_points
            x = rayon * math.cos(angle)
            y = rayon * math.sin(angle)
            points_cercle.append((x, y))

        return points_cercle

    # Cas par défaut : rectangle
    return [
        (-demi_longueur, -demi_largeur),
        (demi_longueur, -demi_largeur),
        (demi_longueur, demi_largeur),
        (-demi_longueur, demi_largeur),
    ]


def polygone_local_vers_monde(points_locaux, x, y, orientation):
    """Transforme des points locaux vers le monde."""
    return [
        transformer_point_local_vers_monde(point_x_local, point_y_local, x, y, orientation)
        for point_x_local, point_y_local in points_locaux
    ]


def point_sur_segment(px, py, ax, ay, bx, by):
    """Vérifie si le point P(px, py) est sur le segment AB."""
    eps = 1e-9
    det = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
    if abs(det) > eps:
        return False

    return (
        min(ax, bx) - eps <= px <= max(ax, bx) + eps
        and min(ay, by) - eps <= py <= max(ay, by) + eps
    )


def orientation(p, q, r):
    """0 aligné, 1 horaire, 2 anti-horaire."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2


def segments_se_coupent(a1, a2, b1, b2):
    """Vérifie si les segments A1A2 et B1B2 se coupent."""
    o1 = orientation(a1, a2, b1)
    o2 = orientation(a1, a2, b2)
    o3 = orientation(b1, b2, a1)
    o4 = orientation(b1, b2, a2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and point_sur_segment(b1[0], b1[1], a1[0], a1[1], a2[0], a2[1]):
        return True
    if o2 == 0 and point_sur_segment(b2[0], b2[1], a1[0], a1[1], a2[0], a2[1]):
        return True
    if o3 == 0 and point_sur_segment(a1[0], a1[1], b1[0], b1[1], b2[0], b2[1]):
        return True
    if o4 == 0 and point_sur_segment(a2[0], a2[1], b1[0], b1[1], b2[0], b2[1]):
        return True

    return False


def point_dans_polygone(point, polygone):
    """Ray casting: nombre de croisements impair => dedans."""
    point_x, point_y = point
    est_dedans = False

    for indice in range(len(polygone)):
        x1, y1 = polygone[indice]
        x2, y2 = polygone[(indice + 1) % len(polygone)]

        if point_sur_segment(point_x, point_y, x1, y1, x2, y2):
            return True

        segment_coupe_le_rayon = (y1 > point_y) != (y2 > point_y)
        if segment_coupe_le_rayon:
            x_intersection = x1 + (point_y - y1) * (x2 - x1) / (y2 - y1)
            if x_intersection >= point_x:
                est_dedans = not est_dedans

    return est_dedans


def polygones_en_collision(polygone_a, polygone_b):
    """Retourne True si 2 polygones se touchent/se croisent."""
    # Étape 1 : une arête de A coupe une arête de B
    for indice_a in range(len(polygone_a)):
        a1 = polygone_a[indice_a]
        a2 = polygone_a[(indice_a + 1) % len(polygone_a)]

        for indice_b in range(len(polygone_b)):
            b1 = polygone_b[indice_b]
            b2 = polygone_b[(indice_b + 1) % len(polygone_b)]

            if segments_se_coupent(a1, a2, b1, b2):
                return True

    # Étape 2 : sinon un polygone peut être complètement dans l'autre
    if point_dans_polygone(polygone_a[0], polygone_b):
        return True
    if point_dans_polygone(polygone_b[0], polygone_a):
        return True

    return False


def collision_robot_avec_monde(pos_robot, robot_forme_locale, obstacles, longueur_monde, largeur_monde):
    """Retourne True si le robot touche un bord ou un obstacle."""
    forme_robot_monde = polygone_local_vers_monde(
        robot_forme_locale,
        pos_robot.x,
        pos_robot.y,
        pos_robot.orientation,
    )

    # Bord du monde
    for point_x, point_y in forme_robot_monde:
        if point_x < 0 or point_x > longueur_monde or point_y < 0 or point_y > largeur_monde:
            return True

    # Obstacles
    for obstacle in obstacles:
        forme_obstacle_monde = coins_rect_dans_monde(
            obstacle.pos.x,
            obstacle.pos.y,
            obstacle.pos.orientation,
            obstacle.longueur,
            obstacle.largeur,
        )

        if polygones_en_collision(forme_robot_monde, forme_obstacle_monde):
            return True

    return False
