from dataclasses import dataclass # on utilise dataclass juste pour simplifier le code de chaque classe, ca enlève de la redondance, pas besoind d'ecrire un constructeur a chaque fois

@dataclass
class Pos2D:
    """Position et orientation du robot dans la simulation"""
    x: float # mètres
    y: float # mètres
    orientation: float  # radians, orientation = 0 -> droite


@dataclass
class CommandeRoues:
    """Commandes envoyées aux roues"""
    vitesse_rotation_gauche: float # rad/s
    vitesse_rotation_droite: float # 


@dataclass
class EtatRoues:
    """
    Etat "réel" des roues
    """
    vitesse_rotation_gauche: float # rad/s
    vitesse_rotation_droite: float #
    rotation_totale_gauche: float # rad
    rotation_totale_droite: float #
