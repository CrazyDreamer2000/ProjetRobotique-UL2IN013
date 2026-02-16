import math

def normaliser_angle(angle):
    """Ramène un angle dans [-pi, pi]"""
    return (angle + math.pi) % (2 * math.pi) - math.pi


class AlgoCarre:
    """
    Fait un carré parfait basé sur la pose réelle du robot.
    """

    def __init__(self, vitesse_roues, longueur_cote=0.5):
        self.v = vitesse_roues
        self.longueur_cote = longueur_cote

        self.etat = "avance"
        self.cote_actuel = 0

        self.x_depart = None
        self.y_depart = None
        self.orientation_depart = None

    def calculer_commande(self, robot, dt):

        # Carré terminé
        if self.cote_actuel >= 4:
            return 0.0, 0.0

        x = robot.pos.x
        y = robot.pos.y
        theta = robot.pos.orientation

        # --- Phase AVANCE ---
        if self.etat == "avance":

            # Initialisation du segment
            if self.x_depart is None:
                self.x_depart = x
                self.y_depart = y

            distance = math.sqrt(
                (x - self.x_depart)**2 +
                (y - self.y_depart)**2
            )

            if distance >= self.longueur_cote:
                # Passage à la rotation
                self.etat = "tourne"
                self.orientation_depart = theta
                self.x_depart = None
                self.y_depart = None
                return 0.0, 0.0

            return self.v, self.v

        # --- Phase TOURNE ---
        elif self.etat == "tourne":

            # différence entre l'orientation actuelle et celle du début de rotation
            diff_angle = normaliser_angle(
                theta - self.orientation_depart
            )

            # si on a atteint 90°
            if abs(diff_angle) >= math.pi / 2:
                self.cote_actuel += 1
                self.etat = "avance"
                self.orientation_depart = None
                return 0.0, 0.0

            angle_restant = (math.pi / 2) - abs(diff_angle) # angle restant avant 90°

            v = self.v * (angle_restant / (math.pi / 2)) # vitesse proportionnelle a l'angle restant

            v = max(v, 0.5) # pr eviter une vitesse trop petite

            return -v, v # tourner sur place (gauche)

        return 0.0, 0.0
