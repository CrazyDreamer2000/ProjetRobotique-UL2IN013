
# **Compte rendu n°6 – Séance LU2IN013**

**Séance n°6**  
**Date : 25/02/2026**

---

## **1. Ordre du jour**

- Redéfinition de la gestion des collisions via un polygone et utilisation de la méthode **SAT (Separating Axis Theorem)**.  
- Organisation du travail : mise à jour du **Trello** et définition de nouvelles tâches.  
- Restructuration du projet conformément aux attentes du **cours 4**.  

---

## **2. Discussions et décisions**

### **2.1. Gestion des collisions (méthode SAT)**  
Le groupe a travaillé sur une nouvelle approche de la gestion des collisions :  
- Passage à une représentation par **polygones**.  
- Utilisation du **Separating Axis Theorem** pour détecter les collisions.  
- Début d’intégration de cette méthode dans le moteur de simulation.

---

### **2.2. Restructuration du projet (selon le cours 4)**  
Une discussion approfondie a permis de définir une nouvelle architecture du projet.  
Les points retenus :

- **Simplification du code** : conserver uniquement les éléments essentiels.  
- Création d’une classe **`Algorithme`** contenant les méthodes :  
  - `start()`  
  - `step()`  
  - `stop()`  
- Mise en place de **classes de stratégie** (ex. : avancer, tourner…).  
- Déplacement de la **boucle principale** dans le contrôleur.  
- Utilisation de **threads** pour séparer :  
  - l’affichage,  
  - la mise à jour de la simulation.  
- Développement et intégration de **tests unitaires**.  
- Réflexion sur une nouvelle **arborescence du projet** :  
  - séparation des modules *monde* et *collisions*,  
  - création de dossiers dédiés au contrôle et à la simulation.  
- Début de réflexion sur l’implémentation d’un **traducteur** pour :  
  - la simulation,  
  - le robot réel.

---

### **2.3. Organisation du travail**  
- Mise à jour du **Trello**.  
- Attribution de nouvelles tâches à chaque membre du groupe.  

---
