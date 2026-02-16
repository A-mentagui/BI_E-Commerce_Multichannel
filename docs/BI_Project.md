# Analyse des performances commerciales et comportement client d’un business e-commerce multicanal

## Contexte

Une entreprise e-commerce souhaite optimiser ses ventes et mieux comprendre ses clients. Elle dispose de données issues de plusieurs canaux (site web, application mobile, pop-up, réseaux sociaux) et souhaite :

- Intégrer et nettoyer ces données
- Analyser les performances par type de canal, par canal, produit, région, période, segment client… L’entreprise s’intéresse tout particulièrement à analyser ses ventes, la livraison à domicile et la satisfaction client.
- Segmenter les clients et prédire leur comportement
- Visualiser les résultats pour la prise de décision

## Objectifs du projet

### 1.Modélisation

- Identifier les faits et les mesures appropriées pour évaluer toutes les facettes de l’activité de l’entreprise.
- Identifier les dimensions
- Réaliser un schéma dimensionnel.

### 2. Intégration des données (Pentaho PDI)

- Extraire, transformer et charger des données issues de fichiers CSV/Excel, site web, bases de données, ou APIs (simulées).
- Exemples de données : commandes, clients, produits, canaux de vente, retours, avis, trafic web.

### 3. Création d’un cube OLAP (Mondrian)

- Concevoir un schéma OLAP pour analyser les ventes selon plusieurs dimensions : temps, canal, produit, région, segment client.
- Définir des mesures : chiffre d’affaires, quantité vendue, taux de retour, panier moyen, etc.

### 4. Requêtes MDX

- Rédiger des requêtes MDX pour répondre à des questions métiers :
  - Quels sont les 5 produits les plus vendus par canal ?
  - Quelle est l’évolution du CA par région et par trimestre ?
  - Quel est le panier moyen des clients fidèles vs nouveaux ?

### 5. Analyse Datamining

- Segmenter les clients (RFM : Récence, Fréquence, Montant) ou utiliser un algorithme de clustering (k-means) pour identifier des profils types.

- Prédire le risque de désabonnement (churn) ou le potentiel de vente croisée (cross-selling) avec un modèle de classification (arbre de décision, random forest).

### 6. Visualisation des résultats

- Utiliser un outil comme Pentaho Report Designer, Tableau ou Power BI pour créer des tableaux de bord interactifs :
  - Carte des ventes par région
  - Évolution du CA par canal
  - Répartition des segments clients
  - Prédictions de churn

Où trouver ces données ?

- Génération automatique :
- Utiliser des outils comme Mockaroo ou Generatedata pour créer des datasets réalistes.
- Script Python avec Faker pour générer des données aléatoires.
- Datasets publics :
- Kaggle E-Commerce Datasets (ex : "E Commerce Dataset", "Online Retail")
- UCI Machine Learning Repository (ex : "Online Retail")
- Simulation :
- Créer un petit script pour simuler des commandes, clients, produits avec des règles métiers simples.

## Livrables attendus

- Un rapport technique décrivant le modèle dimensionnel, l’architecture ETL, le schéma OLAP, les requêtes MDX, et les modèles de datamining.
- Un tableau de bord interactif avec les principales analyses.
- Une présentation orale simulant un rendu client.
- Repo GitHub ou dossier compressé.
