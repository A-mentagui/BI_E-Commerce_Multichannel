# Plan d'implémentation - Projet BI E-commerce Multicanal

## 1. ANALYSE DU PROJET

### Objectifs Stratégiques

- **Intégration multi-canaux** : Web, Mobile, Pop-up, Réseaux sociaux
- **Optimisation des ventes** : Analyse par canal, produit, région, période
- **Segmentation client** : Profiling et prédiction comportementale
- **Prise de décision basée sur les données** : Dashboards interactifs

### Entités Métier Principales

1. **Commandes** : CA, quantité, date, canal, client, produit, lieu de livraison
2. **Clients** : Segment, récence, fréquence, montant (RFM), statut
3. **Produits** : Catégorie, prix, SKU
4. **Canaux** : Type de vente (Web, Mobile, Pop-up, Réseaux sociaux)
5. **Régions** : Localisation, segments géographiques
6. **Retours/Avis** : Satisfaction, taux de retour
7. **Trafic Web** : Visiteurs, sessions, conversions

---

## 2. PHASE 1 : MODÉLISATION DIMENSIONNELLE (Semaine 1)

### 2.1 Schéma en Étoile (Star Schema)

```
                        FACT_SALES
                            |
        ________________________|________________________
        |          |          |         |        |
    DIM_TIME  DIM_PRODUCT  DIM_CHANNEL  DIM_CUSTOMER  DIM_REGION
    DIM_DELIVERY_METHOD

Mesures :
- Revenue, Quantity, Returns_Rate, Average_Basket, Satisfaction_Score
```

### 2.2 Dimensions Détaillées

| Dimension        | Attributs                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------ |
| **DIM_TIME**     | DateKey, Date, Month, Quarter, Year, Weekday, Season                                       |
| **DIM_PRODUCT**  | ProductKey, ProductID, ProductName, Category, SubCategory, Price, Supplier                 |
| **DIM_CHANNEL**  | ChannelKey, ChannelID, ChannelName (Web, Mobile, PopUp, Social), ChannelType               |
| **DIM_CUSTOMER** | CustomerKey, CustomerID, Name, Segment (New, Regular, Loyal), RFM_Score, Registration_Date |
| **DIM_REGION**   | RegionKey, RegionID, RegionName, Country, Postal_Code, Area                                |
| **DIM_DELIVERY** | DeliveryKey, DeliveryMethod, DeliveryTime_Days, Cost                                       |

### 2.3 Faits (FACT_SALES)

```sql
FACT_SALES (
    SaleKey (PK),
    OrderID,
    TimeKey (FK) → DIM_TIME,
    ProductKey (FK) → DIM_PRODUCT,
    ChannelKey (FK) → DIM_CHANNEL,
    CustomerKey (FK) → DIM_CUSTOMER,
    RegionKey (FK) → DIM_REGION,
    DeliveryKey (FK) → DIM_DELIVERY,

    -- Measures
    Revenue (Additive),
    Quantity (Additive),
    Returns (Count),
    Satisfaction_Score (Average),
    Delivery_Status (Delivered/Delayed),
    Discount_Applied,
    Order_Date
)
```

---

## 3. PHASE 2 : GÉNÉRATION DES DONNÉES SYNTHÉTIQUES (Semaine 1-2)

### 3.1 Stratégie de Génération

**Outil** : Python + Faker + Pandas
**Volume** :

- 50,000 commandes
- 10,000 clients
- 500 produits
- 4 canaux
- 50 régions
- Période : 24 mois

### 3.2 Règles Métiers pour la Génération

1. **Distribution des canaux** : Web (50%), Mobile (35%), PopUp (10%), Social (5%)
2. **Panier moyen** :
   - Web : 75€-150€
   - Mobile : 50€-100€
   - PopUp : 100€-250€
   - Social : 30€-80€
3. **Taux de retour** : 5-15% selon le canal
4. **Satisfaction** : Inversement proportionnelle au délai de livraison
5. **Segmentation client RFM** :
   - Loyal : High R, High F, High M
   - Regular : Medium scores
   - New : High R, Low F, Low M
6. **Produits** : 20 catégories × 25 produits par catégorie

### 3.3 Fichiers de Sortie CSV

```
data/
├── customers.csv (CustomerID, Name, Email, Segment, RFM_Score, Registration_Date)
├── products.csv (ProductID, ProductName, Category, Price, Supplier)
├── channels.csv (ChannelID, ChannelName, ChannelType)
├── regions.csv (RegionID, RegionName, Country, Postal_Code)
├── orders.csv (OrderID, CustomerID, ProductID, ChannelID, RegionID, OrderDate, Revenue, Quantity)
├── returns.csv (ReturnID, OrderID, ReturnDate, Reason, ReturnRate)
├── feedback.csv (FeedbackID, OrderID, Satisfaction_Score, Comment)
└── deliveries.csv (DeliveryID, OrderID, DeliveryMethod, DeliveryTime_Days, DeliveryStatus)
```

---

## 4. PHASE 3 : INTÉGRATION ETL (Semaine 2-3)

### 4.1 Architecture Pentaho PDI

```
CSV Files → Transformation → Cleaning → Enrichment → Data Warehouse
    ↓
    ├─ (Extract) Load CSV
    ├─ (Transform) Data quality checks, normalization
    ├─ (Enrich) Add calculated fields, aggregate RFM
    ├─ (Load) Insert into DW tables
    └─ Job orchestration
```

### 4.2 Transformations Pentaho

1. **ETL_1_Load_Customers** : CSV → Dimension client avec RFM
2. **ETL_2_Load_Products** : CSV → Dimension produit
3. **ETL_3_Load_Channels** : CSV → Dimension canal
4. **ETL_4_Load_Regions** : CSV → Dimension région
5. **ETL_5_Load_Sales** : Fusion et agrégation (Orders + Returns + Feedback + Deliveries)
6. **Master_Job** : Orchestration des 5 transformations

### 4.3 Règles de Nettoyage

- Suppression des doublons
- Gestion des valeurs NULL
- Validation des formats
- Vérification des contraintes FK
- Détection des anomalies (CA < 0, quantité > seuil, etc.)

---

## 5. PHASE 4 : CUBE OLAP (Semaine 3-4)

### 5.1 Architecture Mondrian

```xml
<Schema name="EcommerceCube">
  <Cube name="SalesCube">
    <Dimension name="Time">
      <Hierarchy name="TimeLine">
        <Level name="Year" column="Year"/>
        <Level name="Quarter" column="Quarter"/>
        <Level name="Month" column="Month"/>
        <Level name="Day" column="Day"/>
      </Hierarchy>
    </Dimension>

    <Dimension name="Product">...</Dimension>
    <Dimension name="Channel">...</Dimension>
    <Dimension name="Customer">...</Dimension>
    <Dimension name="Region">...</Dimension>

    <Measure name="Revenue" aggregator="sum"/>
    <Measure name="Quantity" aggregator="sum"/>
    <Measure name="Return_Rate" aggregator="avg"/>
    <Measure name="Satisfaction" aggregator="avg"/>
    <Measure name="Avg_Basket" aggregator="avg"/>
  </Cube>
</Schema>
```

### 5.2 Mesures Calculées

- `Profit = Revenue * 0.35`
- `Return_Impact = Revenue * Return_Rate`
- `Customer_Lifetime_Value = SUM(Revenue) par Customer`
- `Churn_Risk = 1 if Recency > 90 days else 0`

---

## 6. PHASE 5 : REQUÊTES MDX (Semaine 4)

### 6.1 Top 5 Produits par Canal

```mdx
SELECT
{[Measures].[Revenue], [Measures].[Quantity]} ON COLUMNS,
HEAD(
ORDER(
[Product].[Product].MEMBERS,
[Measures].[Revenue],
DESC
), 5
) ON ROWS
FROM [SalesCube]
WHERE ([Channel].[Channel].currentMember)
```

### 6.2 Évolution CA par Région et Trimestre

```mdx
SELECT
[Time].[Time].[Quarter].MEMBERS ON COLUMNS,
[Region].[Region].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Measures].[Revenue]
```

### 6.3 Panier Moyen : Fidèles vs Nouveaux

```mdx
SELECT
{[Measures].[Avg_Basket]} ON COLUMNS,
{[Customer].[Segment].[Loyal], [Customer].[Segment].[New]} ON ROWS
FROM [SalesCube]
```

---

## 7. PHASE 6 : DATA MINING (Semaine 5)

### 7.1 Segmentation RFM

**Analyse** : Clustering avec K-means

- **Récence (R)** : Jours depuis dernière commande
- **Fréquence (F)** : Nombre de commandes
- **Montant (M)** : CA total par client

**Segmentation résultante** :

- Champions (R↑, F↑, M↑)
- Fidèles (R↑, F↑, M↑)
- À risque (R↓, F↓, M↓)
- Dormants (R↓, F↓, M↓)

### 7.2 Prédiction du Churn

**Modèle** : Random Forest
**Variables** :

- Récence, Fréquence, Montant
- Panier moyen
- Taux retour
- Satisfaction
- Jours depuis registration

**Cible** : Inactivité > 6 mois

### 7.3 Cross-selling

**Modèle** : Association Rules (Apriori/Eclat)
**Objectif** : Identifier produits fréquemment achetés ensembles
**Métrique** : Support, Confidence, Lift

---

## 8. PHASE 7 : VISUALISATION (Semaine 5-6)

### 8.1 Tableau de Bord - Ventes Globales

- KPI : Revenue, Orders, Avg Basket, Satisfaction
- Charts : Tendance CA, Distribution canal, Top 10 produits
- Filtres : Période, Canal, Région, Produit

### 8.2 Tableau de Bord - Analyse Régionale

- Carte géographique des ventes
- Évolution CA par région
- Livraison vs Retours par région

### 8.3 Tableau de Bord - Segments Client

- Distribution RFM
- Prédiction Churn
- Opportunités Cross-selling

### 8.4 Tableau de Bord - Canaux

- Performance par canal
- Conversion par canal
- Satisfaction par canal

---

## 9. TECHNOLOGIES & STACK

| Composant           | Technologie                                  |
| ------------------- | -------------------------------------------- |
| **Data Generation** | Python (Faker, Pandas, NumPy)                |
| **Data Storage**    | PostgreSQL / SQLite                          |
| **ETL**             | Pentaho PDI (Kettle)                         |
| **OLAP**            | Mondrian / Saiku Analytics                   |
| **Data Mining**     | Python (scikit-learn, pandas)                |
| **Visualisation**   | Power BI / Tableau / Pentaho Report Designer |
| **Version Control** | Git/GitHub                                   |

---

## 10. TIMELINE

| Phase              | Durée            | Livrables                       |
| ------------------ | ---------------- | ------------------------------- |
| 1. Modélisation    | 3 jours          | Schéma ER, DDL                  |
| 2. Data Génération | 2 jours          | Fichiers CSV                    |
| 3. ETL             | 5 jours          | Jobs/Transformations Pentaho    |
| 4. Cube OLAP       | 4 jours          | Schéma Mondrian, Data warehouse |
| 5. Requêtes MDX    | 3 jours          | 10+ requêtes métiers            |
| 6. Data Mining     | 5 jours          | Modèles + résultats             |
| 7. Visualisation   | 4 jours          | 4 Dashboards                    |
| **Total**          | **4-5 semaines** | **Rapport + Dashboards**        |

---

## 11. FICHIERS À CRÉER

```
BI2/
├── data/
│   ├── raw/                    # Fichiers source CSV
│   ├── processed/              # Données transformées
│   └── warehouse/              # Data warehouse
├── etl/
│   ├── transformations/        # Pentaho KTR files
│   ├── jobs/                  # Pentaho Jobs
│   └── scripts/               # Scripts de support
├── olap/
│   ├── mondrian/              # Fichiers de schéma
│   └── queries/               # Requêtes MDX
├── datamining/
│   ├── rfm_analysis.py
│   ├── churn_prediction.py
│   └── association_rules.py
├── visualization/
│   ├── dashboards/            # Fichiers dashboard
│   └── reports/
├── docs/
│   ├── BI_Project.md          # (existant)
│   ├── Data_Model.md
│   ├── ETL_Documentation.md
│   ├── MDX_Queries.md
│   └── Technical_Report.md
├── scripts/
│   └── generate_data.py       # Générateur de données
└── README.md
```

---

## 12. PROCHAINES ÉTAPES

1. ✅ **Créer le générateur de données synthétiques** (Python)
2. Générer les fichiers CSV
3. Configurer la base de données
4. Créer les transformations Pentaho
5. Construire le cube Mondrian
6. Valider avec requêtes MDX
7. Lancer analyses data mining
8. Créer dashboards
9. Documenter tout
10. Préparer présentation client
