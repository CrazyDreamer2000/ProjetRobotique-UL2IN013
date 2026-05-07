from .algo_polygone_safe import AlgoPolygoneSafe
from .algo_foncer_devant import AlgoFoncerDevant
from .primitives import AvancerDistance

# Algorithmes
ALGOS = {
            "polygone" : AlgoPolygoneSafe,
            "avancer" : AvancerDistance,
            "foncerdevant" : AlgoFoncerDevant
        }
