#from .AlgoTournerSurPlace import AlgoTournerSurPlace
#from .AlgoArretDevantObstacle import AlgoArretDevantObstacle
#from .AlgoReculeTourneContact import AlgoReculeTourneContact
#from .AlgoEviter import AlgoEviter
from .algo_carre import AlgoCarre
from .algo_carre_safe import AlgoCarreSafe
from .algo_hexagone import AlgoHexagone
from .algo_aller_retour import AlgoAllerRetour

# Algorithmes
ALGOS = {
            "carre" : AlgoCarre,
            "carresafe" : AlgoCarreSafe,
            "hexagone" : AlgoHexagone,
            "allerretour" : AlgoAllerRetour,
            #"tourner" : AlgoTournerSurPlace,
            #"eviter" : AlgoEviter,
            #"arret" : AlgoArretDevantObstacle,
            #"contact" : AlgoReculeTourneContact
        }
