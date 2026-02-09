from dataclasses import dataclass

@dataclass
class Pos2D:
    """Position et orientation du robot dans la simulation"""
    x: float
    y: float
    orientation: float  # radians, orientation = 0 -> droite


@dataclass
class CommandeRoues:
    """Commandes envoyées aux roues"""
    vitesse_rotation_gauche: float  # rad/s
    vitesse_rotation_droite: float


@dataclass
class EtatRoues:
    """
    Etat "réel" des roues
    """
    vitesse_rotation_gauche: float
    vitesse_rotation_droite: float
    rotation_totale_gauche: float
    rotation_totale_droite: float