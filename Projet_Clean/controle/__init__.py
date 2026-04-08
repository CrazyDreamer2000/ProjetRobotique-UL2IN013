#from .AlgoTournerSurPlace import AlgoTournerSurPlace
#from .AlgoArretDevantObstacle import AlgoArretDevantObstacle
#from .AlgoReculeTourneContact import AlgoReculeTourneContact
#from .AlgoEviter import AlgoEviter
from .algo_carre import AlgoCarre
from .algo_carre_safe import AlgoCarreSafe
from .algo_polygone_safe import AlgoPolygoneSafe

# Algorithmes
ALGOS = {
            "carre" : AlgoCarre,
            "carresafe" : AlgoCarreSafe,
            "polygone" : AlgoPolygoneSafe,
            #"tourner" : AlgoTournerSurPlace,
            #"eviter" : AlgoEviter,
            #"arret" : AlgoArretDevantObstacle,
            #"contact" : AlgoReculeTourneContact
        }
