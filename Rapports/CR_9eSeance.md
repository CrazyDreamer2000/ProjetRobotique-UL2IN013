
---

# **Compte rendu n°9 – Séance UL2IN013 – Projet de développement**  
**Date : 01/04/2026**

## **1. Déroulement de la séance**
Au cours de cette session, chaque membre de l’équipe a présenté la partie du code qu’il avait implémentée.  
Cela a permis d’assurer une compréhension collective des avancées du projet.

Un travail de **nettoyage**, de **réorganisation** et de **mise en commentaire** du code a été réalisé afin d’améliorer sa lisibilité et de faciliter la maintenance par l’ensemble de l’équipe.

---

## **2. Travail sur les stratégies**

Une discussion a été menée concernant les améliorations possibles de la gestion des stratégies.  
Une *feuille de changements* a été rédigée, comprenant notamment :

- Mise en place d’une **stratégie conditionnelle** liée à la gestion des collisions.  
- Création d’une **classe `Boucle`** permettant :
  - de paramétrer une stratégie,
  - de définir un nombre de répétitions,
  - d’exécuter automatiquement la stratégie *n* fois.

La stratégie conditionnelle pour les collisions reposera sur une instruction de type `if`.

Il a également été décidé que dans la primitive **`Evitercollision`**,  
la vérification de l’état de collision ne doit plus être effectuée.  
Cette vérification sera désormais gérée **dans la stratégie conditionnelle**,  
tandis que la primitive ne contiendra que les comportements à exécuter *en cas de collision*.

---

## **3. Notes techniques du 01/04 : points complémentaires**

- Suppression des algorithmes dont le nom commence par une majuscule afin d’uniformiser le code.  
- Remplacement de `traducteur_new` dans les primitives pour améliorer la cohérence et la maintenance.  
- Création de la stratégie **`Boucle`** pour gérer toutes les séquences répétitives (ex. : dessin de formes géométriques), rendant obsolètes les classes dédiées à chaque figure.  
- Début de la gestion des **cas à éviter**, encore en cours de définition.  
- Fonctionnement de la classe `Boucle` :
  - prend en paramètres le nom de la stratégie et le nombre de répétitions,
  - répète la stratégie jusqu’à atteindre le seuil fixé.
- Généralisation de la solution pour les formes : la classe `Boucle` devient une approche universelle pour toutes les répétitions.  
- Mise en place d’une **stratégie conditionnelle à N paramètres** :  
  selon le résultat d’une fonction, exécuter la stratégie 1 ou la stratégie 2, permettant une gestion plus fine des comportements.

---

## **4. Mise à jour de Trello et répartition des nouvelles tâches**

Le tableau Trello a été mis à jour pour refléter les décisions prises lors de la réunion technique du 01/04.  
Les nouvelles tâches ajoutées incluent :

- suppression ou remplacement de certains algorithmes,
- création et intégration de la stratégie `Boucle`,
- uniformisation du code,
- amélioration de la maintenance,
- gestion des cas à éviter,
- application de la solution `Boucle` aux formes répétitives.

La répartition des tâches permet à chaque membre de savoir précisément ce qu’il doit faire, facilitant ainsi le suivi global du projet.

---
