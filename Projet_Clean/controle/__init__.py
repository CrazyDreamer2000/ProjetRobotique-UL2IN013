from .algo_carre import AlgoCarre
from .algo_carre_safe import AlgoCarreSafe
from .algo_polygone_safe import AlgoPolygoneSafe
from .primitives import AvancerDistance

# Algorithmes
ALGOS = {
            "carre" : AlgoCarre,
            "carresafe" : AlgoCarreSafe,
            "polygone" : AlgoPolygoneSafe,
            "avancer" : AvancerDistance
        }
