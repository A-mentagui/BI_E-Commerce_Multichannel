# Modèle de Données - Architecture Dimensionnelle

## 1. OVERVIEW - Schéma en Étoile (Star Schema)

```
                           FACT_ORDERS
                                |
        _____________________________|_____________________________
        |          |          |         |        |         |
    DIM_TIME  DIM_PRODUCT  DIM_CHANNEL  DIM_CUSTOMER  DIM_REGION  DIM_DELIVERY
```

---

## 2. TABLE DE FAITS : FACT_ORDERS

La table centrale qui enregistre les transactions e-commerce.

### Structure

```sql
CREATE TABLE FACT_ORDERS (
    OrderKey SERIAL PRIMARY KEY,
    OrderID VARCHAR(20) UNIQUE NOT NULL,
    TimeKey INTEGER NOT NULL,
    ProductKey INTEGER NOT NULL,
    ChannelKey INTEGER NOT NULL,
    CustomerKey INTEGER NOT NULL,
    RegionKey INTEGER NOT NULL,
    DeliveryKey INTEGER NOT NULL,
    
    -- Mesures additives
    Revenue DECIMAL(10,2) NOT NULL,
    Quantity INTEGER NOT NULL,
    UnitPrice DECIMAL(10,2),
    Discount DECIMAL(10,2) DEFAULT 0,
    
    -- Mesures semi-additives
    OrderStatus VARCHAR(50),
    
    OrderDate DATE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (TimeKey) REFERENCES DIM_TIME(TimeKey),
    FOREIGN KEY (ProductKey) REFERENCES DIM_PRODUCT(ProductKey),
    FOREIGN KEY (ChannelKey) REFERENCES DIM_CHANNEL(ChannelKey),
    FOREIGN KEY (CustomerKey) REFERENCES DIM_CUSTOMER(CustomerKey),
    FOREIGN KEY (RegionKey) REFERENCES DIM_REGION(RegionKey),
    FOREIGN KEY (DeliveryKey) REFERENCES DIM_DELIVERY(DeliveryKey)
);
```

### Mesures Principales

| Mesure | Type | Agrégation | Description |
|--------|------|-----------|-------------|
| **Revenue** | Decimal(10,2) | SUM | Montant total de la commande |
| **Quantity** | Integer | SUM | Nombre d'unités vendues |
| **UnitPrice** | Decimal(10,2) | AVG | Prix unitaire |
| **Discount** | Decimal(10,2) | SUM | Remise appliquée |

---

## 3. DIMENSIONS

### 3.1 DIM_TIME - Dimension Temporelle

```sql
CREATE TABLE DIM_TIME (
    TimeKey INTEGER PRIMARY KEY,
    FullDate DATE UNIQUE NOT NULL,
    Year INTEGER,
    Quarter INTEGER,
    Month INTEGER,
    MonthName VARCHAR(20),
    DayOfMonth INTEGER,
    DayOfWeek INTEGER,
    DayName VARCHAR(20),
    WeekOfYear INTEGER,
    Season VARCHAR(20),
    IsWeekend BOOLEAN,
    IsHoliday BOOLEAN
);
```

**Exemples de données** :
```
TimeKey=20220101, FullDate=2022-01-01, Year=2022, Quarter=1, Month=1, 
MonthName='Janvier', DayOfMonth=1, DayOfWeek=6, DayName='Samedi', 
WeekOfYear=52, Season='Hiver', IsWeekend=TRUE, IsHoliday=FALSE
```

### 3.2 DIM_PRODUCT - Dimension Produit

```sql
CREATE TABLE DIM_PRODUCT (
    ProductKey INTEGER PRIMARY KEY,
    ProductID VARCHAR(20) UNIQUE NOT NULL,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    Price DECIMAL(10,2),
    Supplier VARCHAR(255),
    Stock INTEGER,
    CreatedDate DATE,
    LastModifiedDate DATE
);
```

**Attributs** :
- **ProductID** : Identifiant unique du produit (ex: PROD000001)
- **Category** : 20 catégories principales
- **SubCategory** : Sous-catégories
- **Price** : Prix de vente (distribution lognormale)
- **Stock** : Quantité en stock (0 à 500)

### 3.3 DIM_CHANNEL - Dimension Canal

```sql
CREATE TABLE DIM_CHANNEL (
    ChannelKey INTEGER PRIMARY KEY,
    ChannelID VARCHAR(10) UNIQUE NOT NULL,
    ChannelName VARCHAR(100) NOT NULL,
    ChannelType VARCHAR(50),  -- 'Digital' ou 'Physical'
    Description VARCHAR(255)
);
```

**Canaux** :
| ChannelID | ChannelName | Type | Distribution |
|-----------|------------|------|--------------|
| CHAN00 | Web | Digital | 50% |
| CHAN01 | Mobile | Digital | 35% |
| CHAN02 | Pop-Up | Physical | 10% |
| CHAN03 | Réseaux Sociaux | Digital | 5% |

### 3.4 DIM_CUSTOMER - Dimension Client

```sql
CREATE TABLE DIM_CUSTOMER (
    CustomerKey INTEGER PRIMARY KEY,
    CustomerID VARCHAR(20) UNIQUE NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Segment VARCHAR(50),  -- 'Nouveau', 'Régulier', 'Fidèle'
    RegistrationDate DATE,
    Country VARCHAR(100),
    City VARCHAR(100),
    PostalCode VARCHAR(20),
    LastPurchaseDate DATE
);
```

**Segments** :
- **Nouveau** : < 3 mois depuis inscription (25%)
- **Régulier** : Entre 3 et 12 mois (50%)
- **Fidèle** : > 12 mois (25%)

### 3.5 DIM_REGION - Dimension Région

```sql
CREATE TABLE DIM_REGION (
    RegionKey INTEGER PRIMARY KEY,
    RegionID VARCHAR(10) UNIQUE NOT NULL,
    RegionName VARCHAR(100) NOT NULL,
    Country VARCHAR(100),
    Population BIGINT,
    UrbanRate DECIMAL(5,2)
);
```

**Régions couverts** : 13 régions françaises
- Île-de-France (Plus grand marché)
- PACA, Auvergne-Rhône-Alpes, etc.

### 3.6 DIM_DELIVERY - Dimension Livraison

```sql
CREATE TABLE DIM_DELIVERY (
    DeliveryKey INTEGER PRIMARY KEY,
    DeliveryID VARCHAR(20),
    DeliveryMethod VARCHAR(100),
    DeliveryTimeDays INTEGER,
    Cost DECIMAL(10,2),
    Reliability DECIMAL(5,2)  -- % de respect des délais
);
```

**Méthodes de livraison** :
| Méthode | Délai | Coût | % livraison |
|---------|-------|------|-------------|
| Standard (5-7 jours) | 6 | €5 | 98% |
| Express (2-3 jours) | 2.5 | €15 | 99% |
| Urgent (24h) | 1 | €25 | 97% |
| Retrait en point | 3 | €3 | 100% |

---

## 4. TABLES TRANSACTIONNELLES (BRIDGE TABLES)

### 4.1 FACT_RETURNS - Retours et Remboursements

```sql
CREATE TABLE FACT_RETURNS (
    ReturnKey SERIAL PRIMARY KEY,
    ReturnID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INTEGER NOT NULL,
    ReturnDate DATE NOT NULL,
    ReturnReason VARCHAR(255),
    RefundAmount DECIMAL(10,2),
    
    FOREIGN KEY (OrderKey) REFERENCES FACT_ORDERS(OrderKey)
);
```

**Raisons de retour** :
- Produit défectueux
- Mauvaise taille
- Produit différent
- Délai de livraison trop long
- Insatisfait de la qualité
- Changement d'avis

### 4.2 FACT_FEEDBACK - Satisfaction Client

```sql
CREATE TABLE FACT_FEEDBACK (
    FeedbackKey SERIAL PRIMARY KEY,
    FeedbackID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INTEGER NOT NULL,
    Satisfaction INTEGER (1-5),
    Comment TEXT,
    FeedbackDate DATE,
    
    FOREIGN KEY (OrderKey) REFERENCES FACT_ORDERS(OrderKey)
);
```

**Satisfaction** : Échelle 1 à 5
- 1 : Très insatisfait
- 5 : Très satisfait

---

## 5. STATISTIQUES DESCRIPTIVES (DONNÉES SYNTHÉTIQUES)

### 5.1 Volume de Données

| Table | Nombre de Lignes | Taille Estimée |
|-------|------------------|----------------|
| DIM_TIME | 1,107 | ~100 KB |
| DIM_PRODUCT | 500 | ~80 KB |
| DIM_CHANNEL | 4 | ~1 KB |
| DIM_CUSTOMER | 10,000 | ~2 MB |
| DIM_REGION | 13 | ~1 KB |
| DIM_DELIVERY | 4 | ~1 KB |
| **FACT_ORDERS** | **50,000** | **~20 MB** |
| FACT_RETURNS | ~3,500 | ~600 KB |
| FACT_FEEDBACK | ~35,000 | ~10 MB |
| **TOTAL** | **~99,000** | **~33 MB** |

### 5.2 Distribution par Canal

```
Web              : 50% → 25,000 commandes
Mobile           : 35% → 17,500 commandes
Pop-Up           : 10% → 5,000 commandes
Réseaux Sociaux  : 5%  → 2,500 commandes
```

### 5.3 Distribution par Segment Client

```
Nouveau          : 25% → 2,500 clients
Régulier         : 50% → 5,000 clients
Fidèle           : 25% → 2,500 clients
```

### 5.4 Taux de Retour par Canal

```
Web              : 8%
Mobile           : 6%
Pop-Up           : 12%
Réseaux Sociaux  : 15%
```

### 5.5 Métriques Clés

```
Panier Moyen Total       : €75 - €150
Panier Moyen Web         : €75 - €150
Panier Moyen Mobile      : €50 - €100
Panier Moyen Pop-Up      : €100 - €250
Panier Moyen Social      : €30 - €80

Satisfaction Moyenne     : 3.2/5
Taux de Feedback         : 70%
Taux de Retour Global    : 8.5%
```

---

## 6. CLÉS ÉTRANGÈRES ET INTÉGRITÉ RÉFÉRENTIELLE

### Relations

```
FACT_ORDERS:
  TimeKey       → DIM_TIME.TimeKey
  ProductKey    → DIM_PRODUCT.ProductKey
  ChannelKey    → DIM_CHANNEL.ChannelKey
  CustomerKey   → DIM_CUSTOMER.CustomerKey
  RegionKey     → DIM_REGION.RegionKey
  DeliveryKey   → DIM_DELIVERY.DeliveryKey

FACT_RETURNS:
  OrderKey      → FACT_ORDERS.OrderKey

FACT_FEEDBACK:
  OrderKey      → FACT_ORDERS.OrderKey
```

---

## 7. MESURES CALCULÉES (POUR LE CUBE OLAP)

### Mesures Basiques
- **Revenue** = SUM(Revenue)
- **Quantity** = SUM(Quantity)
- **Order Count** = COUNT(OrderID)

### Mesures Dérivées
- **Average Basket** = Revenue / Order Count
- **Return Rate** = Count(Returns) / Order Count
- **Average Satisfaction** = AVG(Satisfaction)
- **Total Refund Amount** = SUM(RefundAmount)

### KPIs Avancés
- **Customer Lifetime Value** = SUM(Revenue) par Customer
- **Churn Risk** = IF(Recency > 90 days, HIGH, LOW)
- **Repeat Purchase Rate** = Customers with 2+ orders / Total Customers
- **Net Revenue** = Revenue - Discount - Refunds

---

## 8. FICHIERS CSV GÉNÉRÉS

### Structure des Fichiers

#### customers.csv
```
CustomerID,CustomerName,Email,Segment,RegistrationDate,Country,City,PostalCode
CUST000001,Jean Dupont,jean@email.com,Fidèle,2022-06-15,France,Paris,75001
CUST000002,Marie Martin,marie@email.com,Nouveau,2024-01-20,France,Lyon,69000
```

#### products.csv
```
ProductID,ProductName,Category,SubCategory,Price,Supplier,Stock
PROD000001,electronics computer,Électronique,Informatique,1299.99,TechCorp,45
PROD000002,mode apparel,Mode & Vêtements,Vêtements,49.99,FashionWorld,120
```

#### orders.csv
```
OrderID,CustomerID,ProductID,ChannelID,ChannelName,RegionID,RegionName,OrderDate,Quantity,UnitPrice,Revenue,Discount,DeliveryMethod,OrderStatus
ORD00000001,CUST000001,PROD000001,CHAN00,Web,REG75,Île-de-France,2022-07-10,1,1299.99,1299.99,0,Express (2-3 jours),Livré
```

#### returns.csv
```
ReturnID,OrderID,ReturnDate,ReturnReason,RefundAmount
RET00000001,ORD00000005,2022-08-05,Produit défectueux,89.99
```

#### feedback.csv
```
FeedbackID,OrderID,Satisfaction,Comment,FeedbackDate
FB00000001,ORD00000001,5,Très satisfait,2022-07-25
```

---

## 9. CARDINALITÉS

```
1 Customer  → N Orders
1 Product   → N Orders
1 Channel   → N Orders
1 Region    → N Orders
1 Delivery  → N Orders
1 Order     → 0..1 Return
1 Order     → 0..1 Feedback
```

---

## 10. INDEXES RECOMMANDÉS

```sql
-- Fact table
CREATE INDEX idx_fact_orders_customerkey ON FACT_ORDERS(CustomerKey);
CREATE INDEX idx_fact_orders_productkey ON FACT_ORDERS(ProductKey);
CREATE INDEX idx_fact_orders_timekey ON FACT_ORDERS(TimeKey);
CREATE INDEX idx_fact_orders_channelkey ON FACT_ORDERS(ChannelKey);
CREATE INDEX idx_fact_orders_orderdate ON FACT_ORDERS(OrderDate);

-- Bridge tables
CREATE INDEX idx_returns_orderkey ON FACT_RETURNS(OrderKey);
CREATE INDEX idx_feedback_orderkey ON FACT_FEEDBACK(OrderKey);

-- Dimensions
CREATE INDEX idx_customer_segment ON DIM_CUSTOMER(Segment);
CREATE INDEX idx_region_country ON DIM_REGION(Country);
CREATE INDEX idx_time_year ON DIM_TIME(Year);
```

---

## 11. NOTES

- **Periode** : 2022-01-01 à 2024-02-15 (2 ans et ~1.5 mois)
- **Locale** : France (données francophones)
- **Seed** : Random seed fixé pour reproductibilité
- **Format Date** : YYYY-MM-DD (ISO 8601)
- **Devise** : EUR (€)
