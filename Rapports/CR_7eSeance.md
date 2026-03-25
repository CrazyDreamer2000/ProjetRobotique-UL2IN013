
---

# Compte rendu n°7 – Séance UL2IN013  
## Projet de développement

## Fiche des changements à apporter pour la semaine prochaine

###  Gestion du paramètre `dt`
- `dt` doit être défini **en secondes**, pas en fonction du clock tick.  
- Le paramètre `dt` doit être **local à la fonction `step`**.

---

### Réorganisation du code principal (`main`)
- Environ **75 % du code** actuellement dans `main` doit être déplacé dans d’autres modules.  
- Le **dictionnaire des algorithmes** doit être déplacé dans le module `controle` ou `init`.  
- L’initialisation de **pygame** doit être faite dans le module **affichage**.  
- La **création du monde** doit être gérée ailleurs si possible.  
- La **gestion des événements pygame** doit être sortie du `main`.  
- La fonction `display` doit appartenir au module **affichage**.

---

### Module d’affichage
- Il n’est **pas nécessaire** de passer `screen`, `monde`, etc. en paramètres.

---

### Algorithmes
- `algo.step` doit envoyer **directement** les commandes au robot.  
- Ne pas passer `monde` et `dt` au robot : `dt` est calculé localement.  
- À l’initialisation d’un algorithme, le robot est donné **une seule fois**.  
- Les méthodes `start` et `step` de l’algorithme de base **ne prennent aucun paramètre**.  
- La méthode `stop` (algo/prim) doit tester les **conditions d’arrêt** des primitives.  
- Il ne doit y avoir **aucun retour** dans `start` et `step`.

---

### Considérations générales
- Le monde doit appeler `robot.step` lors de `monde.step` pour mettre à jour les capteurs.  
- Une classe héritée de `screen` doit être créée (hérite de la fenêtre + méthodes utiles).

---

### Traducteurs
- Chaque attribut doit avoir une **fonction correspondante** dans le traducteur.  
- Le traducteur peut accéder aux **attributs réels**.  
- Une **classe abstraite `Traducteur`** doit être définie.  
- Le traducteur communique avec le **contrôleur** (ex : obtenir la distance).

---

### Répartition des tâches
- Mettre à jour la répartition des tâches sur **Trello**.

---

## Explications et discussions techniques

### Gestion des collisions avec SAT
- Le code utilise l’algorithme **SAT (Separating Axis Theorem)** pour détecter les collisions entre polygones convexes.  
- Le principe : projeter les sommets sur plusieurs axes et vérifier s’il existe un **axe de séparation**.  
- S’il existe → pas de collision.  
- S’il n’existe pas → collision.  
- Le code implémente les projections, compare les intervalles et conclut selon la présence ou non d’un axe séparateur.

---

### Stratégies : primitives, compositions, séquences
- **Primitives** : comportements de base.  
- **Compositions** : assemblages de primitives pour créer des comportements plus complexes.  
- **Séquences** : organisation ordonnée des primitives/compositions pour gérer le flux d’actions.

---

### Structure de la partie « Contrôle »
- Objectif : organiser efficacement la gestion des commandes et interactions.  
- Le module contrôle centralise les mécanismes permettant de coordonner les stratégies et d’assurer le bon déroulement des actions.

---
