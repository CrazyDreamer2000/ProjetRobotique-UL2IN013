from .AlgoTournerSurPlace import AlgoTournerSurPlace
from .AlgoArretDevantObstacle import AlgoArretDevantObstacle
from .AlgoReculeTourneContact import AlgoReculeTourneContact
from .AlgoEviter import AlgoEviter
from .algo_carre import AlgoCarre
from .algo_carre_safe import AlgoCarreSafe

# Algorithmes
ALGOS = {
            "carre" : AlgoCarre,
            "carresafe" : AlgoCarreSafe,
            "tourner" : AlgoTournerSurPlace,
            "eviter" : AlgoEviter,
            "arret" : AlgoArretDevantObstacle,
            "contact" : AlgoReculeTourneContact
        }