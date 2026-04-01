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




---- NOTES DU 18/03 -----

- dt:
    - dt defini selon secondes, pas clock tick
    - Rendre le dt local à la fonction (step)
- main:
    - 3/4 du code dans main doit etre ailleurs
    - dict algo a reporter dans module controle / init
    - pygame init etc dans init de l'affichage
    - creation monde pq pas 
    - event pygame autre part
    - display fait partie de l'affichage
- affichage:
    - affichage pas besoin de passer screen monde etc en param
- algos:
    - algo.step envoie direct au robot les commandes
    - ne pas passer monde dans robot + dt pas la peine (calculé localement)
    - lors de init algo mettre robot , pas robot dans param a chaque fois
    - start prend rien, step prend rien (algo base)
    - stop (algo/prim) qui teste conditions d'arret des primitives
    - plus de retour dans start step 
- general:
    - monde.step pas robot.step ( mieux  robot step dans monde + maj capteur)
    - obligé de créer une classe qui herite de screen (heritGe de la fenetre et toutes les methodes quon veut a l'interieur) -> ?
- traducteurs: notes
    - traducteurs: partout ou ya attribut ya fonction du traducteur (pas de difference traducteur / robot) juste au niveau de strategie
    - traducteur lui pourra accéder aux attributs reels
    - classe abstraite traducteur
    - traducteur parle au controlleur ( get distance, etc)

Tout ca pour la semaine prochaine !


----


tout seul:
a faire:
- monde.step
- super().step() termine la fonction quand appelée
- 


NOTES du 25/03:

- alex: gitignore pour pas mettre cache
- changer et simplifier main davantage (photo) + utiliser adaptateurs (pr simu / reel) (?)
- sequence trop complique, bcp de code qui se repete
- enlever self.fini, remplacer seulement par stop()
- BCP a simplifier
- dans primitive, calculs de angle et distance etc pas bien, pas a etre la. Seule chose utile 
- maintenant: plus self.pos, mais distance parcourue depuis dernière fois. Pareil dans traducteur (se calcule differemment selon traducteur)
- clock.tick -> time.sleep (python)
- dt calcule temps entre appel de derniere fonction et maintenant , stocker dans variable de classe. Calculé LOCALEMENT
- dt local (temps depuis dernier appel) là où il y en a besoin: robot, maj_capteur

- strategie ne connaitra qu'un adapteteur, sias pas si robot ou simulé
- savoir distance parcourue dans simu et reel est different
- adaptateur fait pont

  NOTES du 01/04:

  - Virer les algos qui commencent par majuscule (rappel)
- Remplacer dans primitives l'utilisation de traducteur_new
- Comme sequence, faire strategie boucle, qui répète n fois stratégie (permet de faire carré,pentagone ou hexagone... )
- Cas éviter à traiter (vague), 
- Classe boucle(nom stratégie, nombre fois executé): 
- si pas dépassé, alors répéter
    - Plus besoin de classe pour carré (Plus général)

-Stratégie conditionelle qui prend deux stratégies en paramètre, si fonction vraie renvoie stratégie 1 sinon stratégie 2

-TME SOLO: LISTE EXERCICES:
mettre dans readme exos fait, exos pas fait, comme ça correcteur sait ce qu'on a fait et pas fait (nous avantage)

- dans controlleur: parle au robot reel


NOTES du 01/04 : A FAIRE 

• Généralisation des stratégies répétitives :

- Implémenter la classe Boucle avec deux paramètres principaux : nom de la stratégie à appliquer et nombre de répétitions.
- Permettre l’exécution répétée d’une stratégie pour dessiner des formes géométriques (carré, pentagone, hexagone, etc.) sans classe dédiée par figure.
- La boucle continue tant que le seuil de répétition n’est pas dépassé.
- Cette approche rend obsolète la création de classes spécifiques à chaque forme et simplifie la maintenance du code.
  
• Stratégies conditionnelles pour la gestion des collisions :

- Développer une stratégie conditionnelle prenant deux stratégies en paramètre.
- Selon le résultat d’une fonction (ex : test de collision), exécuter soit la stratégie 1, soit la stratégie 2.
- Permet une gestion fine des comportements selon les situations rencontrées.
- Dans la primitive Evitercollision, supprimer la vérification "si on est en collision ou pas"; cette vérification doit être gérée dans la stratégie conditionnelle.
- La primitive Evitercollision ne doit comporter que les comportements à appliquer en cas de collision.
  
• Suppression et remplacement d’éléments pour uniformisation :

Supprimer tous les algorithmes dont le nom commence par une majuscule pour garantir uniformité et lisibilité du code.

