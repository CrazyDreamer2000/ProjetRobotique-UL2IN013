- Faire en sorte que le robot ait des collisions fonctionnelles peu importe sa forme et ses dimensions
- Meilleure organisation du code: chaque truc dans son fichier
- BONNE séparation entre simulation et controle: partie controle doit être inchangée quasi quand on met simulation 3D ou vrai robot sur partie simulation
- Un proxy/API (?) qui assure qu'on envoie les mêmes commandes vers le robot simulateur et le robot réel, et qui assure qu'ils font la même chose

Comment modifier code pour avoir tous les changements nécessaires/benefiques du cours 4 ?
modifier structure algos (cours 4)
THREADING pour l'affichage ?



--- NOTES DU 24/02 ---


- on a besoin d'un code MINIMAL et SIMPLE
- controlleur qui controlle tout: réutilisable dans le vrai robot (regarder Strategie: bonne solution dans cours4 / Strategie sequentielle dans Mix)
- stratégie séquentielle / mixer strategies (avec conditionnelle) pour interruptions de strategie
    - a chaque itération du controlleur (a voir), tester conditions pour autres stratégies, utiliser des LOCK pour interrompre d'autres strategies 
- ON A une API donné par le PROF
- DANS ALGOS: UTILISER LES FONCTIONS DE L'API ET FAIRE UN TRADUCTEUR POUR QUE LA SIMULATION ET LE ROBOT COMPRENNE  (Traducteur = proxy)
    - avoir mêmes signatures / fonctions pour simu et irl ne sert a rien (prof) ...
    - traducteur sim  et  traducteur irl  (avec mêmes signatures de fonctions, d'apres prof)
- definir blocs de base stratégie:
    - StratAvancer, StratTourner, Strat... (-> langage de haut niveau)
    - ./algos et ./stratégies ?

Idées pour la prochaine fois (bonus)
- afficher roues sur simulateur
- utiliser config du prof


--- pour après les vacances ---

