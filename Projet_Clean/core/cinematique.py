import math

class CinematiqueDeuxRoues:
    """
    Intermédiaire entre mesures + état des roues et le déplacement du robot (mises à jour de la position)
    """

    def __init__(self, rayon_roue_m: float, ecartement_roues_m: float):
        self.rayon_roue = rayon_roue_m
        self.ecartement_roues = ecartement_roues_m

    def vitesses_robot_depuis_roues(self, vitesse_rotation_gauche: float, vitesse_rotation_droite: float) -> tuple[float, float]:
        """
        Prends en paramètre les vitesses de rotation des roues et renvoie la vitesse avant (m/s) et la vitesse de rotation (rad/s) du robot
        """
        vitesse_lineaire_gauche = self.rayon_roue * vitesse_rotation_gauche # mètres/s = mètres * rad/s 
        vitesse_lineaire_droite = self.rayon_roue * vitesse_rotation_droite #

        vitesse_avant = (vitesse_lineaire_droite + vitesse_lineaire_gauche) / 2 # moyenne de la vitesse des roues (choix)
        vitesse_rotation = (vitesse_lineaire_droite - vitesse_lineaire_gauche) / self.ecartement_roues # différence des vitesses des deux roues / ecartement (plus ils sont écartés, moins le robot tourne vite)
        
        return vitesse_avant, vitesse_rotation

    def avance_pos(self, pos, vitesse_avant: float, vitesse_rotation: float, dt: float):
        """
        Prend en paramètre la position, vitesse avant, et vitesse de rotation du robot ainsi qu'une marge de temps (en secondes) et calcule la nouvelle position du robot à partir des paramètres.
        """
        x, y, ori = pos.x, pos.y, pos.orientation

        # Si on tourne très peu : approx tout droit
        if abs(vitesse_rotation) < 1e-9:
            x2 = x + vitesse_avant * math.cos(ori) * dt # On rajoute la distance parcourue avec une vitesse vitesse_avant en dt temps avec une orientation ori (cos pour le x pour avancer sur les x plus lentement si on avance pas tout droit sur les x)
            y2 = y + vitesse_avant * math.sin(ori) * dt # Pareil pour les y
            ori2 = ori
            return type(pos)(x2, y2, ori2)

        # Sinon : arc de cercle
        rayon_virage = vitesse_avant / vitesse_rotation # Distance entre centre robot et centre de rotation. Plus vitesse_rotation grande, plus rayon_virage petit = angle plus aigu
        ori2 = ori + vitesse_rotation * dt # Angle obtenu avec vitesse_rotation en dt temps

        x2 = x + rayon_virage * (math.sin(ori2) - math.sin(ori))
        y2 = y - rayon_virage * (math.cos(ori2) - math.cos(ori))

        return type(pos)(x2, y2, ori2)

