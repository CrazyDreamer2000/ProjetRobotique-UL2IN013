import argparse

def build_parser() -> argparse.ArgumentParser:
    """
    Cette fonction crée un objet parser et lui enregistre les options avec add_argument.
    Elle cree la liste des options autorisées (algo, vitesse_roues, orientation). 
    """
    parser = argparse.ArgumentParser()

    parser.add_argument( 
        "--algo",
        type=str,
        default="polygone",
        choices=["carre", "carresafe", "polygone", "avancer", "foncerdevant"],
        help="Nom de l'algorithme",
    )
    parser.add_argument(
        "--vitesse_roues",
        type=float,
        default=6.0,
        help="Vitesse des roues (rad/s)",
    )
    parser.add_argument(
        "--simu",
        action="store_true",
        help="Execution en mode simulation ou sur le vrai robot"
    )
    return parser

def parse_args() -> argparse.Namespace: 
    """
    Cette fonction lit les arguments de la ligne de commande passés au lancement du programme.
    Namespace est un conteneur des valeurs lit
    """
    return build_parser().parse_args()
