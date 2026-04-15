# controle/traducteur.py

from abc import ABC, abstractmethod # Pour les classes abstraites
from core.robot import Robot
from monde.monde import Monde
from core.geom import normaliser_angle
import math

class Traducteur(ABC):
    """
    Classe abstraite définissant l'interface entre le controlleur et le robot
    """
    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        pass

    def get_distance_devant(self) -> float:
        pass

    def reset_distance_parcourue(self):
        pass

    def get_distance_parcourue(self) -> float:
        pass

    def reset_angle_parcouru(self):
        pass

    def get_angle_parcouru(self) -> float:
        pass

    def est_en_collision(self) -> bool:
        pass

class TraducteurSimu(Traducteur):
    """
    Implémentation du traducteur pour la simulation.
    Fait le lien entre les commandes de l'algo et les objets Robot/Monde.
    """
    def __init__(self, monde: Monde):
        self.monde = monde

        # Références de départ pour les mesures relatives
        self._distance_depart_gauche = 0.0
        self._distance_depart_droite = 0.0
        self._orientation_depart = monde.robot.pos.orientation

    # COMMANDES

    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        """
        Paramètres:
            - v_gauche : float
              Vitesse de rotation de la roue gauche (rad/s)
            - v_droite : float
              Vitesse de rotation de la roue droite (rad/s)
        """
        # Envoie directement les commandes au robot simulé
        self.monde.robot.roue_gauche.vitesse_rotation = v_gauche
        self.monde.robot.roue_droite.vitesse_rotation = v_droite

    # DISTANCE PARCOURUE

    def reset_distance_parcourue(self):
        """ Réinitialise les références de distance pour le calcul de la distance parcourue."""
        self._distance_depart_gauche = self.monde.robot.roue_gauche.rotation_totale
        self._distance_depart_droite = self.monde.robot.roue_gauche.rotation_totale

    def get_distance_parcourue(self) -> float:
        """ Calcule la distance parcourue depuis le dernier reset en utilisant les rotations des roues."""
        rayon = self.monde.cinematique.rayon_roue

        delta_gauche = self.monde.robot.roue_gauche.rotation_totale - self._distance_depart_gauche
        delta_droite = self.monde.robot.roue_gauche.rotation_totale - self._distance_depart_droite

        distance_gauche = delta_gauche * rayon
        distance_droite = delta_droite * rayon

        return abs(distance_gauche + distance_droite) / 2

    def reset_angle_parcouru(self):
        """ Réinitialise la référence d'orientation pour le calcul de l'angle parcouru."""
        self._orientation_depart = self.monde.robot.pos.orientation

    def get_angle_parcouru(self) -> float:
        """ Calcule l'angle parcouru depuis le dernier reset en utilisant l'orientation du robot."""
        return normaliser_angle(self.monde.robot.pos.orientation - self._orientation_depart)

    # CAPTEURS / ETAT

    def get_distance_devant(self) -> float:
        """
        Sortie:
            - monde.lire_distance_devant(robot.pos) : float
              Valeur du capteur de distance (distance en millimètres : (0.5 -> 8000) )
        """
        # Utilise le monde pour calculer de distance
        return self.monde.lire_distance_devant(self.monde.robot.pos)
    
    def est_en_collision(self) -> bool:
        """
        Renvoie True si le robot simulé est en collision, False sinon
        """
        return self.monde.robot.en_collision
    
class TraducteurReel(Traducteur):
    """
    Implémentation du traducteur pour le robot réel.
    Fait le lien entre les commandes de l'algo et les fonctions d'interface du robot réel.
    """
    def __init__(self, robot):
        self.robot = robot
    # Pour la distance
        self._ref_pos_gauche_distance = 0.0
        self._ref_pos_droite_distance = 0.0


    def set_vitesse_roues(self, v_gauche: float, v_droite: float):
        """
        Ici on effectue la conversion de rad/s à deg/s
        v_gauche: Vitesse de la roue gauche (en rad/s)
        v_droite: Vitesse de la roue droite (en rad/s)
        """
        # formule de degré par radian
        deg_par_rad = 180 / math.pi #57.296

        #Ici on effectue la conversion rad/s à deg/s
        dps_gauche=  v_gauche  *  deg_par_rad
        dps_droite = v_droite *  deg_par_rad

        #ici on applique la vitesse en deg/s au moteurs gauche et droite
        self.robot.set_motor_dps(self.robot.MOTOR_left,dps_gauche)
        self.robot.set_motor_dps(self.robot.MOTOR_right,dps_droite) 

    def get_distance_devant(self) -> float:
        """
        Sortie:
            - (Fonction a nettoyer)
            - distance_devant(robot. : float
              Valeur du capteur de distance (distance en milimètres : 2m, 2000mm max)
        """
        #On lit le capteur de distance du robot, qui renvoie distance entière en milimètre,
        distance_devant= self.robot.get_distance()
        #A voir dans doc de la classe, mais ici l'intervalle est de **5-8,000** millimeters.
        #Lorsque la valeur est en dehors de l'intervalle, le retour est **8190** 
        # Autrement dit si distance devant < 5  ou distance_devant > 8000 millimeters (0.005 et 8mètres respectivement)
        if distance_devant == 8190:
            #deux options je vous laisse choisir pour implementation:
            #si objet très proche <5mm dans réel:
            #return 0.0 ? je sais pas mais dans 
            #si on suppose trop loin, cas par défaut pour rafraichissement tick
            return 8.0
        return distance_devant/1000.0

    def reset_distance_parcourue(self):
        """Réinitialise les références de distance pour le calcul de la distance parcourue."""
        #get_motor_position renvoie un couple (degré,degré)
        encodeurs=self.robot.get_motor_position()
        self._ref_pos_gauche_distance = encodeurs[0]
        self._ref_pos_droite_distance = encodeurs[1]

    def get_distance_parcourue(self) -> float:
        """Calcule la distance parcourue depuis le dernier reset."""
        rayon = self.robot.WHEEL_DIAMETER / 2.0 # On recupere le rayon de la roue (diamètre/2)

        #get_motor_position renvoie un couple (degré,degré)
        encodeurs=self.robot.get_motor_position()                   
        delta_gauche = encodeurs[0] - self._ref_pos_gauche_distance
        delta_droite = encodeurs[1] - self._ref_pos_droite_distance
        
        #distance = angle * rayon (ici on convertit dégrés en radian pour distance metres)
        distance_gauche = delta_gauche * (math.pi / 180) * rayon
        distance_droite = delta_droite * (math.pi / 180) * rayon
        #on retourne la distance moyenne parcourue par les deux roues
        return abs(distance_gauche + distance_droite) / 2

    def reset_angle_parcouru(self):
        pass

    def get_angle_parcouru(self) -> float:
        pass

    def est_en_collision(self) -> bool:
        """ Indique si le robot est en collision en se basant sur la distance devant et un seuil de collision."""
        SEUIL_COLLISION = 0.2 #ici on met notre seuil voulu
        if self.get_distance_devant() < SEUIL_COLLISION: 
            return True
        return False