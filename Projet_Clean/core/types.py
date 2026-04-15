from dataclasses import dataclass # on utilise dataclass juste pour simplifier le code de chaque classe, ca enlève de la redondance, pas besoind d'ecrire un constructeur a chaque fois

@dataclass
class Pos2D:
    """Position et orientation du robot dans la simulation"""
    x: float # millimètres
    y: float # millimètres
    orientation: float  # radians, orientation = 0 -> droite


@dataclass
class Roue:
    """
    Etat d'une roue
    """
    vitesse_rotation: float # rad/s
    rotation_totale: float # rad


@dataclass
class Capteurs:
    """Différentes valeurs des capteurs envoyées au robot"""
    accelerometre: float
    capteur_distance: float
