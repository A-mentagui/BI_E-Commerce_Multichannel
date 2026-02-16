# MDX Queries - Analyse OLAP

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Requêtes Commerciales](#requêtes-commerciales)
3. [Requêtes Géographiques](#requêtes-géographiques)
4. [Requêtes Clients](#requêtes-clients)
5. [Requêtes Produits](#requêtes-produits)
6. [Requêtes Avancées](#requêtes-avancées)
7. [KPIs et Mesures Calculées](#kpis-et-mesures-calculées)

---

## Vue d'ensemble

Les requêtes MDX (Multi-Dimensional Expressions) analysent le cube OLAP `SalesCube` selon plusieurs dimensions.

### Cube Structure

```
SalesCube
├─ Dimensions:
│  ├─ Time (Year→Quarter→Month→Day)
│  ├─ Product (Category→SubCategory→Product)
│  ├─ Channel (ChannelType→Channel)
│  ├─ Customer (Segment→Country→City→Customer)
│  ├─ Region (Region)
│  └─ Delivery (Delivery)
│
└─ Measures:
   ├─ Revenue
   ├─ Quantity
   ├─ Return_Rate
   ├─ Satisfaction
   ├─ Avg_Basket
   └─ Churn_Risk
```

---

## Requêtes Commerciales

### 1️⃣ Top 5 Produits par Canal

**Objectif** : Identifier les best-sellers par canal
**Utilisation** : Optimiser le mix produit par canal

```mdx
SELECT
  {[Measures].[Revenue], [Measures].[Quantity]} ON COLUMNS,
  HEAD(
    ORDER(
      [Product].[ProductHierarchy].MEMBERS,
      [Measures].[Revenue],
      DESC
    ), 5
  ) ON ROWS
FROM [SalesCube]
WHERE [Channel].[ChannelHierarchy].currentMember
```

**Variations** :

```mdx
-- Top 5 produits sur Web
SELECT ... 
WHERE [Channel].[ChannelHierarchy].[Web]

-- Top 5 produits sur Mobile
SELECT ... 
WHERE [Channel].[ChannelHierarchy].[Mobile]

-- Top 5 produits sur Pop-Up
SELECT ... 
WHERE [Channel].[ChannelHierarchy].[Pop-Up]
```

---

### 2️⃣ Évolution du Chiffre d'Affaires par Trimestre

**Objectif** : Analyser tendance CA trimestrielle
**Utilisation** : Planification budgétaire, détection saisonnalité

```mdx
SELECT
  [Time].[TimeHierarchy].[Year].MEMBERS ON COLUMNS,
  [Time].[TimeHierarchy].[Quarter].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Measures].[Revenue]
```

**Détail Mensuel** :

```mdx
SELECT
  [Time].[TimeHierarchy].[Month].MEMBERS ON COLUMNS,
  [Measures].[Revenue] ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

### 3️⃣ Revenue par Canal vs Satisfaction

**Objectif** : Corréler revenue et satisfaction par canal
**Utilisation** : Évaluer qualité du service par canal

```mdx
SELECT
  {[Measures].[Revenue], [Measures].[Satisfaction]} ON COLUMNS,
  [Channel].[ChannelHierarchy].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

### 4️⃣ Revenu Net (Revenue - Discount - Refunds)

**Objectif** : Calculer profit réel après remises et retours
**Utilisation** : Profitabilité réelle par segment

```mdx
WITH MEMBER [Measures].[Gross_Revenue] AS
  [Measures].[Revenue]
  
MEMBER [Measures].[Total_Refunds] AS
  SUM([Fact_Returns].[Return_Amount])
  
MEMBER [Measures].[Net_Revenue] AS
  [Measures].[Gross_Revenue] - [Measures].[Total_Refunds]

SELECT
  {[Measures].[Gross_Revenue], [Measures].[Total_Refunds], [Measures].[Net_Revenue]} ON COLUMNS,
  [Channel].[ChannelHierarchy].MEMBERS ON ROWS
FROM [SalesCube]
```

---

## Requêtes Géographiques

### 5️⃣ Performance par Région et Trimestre

**Objectif** : Analyser CA par région et période
**Utilisation** : Identification régions performantes/faibles

```mdx
SELECT
  [Time].[TimeHierarchy].[Quarter].MEMBERS ON COLUMNS,
  [Region].[RegionHierarchy].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Measures].[Revenue]
```

---

### 6️⃣ Taux de Retour par Région

**Objectif** : Identifier régions avec fort taux retour
**Utilisation** : Améliorer logistique régionale

```mdx
WITH MEMBER [Measures].[Return_Rate_Percent] AS
  ROUND(
    ([Measures].[Return_Count] / [Measures].[Order_Count]) * 100, 2
  )

SELECT
  [Measures].[Return_Rate_Percent] ON COLUMNS,
  [Region].[RegionHierarchy].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
ORDER BY CURRENT MEMBER ON ROWS DESC
```

---

### 7️⃣ Heatmap Régionale (Carte des Ventes)

**Objectif** : Visualiser distribution ventes géographiques
**Utilisation** : Planning expansion marché

```mdx
SELECT
  [Region].[RegionHierarchy].MEMBERS ON COLUMNS,
  [Measures].[Revenue] ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

## Requêtes Clients

### 8️⃣ Panier Moyen par Segment Client

**Objectif** : Comparer panier moyen entre segments
**Utilisation** : Stratégie prix, propositions commerciales

```mdx
WITH MEMBER [Measures].[Avg_Basket] AS
  [Measures].[Revenue] / [Measures].[Order_Count]

SELECT
  [Measures].[Avg_Basket] ON COLUMNS,
  [Customer].[CustomerHierarchy].[Segment].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

### 9️⃣ Revenu Cumulé par Segment Client (CLV)

**Objectif** : Customer Lifetime Value par segment
**Utilisation** : Segmentation valeur client

```mdx
WITH MEMBER [Measures].[Cumul_Revenue] AS
  SUM(
    [Time].[TimeHierarchy].MEMBERS,
    [Measures].[Revenue]
  )

SELECT
  [Measures].[Cumul_Revenue] ON COLUMNS,
  [Customer].[CustomerHierarchy].[Segment].MEMBERS ON ROWS
FROM [SalesCube]
```

**Variation - Top 10 Clients** :

```mdx
SELECT
  [Measures].[Revenue] ON COLUMNS,
  HEAD(
    ORDER(
      [Customer].[CustomerHierarchy].[Customer].MEMBERS,
      [Measures].[Revenue],
      DESC
    ), 10
  ) ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

### 🔟 Satisfaction par Segment

**Objectif** : Évaluer satisfaction par type client
**Utilisation** : Améliorer service pour segments spécifiques

```mdx
SELECT
  [Measures].[Satisfaction] ON COLUMNS,
  [Customer].[CustomerHierarchy].[Segment].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

## Requêtes Produits

### 1️⃣1️⃣ Top 10 Produits par Revenue

**Objectif** : Produits les plus rentables
**Utilisation** : Focus marketing, recommandations produits

```mdx
SELECT
  {[Measures].[Revenue], [Measures].[Quantity]} ON COLUMNS,
  HEAD(
    ORDER(
      [Product].[ProductHierarchy].[Product].MEMBERS,
      [Measures].[Revenue],
      DESC
    ), 10
  ) ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

### 1️⃣2️⃣ Produits par Catégorie

**Objectif** : Analyse par catégorie produits
**Utilisation** : Gestion portefeuille produits

```mdx
SELECT
  [Product].[ProductHierarchy].[Category].MEMBERS ON COLUMNS,
  {[Measures].[Revenue], [Measures].[Quantity], [Measures].[Avg_Basket]} ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

### 1️⃣3️⃣ Taux Retour par Catégorie

**Objectif** : Identifier catégories avec problèmes qualité
**Utilisation** : Amélioration produit, fournisseurs

```mdx
WITH MEMBER [Measures].[Return_Rate_Percent] AS
  ROUND(
    ([Measures].[Return_Count] / [Measures].[Order_Count]) * 100, 2
  )

SELECT
  [Measures].[Return_Rate_Percent] ON COLUMNS,
  [Product].[ProductHierarchy].[Category].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
ORDER BY CURRENT MEMBER ON ROWS DESC
```

---

## Requêtes Avancées

### 1️⃣4️⃣ Analyse Complète Multi-Dimensionnelle

**Objectif** : Vue consolidée (Temps × Région × Canal × Segment)
**Utilisation** : Dashboard exécutif principal

```mdx
SELECT
  [Time].[TimeHierarchy].[Quarter].MEMBERS ON COLUMNS,
  CROSSJOIN(
    [Region].[RegionHierarchy].MEMBERS,
    CROSSJOIN(
      [Channel].[ChannelHierarchy].MEMBERS,
      [Customer].[CustomerHierarchy].[Segment].MEMBERS
    )
  ) ON ROWS
FROM [SalesCube]
WHERE [Measures].[Revenue]
```

---

### 1️⃣5️⃣ Growth Rate (YoY)

**Objectif** : Croissance annuelle sur année précédente
**Utilisation** : Performance vs année antérieure

```mdx
WITH MEMBER [Measures].[PrevYear_Revenue] AS
  CLOSINGPERIOD(
    [Time].[TimeHierarchy].[Year],
    PARALLELPERIOD(
      [Time].[TimeHierarchy].[Year],
      1,
      [Time].[TimeHierarchy].currentMember
    )
  ).Item(0).Item(0)

MEMBER [Measures].[YoY_Growth_Percent] AS
  ROUND(
    (([Measures].[Revenue] - [Measures].[PrevYear_Revenue]) /
     [Measures].[PrevYear_Revenue]) * 100, 2
  )

SELECT
  {[Measures].[Revenue], [Measures].[PrevYear_Revenue], [Measures].[YoY_Growth_Percent]} ON COLUMNS,
  [Time].[TimeHierarchy].[Year].MEMBERS ON ROWS
FROM [SalesCube]
```

---

### 1️⃣6️⃣ Pareto Analysis (80/20)

**Objectif** : Identifier 20% produits = 80% chiffre
**Utilisation** : Priorisation, allocation ressources

```mdx
WITH MEMBER [Measures].[Revenue_Cumul] AS
  SUM(
    HEAD(
      ORDER(
        [Product].[ProductHierarchy].[Product].MEMBERS,
        [Measures].[Revenue],
        DESC
      ),
      0
    ),
    [Measures].[Revenue]
  )

MEMBER [Measures].[Percent_Total] AS
  ROUND(
    ([Measures].[Revenue_Cumul] / 
     SUM([Product].[ProductHierarchy].[Product].MEMBERS, [Measures].[Revenue])) * 100, 2
  )

SELECT
  {[Measures].[Revenue], [Measures].[Percent_Total]} ON COLUMNS,
  HEAD(
    ORDER(
      [Product].[ProductHierarchy].[Product].MEMBERS,
      [Measures].[Revenue],
      DESC
    ), 50
  ) ON ROWS
FROM [SalesCube]
WHERE [Percent_Total] <= 80
```

---

### 1️⃣7️⃣ Channel Mix Evolution

**Objectif** : Evolution % par canal dans le temps
**Utilisation** : Planification marketing, allocation budget

```mdx
WITH MEMBER [Measures].[Channel_Percent] AS
  ROUND(
    [Measures].[Revenue] / 
    SUM([Channel].[ChannelHierarchy].MEMBERS, [Measures].[Revenue]) * 100, 2
  )

SELECT
  [Time].[TimeHierarchy].[Quarter].MEMBERS ON COLUMNS,
  [Channel].[ChannelHierarchy].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Measures].[Channel_Percent]
```

---

## KPIs et Mesures Calculées

### Définitions des KPIs Principaux

```mdx
-- 1. Average Basket Value
WITH MEMBER [Measures].[Avg_Basket] AS
  ROUND([Measures].[Revenue] / [Measures].[Order_Count], 2)

-- 2. Return Rate (%)
WITH MEMBER [Measures].[Return_Rate_Pct] AS
  ROUND(([Measures].[Return_Count] / [Measures].[Order_Count]) * 100, 2)

-- 3. Satisfaction Score (1-5)
WITH MEMBER [Measures].[Avg_Satisfaction] AS
  ROUND([Measures].[Satisfaction] / [Measures].[Feedback_Count], 1)

-- 4. Customer Lifetime Value
WITH MEMBER [Measures].[CLV] AS
  SUM([Customer].[CustomerHierarchy].[Customer].MEMBERS, [Measures].[Revenue])

-- 5. Revenue per Customer
WITH MEMBER [Measures].[Revenue_Per_Customer] AS
  ROUND([Measures].[Revenue] / [Measures].[Unique_Customers], 2)

-- 6. Order Frequency (Orders per Customer)
WITH MEMBER [Measures].[Order_Frequency] AS
  ROUND([Measures].[Order_Count] / [Measures].[Unique_Customers], 2)

-- 7. Net Revenue (after refunds)
WITH MEMBER [Measures].[Net_Revenue] AS
  [Measures].[Revenue] - [Measures].[Refund_Amount]

-- 8. Conversion Rate (Orders / Visits) - if web data available
WITH MEMBER [Measures].[Conversion_Rate] AS
  ROUND(([Measures].[Order_Count] / [Measures].[Web_Visits]) * 100, 2)
```

---

## Exemples d'Utilisation

### Dashboard Exécutif

```mdx
-- KPIs principaux
SELECT
  {
    [Measures].[Revenue],
    [Measures].[Order_Count],
    [Measures].[Avg_Basket],
    [Measures].[Return_Rate_Pct],
    [Measures].[Avg_Satisfaction]
  } ON COLUMNS,
  [Time].[TimeHierarchy].[Year].MEMBERS ON ROWS
FROM [SalesCube]
```

### Dashboard Régional

```mdx
SELECT
  [Time].[TimeHierarchy].[Quarter].MEMBERS ON COLUMNS,
  [Region].[RegionHierarchy].MEMBERS ON ROWS
FROM [SalesCube]
WHERE [Measures].[Revenue]
```

### Dashboard Produit

```mdx
SELECT
  [Product].[ProductHierarchy].[Category].MEMBERS ON COLUMNS,
  {[Measures].[Revenue], [Measures].[Quantity], [Measures].[Return_Rate_Pct]} ON ROWS
FROM [SalesCube]
WHERE [Time].[TimeHierarchy].[Year].[2023]
```

---

## Exécution des Requêtes

### Option 1: Saiku Analytics (Pentaho)

1. Ouvrir Saiku Analytics
2. Connecter au cube `SalesCube`
3. Construire requête via interface drag-drop
4. Exécuter et visualiser

### Option 2: Direct MDX (Mondrian)

```java
String query = "SELECT ... FROM [SalesCube]";
DataSource ds = new DataSource("jdbc:mysql://localhost/ecommerce_bi");
OlapConnection conn = ds.getConnection();
PreparedOlapStatement stmt = conn.prepareOlapStatement(query);
CellSet results = stmt.executeOlapQuery();
```

### Option 3: Power BI DAX (Equivalent)

```dax
EVALUATE
  ADDCOLUMNS(
    'DIM_CHANNEL',
    "Revenue", SUMX(RELATEDTABLE('FACT_ORDERS'), 'FACT_ORDERS'[Revenue])
  )
```

---

## Performance Notes

- Queries run on OLAP cube (aggregated, pre-calculated)
- Response time typically < 1 second
- Cache results for dashboard refresh (hourly)
- Use filters to reduce dimension cardinality
- Avoid Cartesian products in CROSSJOIN

---

**End of MDX Queries Documentation**
