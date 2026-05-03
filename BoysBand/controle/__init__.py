from .algo_carre import AlgoCarre
from .algo_carre_safe import AlgoCarreSafe
from .algo_polygone_safe import AlgoPolygoneSafe
from .algo_foncer_devant import AlgoFoncerDevant
from .primitives import AvancerDistance

# Algorithmes
ALGOS = {
            "carre" : AlgoCarre,
            "carresafe" : AlgoCarreSafe,
            "polygone" : AlgoPolygoneSafe,
            "avancer" : AvancerDistance,
            "foncerdevant" : AlgoFoncerDevant
        }
