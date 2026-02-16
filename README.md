# 📊 BI E-Commerce Multicanal - Projet Complet

**Analyse des performances commerciales et comportement client d'un business e-commerce multicanal**

---

## 📑 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Structure du Projet](#structure-du-projet)
3. [Démarrage Rapide](#démarrage-rapide)
4. [Générer les Données](#générer-les-données)
5. [Architecture Dimensionnelle](#architecture-dimensionnelle)
6. [Phases de Réalisation](#phases-de-réalisation)
7. [Documentation](#documentation)
8. [Outils & Technologies](#outils--technologies)

---

## Vue d'Ensemble

Ce projet est une solution complète de **Business Intelligence** pour une entreprise e-commerce opérant sur plusieurs canaux (Web, Mobile, Pop-Up, Réseaux Sociaux).

### 🎯 Objectifs Principaux

| Objectif         | Description                                |
| ---------------- | ------------------------------------------ |
| **Intégration**  | Fusionner données de plusieurs canaux      |
| **Modélisation** | Créer un schéma dimensionnel robuste       |
| **Analyse**      | Analyser ventes, retours, satisfaction     |
| **Prédiction**   | Segmenter clients, prévoir churn           |
| **Décision**     | Créer dashboards pour la prise de décision |

### 📈 Périmètre

- **Période couverte** : 2022-01-01 à 2024-02-15
- **Clients** : 10,000 profils
- **Produits** : 500 références (20 catégories)
- **Commandes** : 50,000 transactions
- **Canaux** : Web (50%), Mobile (35%), Pop-Up (10%), Réseaux Sociaux (5%)
- **Régions** : 13 régions françaises
- **Localisation** : France

---

## Structure du Projet

```
BI2/
│
├── 📄 README.md                          ← Vous êtes ici
│
├── 📋 PROJECT_IMPLEMENTATION_PLAN.md     Planification détaillée
├── 📊 DATA_MODEL.md                      Architecture dimensionnelle
│
├── 🐍 generate_data.py                   Script de génération de données
├── 🗄️ setup_database.sql                 Script de création de base de données
│
├── 📁 data/
│   ├── raw/                              Fichiers CSV bruts générés
│   │   ├── customers.csv                 10,000 clients
│   │   ├── products.csv                  500 produits
│   │   ├── channels.csv                  4 canaux
│   │   ├── regions.csv                   13 régions
│   │   ├── orders.csv                    50,000 commandes
│   │   ├── returns.csv                   ~3,500 retours
│   │   └── feedback.csv                  ~35,000 retours client
│   ├── processed/                        (À venir) Données nettoyées par ETL
│   └── warehouse/                        (À venir) Data warehouse chargé
│
├── 📁 etl/
│   ├── transformations/                  Fichiers Pentaho KTR
│   │   ├── ETL_1_Load_Customers.ktr
│   │   ├── ETL_2_Load_Products.ktr
│   │   ├── ETL_3_Load_Channels.ktr
│   │   ├── ETL_4_Load_Regions.ktr
│   │   ├── ETL_5_Load_Sales.ktr
│   │   └── ETL_6_Load_Returns_Feedback.ktr
│   └── jobs/
│       └── Master_Job.kjb                Orchéstration des ETLs
│
├── 📁 olap/
│   ├── mondrian/
│   │   ├── ecommerce_schema.xml          Schéma du cube OLAP
│   │   └── olap_analysis.xml             Configuration analytique
│   └── queries/
│       ├── top_products.mdx
│       ├── revenue_analysis.mdx
│       ├── customer_segments.mdx
│       └── regional_performance.mdx
│
├── 📁 datamining/
│   ├── rfm_analysis.py                   Analyse RFM et segmentation
│   ├── churn_prediction.py               Modèle prédictif churn
│   ├── association_rules.py              Regroupement de produits
│   └── results/                          Résultats d'analyse
│
├── 📁 visualization/
│   ├── dashboards/
│   │   ├── Dashboard_Sales.pbix          (Power BI)
│   │   ├── Dashboard_Regions.pbix
│   │   ├── Dashboard_Customers.pbix
│   │   └── Dashboard_Channels.pbix
│   └── reports/
│
├── 📁 docs/
│   ├── BI_Project.md                     (Original) Cahier des charges
│   ├── Data_Model.md                     Modèle de données
│   ├── ETL_Documentation.md              (À venir) Guide ETL
│   ├── MDX_Queries.md                    (À venir) Requêtes analytiques
│   └── Technical_Report.md               (À venir) Rapport technique
│
└── 📁 scripts/
    ├── load_csv_to_db.py                 Charger CSVs en base
    ├── generate_time_dimension.sql       Générer calendrier
    └── create_indexes.sql                Créer indexes
```

---

## 🚀 Démarrage Rapide

### Étape 1 : Installer les Dépendances

```bash
# Vérifier Python 3.8+ installé
python --version

# Installer les packages requis
pip install faker pandas numpy
```

**Dépendances** :

- `faker` : Générateur de données réalistes
- `pandas` : Manipulation de données
- `numpy` : Calculs numériques

### Étape 2 : Générer les Données Synthétiques

```bash
# Aller au dossier du projet
cd c:\Users\Small\Desktop\vs\BI2

# Lancer le script de génération
python generate_data.py
```

**Résultat** : Les fichiers CSV sont créés dans `data/raw/`

```
✓ customers.csv (10,000 rows)
✓ products.csv (500 rows)
✓ channels.csv (4 rows)
✓ regions.csv (13 rows)
✓ orders.csv (50,000 rows)
✓ returns.csv (~3,500 rows)
✓ feedback.csv (~35,000 rows)
```

### Étape 3 : Créer la Base de Données

**Option A : MySQL/MariaDB**

```bash
mysql -u root -p < setup_database.sql
```

**Option B : PostgreSQL**

Adapter le script SQL pour PostgreSQL (syntaxe SERIAL, CURRENT_TIMESTAMP, etc.)

**Option C : SQLite** (Pour développement local)

```python
import sqlite3
import pandas as pd

# Charger les CSVs dans SQLite
conn = sqlite3.connect('ecommerce_bi.db')

for table_name in ['customers', 'products', 'channels', 'regions', 'orders', 'returns', 'feedback']:
    df = pd.read_csv(f'data/raw/{table_name}.csv')
    df.to_sql(f'fact_{table_name}', conn, if_exists='replace', index=False)

conn.close()
```

### Étape 4 : Configurer Pentaho PDI (ETL)

1. **Télécharger Pentaho Data Integration** : https://sourceforge.net/projects/pentaho/files/
2. **Créer les transformations** (voir dossier `etl/transformations/`)
3. **Charger les données** dans le Data Warehouse

### Étape 5 : Mettre en Place le Cube OLAP (Mondrian)

1. **Configurer Saiku Analytics** ou **Mondrian**
2. **Charger le schéma** : `olap/ecommerce_catalog.xml`
3. **Choisir la source OLAP selon la base** :
  - MySQL : `olap/saiku-datasource.properties` + `olap/mondrian.properties`
  - PostgreSQL : `olap/saiku-datasource-postgres.properties` + `olap/mondrian-postgres.properties`
4. **Exécuter des requêtes MDX**

### Étape 6 : Data Mining et Analyse

```bash
# Analyse RFM
python datamining/rfm_analysis.py

# Prédiction Churn
python datamining/churn_prediction.py

# Regroupements Produits
python datamining/association_rules.py
```

### Étape 7 : Créer les Dashboards

Utiliser **Power BI**, **Tableau** ou **Pentaho Report Designer** pour visualiser les résultats.

---

## 📊 Générer les Données

### Détails du Script `generate_data.py`

Le script génère des données réalistes avec les caractéristiques suivantes :

#### 🎲 Données Clients (10,000)

```python
- CustomerID : Identifiant unique
- Segment : Nouveau (25%), Régulier (50%), Fidèle (25%)
- Registration Date : Répartis sur toute la période
- Email, City, Postal Code : Données Faker
```

#### 🛍️ Données Produits (500)

```python
- ProductID : Unique
- Category : 20 catégories (électronique, mode, beauté, etc.)
- Price : Distribution lognormale (€10 - €5,000)
- Supplier : Entreprises générées
- Stock : 0-500 unités
```

#### 📦 Données Commandes (50,000)

```python
- OrderID : Unique
- Date : 2022-2024
- Canal : Web (50%), Mobile (35%), Pop-Up (10%), Réseaux Sociaux (5%)
- Revenue : Dépend du canal
  - Web : €75-150
  - Mobile : €50-100
  - Pop-Up : €100-250
  - Réseaux Sociaux : €30-80
- Discount : 10% de chance d'appliquer 10% de remise
```

#### 🔄 Données Retours (~3,500)

```python
- Taux de retour par canal :
  - Web : 8%
  - Mobile : 6%
  - Pop-Up : 12%
  - Réseaux Sociaux : 15%
- Raisons : Produit défectueux, mauvaise taille, etc.
```

#### ⭐ Feedback Client (~35,000)

```python
- Satisfaction : 1-5 (inverse au délai)
- 70% des clients donnent un avis
```

### Personnaliser la Génération

Modifier les constantes en haut de `generate_data.py` :

```python
NUM_CUSTOMERS = 10000         # Augmenter/diminuer
NUM_PRODUCTS = 500
NUM_ORDERS = 50000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 2, 15)
```

---

## 🏗️ Architecture Dimensionnelle

### Schéma en Étoile (Star Schema)

```
                           FACT_ORDERS
                            (50,000)
                                |
        ________________________|________________________
        |          |          |        |        |        |
    DIM_TIME   DIM_PRODUCT  DIM_CHANNEL  DIM_CUSTOMER  DIM_REGION
    (1,107)      (500)        (4)       (10,000)      (13)
```

### Tables Principales

| Table             | Lignes | Rôle                      |
| ----------------- | ------ | ------------------------- |
| **FACT_ORDERS**   | 50,000 | Transactions de vente     |
| **FACT_RETURNS**  | 3,500  | Retours et remboursements |
| **FACT_FEEDBACK** | 35,000 | Satisfaction client       |
| **DIM_TIME**      | 1,107  | Calendrier                |
| **DIM_PRODUCT**   | 500    | Catalogue produits        |
| **DIM_CHANNEL**   | 4      | Canaux de vente           |
| **DIM_CUSTOMER**  | 10,000 | Profils clients           |
| **DIM_REGION**    | 13     | Régions géographiques     |
| **DIM_DELIVERY**  | 4      | Méthodes de livraison     |

### Mesures Calculées

```
- Revenue = SUM(Revenue)
- Quantity = SUM(Quantity)
- Average Basket = Revenue / Order Count
- Return Rate = COUNT(Returns) / COUNT(Orders) * 100
- Satisfaction = AVG(Satisfaction Score)
- Customer Lifetime Value = SUM(Revenue) par Customer
```

---

## ⏭️ Phases de Réalisation

### Phase 1 : Modélisation ✅ (Complété)

- [x] Schéma dimensionnel conçu
- [x] Diagramme ER validé
- [x] Tables dimensionnelles identifiées
- [x] Mesures et KPIs définis

**Livrables** : `DATA_MODEL.md`, `setup_database.sql`

### Phase 2 : Génération de Données ✅ (Complété)

- [x] Script Python créé
- [x] Données synthétiques générées (50,000 orders)
- [x] Fichiers CSV préparés
- [x] Validation de qualité

**Livrables** : `generate_data.py`, fichiers CSV

### Phase 3 : Intégration ETL 🔄 (À Faire)

- [ ] Transformations Pentaho créées
- [ ] Validation des données
- [ ] Chargement en data warehouse
- [ ] Tests de réconciliation

**Durée estimée** : 5 jours

### Phase 4 : Cube OLAP 🔄 (À Faire)

- [ ] Schéma Mondrian conçu
- [ ] Dimensions et mesures configurées
- [ ] Hiérarchies définies
- [ ] Cube déployé

**Durée estimée** : 4 jours

### Phase 5 : Requêtes MDX 🔄 (À Faire)

- [ ] 10+ requêtes métiers rédigées
- [ ] Analyses complètes
- [ ] Documentation des requêtes
- [ ] Tests de performance

**Durée estimée** : 3 jours

### Phase 6 : Data Mining 🔄 (À Faire)

- [ ] Analyse RFM (Segmentation)
- [ ] Prédiction Churn (Classification)
- [ ] Association Rules (Cross-selling)
- [ ] Modèles validés

**Durée estimée** : 5 jours

### Phase 7 : Visualisation 🔄 (À Faire)

- [ ] Dashboards créés (4 principaux)
- [ ] KPIs mis en place
- [ ] Filtres interactifs configurés
- [ ] Tests utilisateur

**Durée estimée** : 4 jours

---

## 📚 Documentation

### Documents Existants

| Document                           | Contenu                      |
| ---------------------------------- | ---------------------------- |
| **README.md** (ce fichier)         | Guide complet du projet      |
| **PROJECT_IMPLEMENTATION_PLAN.md** | Plan détaillé de réalisation |
| **DATA_MODEL.md**                  | Architecture dimensionnelle  |
| **BI_Project.md**                  | Cahier des charges original  |
| **DOCKER_FULL_ENVIRONMENT.md**     | Environnement Docker/Podman complet |

### Documents À Créer

| Document                   | Contenu                           | Priorité |
| -------------------------- | --------------------------------- | -------- |
| **ETL_Documentation.md**   | Guide des transformations Pentaho | Haute    |
| **MDX_Queries.md**         | Requêtes analytiques MDX          | Haute    |
| **Technical_Report.md**    | Rapport technique complet         | Moyenne  |
| **Data_Quality_Report.md** | Résultats nettoyage/validation    | Moyenne  |
| **Mining_Report.md**       | Résultats analyses prédictives    | Basse    |

---

## 🛠️ Outils & Technologies

### Stack Technologique Complet

| Composant           | Outil                   | Version | Rôle                          |
| ------------------- | ----------------------- | ------- | ----------------------------- |
| **Backend**         | Python                  | 3.8+    | Scripts ETL et data mining    |
| **Database**        | MySQL/PostgreSQL/SQLite | Latest  | Stockage donnees              |
| **ETL**             | Pentaho PDI             | 9.0+    | Intégration et transformation |
| **OLAP**            | Mondrian/Saiku          | Latest  | Cube analytique               |
| **Visuals**         | Power BI / Tableau      | Latest  | Dashboards                    |
| **Version Control** | Git                     | -       | Gestion code                  |
| **IDE**             | VS Code                 | Latest  | Développement                 |

### Bibliothèques Python Principales

```
faker              - Génération de données réalistes
pandas             - Manipulation DataFrames
numpy              - Calculs numériques
scikit-learn       - Machine Learning
matplotlib         - Visualizations
seaborn            - Statistical plots
sqlalchemy         - ORM de base de données
```

---

## 📞 Support & Contribution

### Questions Fréquentes

**Q : Comment augmenter le volume de données ?**

A : Modifier `NUM_ORDERS` dans `generate_data.py` et relancer.

**Q : Puis-je utiliser d'autres sources de données ?**

A : Oui, adapter les connecteurs ETL Pentaho pour CSV, BBDD, APIs.

**Q : Quels sont les KPIs essentiels ?**

A : Revenue, Avg Basket, Return Rate, Satisfaction, Churn Risk, CLV.

### Prochaines Actions Recommandées

1. ✅ Générer les données synthétiques
2. ⏳ Créer la base de données
3. ⏳ Mettre en place les transformations ETL
4. ⏳ Configurer le cube OLAP
5. ⏳ Développer les analyses prédictives
6. ⏳ Créer les dashboards de visualisation

---

## 📋 Checklist de Déploiement

```
[ ] Données synthétiques générées ✅
[ ] Base de données créée
[ ] ETL Pentaho configuré
[ ] Cube OLAP déployé
[ ] Requêtes MDX validées
[ ] Modèles data mining entraînés
[ ] Dashboards créés
[ ] Tests complets réalisés
[ ] Documentation finalisée
[ ] Présentation client préparée
[ ] Code source poussé sur GitHub
```

---

## 📄 Licence & Mentions

**Projet** : Analyse BI E-commerce Multicanal
**Auteur** : BI Project Team
**Date de Création** : Février 2026
**Localisation** : France
**Langue** : Français

---

## 🎓 Ressources Complémentaires

### Tutoriels & Documentation

- [Pentaho PDI Documentation](https://help.pentaho.com/)
- [Mondrian Documentation](https://mondrian.pentaho.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

### Données Supplémentaires

- [Kaggle E-Commerce Datasets](https://www.kaggle.com/datasets)
- [UCI Machine Learning](https://archive.ics.uci.edu/ml/)
- [Mockaroo](https://www.mockaroo.com/) - Générateur de données

---

## 📞 Contact & Support

Pour toute question concernant ce projet :

- 📧 Team Contact : [À définir]
- 📚 Documentation : Voir dossier `/docs`
- 🐛 Issues : Signaler sur GitHub Issues

---

**Dernière mise à jour** : 15 février 2026

✨ **Bon courage sur votre projet BI !** ✨
