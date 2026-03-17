import math

# Outils generaux

def aretes(poly):
    """
    Parcourt les arêtes du polygone
    Chaque arête est renvoyée sous la forme ((x1, y1), (x2, y2))
    """
    n = len(poly) # nombre de coins
    for i in range(n):
        yield poly[i], poly[(i + 1) % n]

def normale_unitaire(p1, p2):
    """
    Calcule une "normale unitaire" à l'arête [p1, p2]
    Si l'arête est de longueur nulle -> renvoie None.
    """
    x1, y1 = p1 # coin i
    x2, y2 = p2 # coin i+1 (on utilise modulo pour le cas où on passe sur un coin déjà vu, i>n)

    # vecteur "arête" entre les deux coins
    ex, ey = x2 - x1, y2 - y1 # formule d'un vecteur

    # normale (vecteur normal à l'arête)
    nx, ny = -ey, ex

    norme = math.hypot(nx, ny) # longueur (hypothenuse) entre les deux points
    if norme < 1e-12: # si norm est nulle
        return None

    return nx / norme, ny / norme

# Outils internes SAT

def _axes_sat(poly):
    """
    Retourne les axes (normales aux arêtes) à tester pour la collision.
    """
    axes = [] # liste des axes des vecteurs normaux des côtés du polygone

    for p1, p2 in aretes(poly):
        normale = normale_unitaire(p1, p2)
        if normale is not None:
            axes.append(normale)
    
    return axes

def _projeter(poly, axe):
    """Projette un polygone sur un axe et retourne l'intervalle [min,max] des projections"""

    ax, ay = axe

    p0 = poly[0][0] * ax + poly[0][1] * ay
    mn = mx = p0

    for x, y in poly[1:]:
        p = x * ax + y * ay
        if p < mn:
            mn = p
        if p > mx:
            mx = p
    
    return mn, mx

def _intervalles_se_recouvrent(a : tuple, b : tuple) -> bool:
    return not (a[1] < b[0] or b[1] < a[0])


# Collision SAT principale

def collision_sat(poly_a, poly_b):
    """
    Test de collision polygone convexe vs polygone convexe
    """
    axes = _axes_sat(poly_a) + _axes_sat(poly_b)

    for axe in axes:
            proj_a = _projeter(poly_a, axe)
            proj_b = _projeter(poly_b, axe)

            if not _intervalles_se_recouvrent(proj_a, proj_b):
                return False # "axe séparateur" trouvé -> pas de collision      
    
    # sinon:
    return True


def point_dans_polygone_convexe(x: float, y: float, poly) -> bool:
    """
    Retourne True si le point (x,y) est dans le polygone convexe poly.
    (on vérifie que le point reste du même côté de toutes les arêtes)
    """
    n = len(poly)
    signe_reference = None

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        # vecteur arête
        ex = x2 - x1
        ey = y2 - y1

        # vecteur du sommet vers le point
        px = x - x1
        py = y - y1

        # produit vectoriel 2D
        produit = ex * py - ey * px

        # si très proche de 0, on considère que le point est sur l'arête
        if abs(produit) < 1e-12:
            continue

        signe = produit > 0

        if signe_reference is None:
            signe_reference = signe
        elif signe != signe_reference:
            return False

    return True