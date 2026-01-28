
----------

# COMPTE RENDU n°2

**Séance LU2IN013** **Date :** 28 janvier 2026

----------

## 1. État d'avancement du projet

Le projet de **simulateur de mouvement de robot** a franchi une étape majeure aujourd'hui.

### Présentation et démonstration

-   Réalisation de la **première démonstration** du simulateur.
    
-   Validation des premières fonctionnalités intégrées.
    
-   Définition d'un **code de base** solide, destiné à être enrichi et amélioré au fil des séances.
    

----------

## 2. Développement Technique & Mises à jour

L'effort s'est concentré sur la précision physique du robot et la sécurité des trajectoires.

### Gestion des limites

Développement de la fonction : `def control_depassement(self, surface)`.

> **Objectif :** Détecter si le robot sort des limites de la carte afin de garantir que le mouvement reste dans l'environnement simulé.

### Évolution de la classe `Robot`

-   **Cinématique :** Définition des vitesses angulaire et linéaire en fonction de la vitesse des roues (amélioration de la précision).
    
-   **Modélisation :** Implantation de la classe `Roue` pour une gestion individuelle de chaque composant.
    
-   **Dynamique :** Ajout de la fonction `update_position()` pour une mise à jour fluide de la position en temps réel.
    

----------

## 3. Organisation et Gestion de l'Équipe

### Ressources humaines

-   **Arrivée d'un nouveau membre** dans l'équipe, permettant une meilleure répartition de la charge de travail et une accélération du développement.
    

### Qualité du code

-   Début de la phase de **commentaires du code** pour assurer la maintenabilité et la compréhension mutuelle entre les membres.
    

### Suivi de projet (Trello)

-   Mise à jour du tableau **Trello**.
    
-   Vérification des tâches précédentes.
    
-   **Nouvelle répartition des tâches** établie suite à un entretien avec le professeur.
    

----------

## 4. Perspectives pour la prochaine séance

-   Amélioration continue du code de base.
    
-   Intégration des nouvelles fonctionnalités selon la répartition Trello.
    

----------

