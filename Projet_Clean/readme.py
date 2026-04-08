""" Questions traitées:

- 1.1 On a modifié dans le fichier monde.py à la définition de la classe, on a ajouté 3 obstacles (qui ne sont plus définis arbitrairement)
- Et pour le robot on a Changé dans main.py à l'apparition du robot sa position

-1.5 Si on veut on peut remplacer, par algo_polygone, il suffit de décommenter self nb_cotes dans la stratégie et dans le main.py (après on écrit manuellement ou input le nombre de cotés dans l'appel mais ici j'ai fait manuellement)
- remplacé (par facilité pas besoin) ficiher obsolete par algo_hexagone.py, dans parser j'ai ajouté sa définition et init aussi, et je l'ai défini comme algo par défaut
- 2.1 (modif affichage,monde.py et main)

"Questions non traitées:

-1.2: dans __init__ robot: self.stylo = "posé"
1.3 si on suppose 1.2 traitée, if b: self.stylo="posé" dans init 
else: self.stylo = "levé" (pour posé -> tracé et levé -> rien)
1.4: self.couleur = (r,g,b) dans init robot et self.couleur= couleur, qui est en argument de la fonction
2.2 Supposons que 1.2 traitée, il suffit d'utiliser stratégie par defaut pour robot1 (algo: carré allezretour) et d'y ajouter tracé, et pour robot2 allez retour c'est tout simplement avancer,tourner(pi), 2 fois + l'ajout du tracé (mais j'ai pas reussi à tracer...)
2.3 
2.4
2.5
2.6
 """
