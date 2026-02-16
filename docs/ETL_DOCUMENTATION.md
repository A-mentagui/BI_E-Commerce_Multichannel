# ETL Documentation - Pentaho Data Integration

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture ETL](#architecture-etl)
3. [Transformations Détaillées](#transformations-détaillées)
4. [Gestion de la Qualité](#gestion-de-la-qualité)
5. [Orchestration & Planification](#orchestration--planification)
6. [Monitoring et Logs](#monitoring-et-logs)

---

## Vue d'ensemble

Le processus ETL (Extract, Transform, Load) intègre les données CSV brutes dans le data warehouse dimensionnel en 5-6 transformations principales coordonnées par un job master.

### Architecture Globale

```
CSV Files (Raw Data)
    ↓
    ├─ Extract (Pentaho Transformation)
    ├─ Transform (Validation, Cleaning, Enrichment)
    ├─ Load (Insert/Update dimensions & facts)
    └─ Reconciliation (Data Quality Checks)
         ↓
    Data Warehouse (Star Schema)
```

---

## Architecture ETL

### Structure des Fichiers Pentaho

```
etl/
├── transformations/
│   ├── ETL_1_Load_Customers.ktr          Charge DIM_CUSTOMER
│   ├── ETL_2_Load_Products.ktr           Charge DIM_PRODUCT
│   ├── ETL_3_Load_Channels.ktr           Charge DIM_CHANNEL
│   ├── ETL_4_Load_Regions.ktr            Charge DIM_REGION
│   ├── ETL_5_Load_Delivery.ktr           Charge DIM_DELIVERY
│   ├── ETL_6_Load_Orders.ktr             Charge FACT_ORDERS
│   ├── ETL_7_Load_Returns.ktr            Charge FACT_RETURNS
│   └── ETL_8_Load_Feedback.ktr           Charge FACT_FEEDBACK
│
├── jobs/
│   ├── Master_Job.kjb                    Orchestration principale
│   ├── DIM_Load_Job.kjb                  Charge les dimensions
│   └── FACT_Load_Job.kjb                 Charge les faits
│
└── utilities/
    ├── Data_Quality_Checks.ktr           Validations
    ├── Reconciliation_Report.ktr         Rapport réconciliation
    └── Data_Lineage.ktr                  Traçabilité
```

---

## Transformations Détaillées

### 1️⃣ ETL_1_Load_Customers

**Entrée** : `data/raw/customers.csv`
**Sortie** : `DIM_CUSTOMER` (10,000 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│  ├─ Delimiter: ,
│  ├─ Encoding: UTF-8
│  └─ Quote handling: "
│
├─ Filter Rows
│  └─ Remove rows where Email is NULL
│
├─ Java Script
│  ├─ CustomerKey = auto_increment()
│  ├─ Segment = Trim(Segment)
│  └─ Email = Lower(Email)
│
├─ Database Lookup (Optional - Check duplicates)
│  └─ Lookup on CustomerID
│
└─ Database Insert/Update
   ├─ Table: DIM_CUSTOMER
   ├─ Update on: CustomerID
   ├─ Insert: First occurrence
   └─ Log: errors.txt
```

#### Validations

```
Quality Checks:
- Email format: Must contain '@'
- Segment: Must be in ['Nouveau', 'Régulier', 'Fidèle']
- RegistrationDate: Between 2022-01-01 and 2024-02-15
- No NULL CustomerID
```

#### Error Handling

```
- Invalid emails → Send to error_customers.csv
- Duplicate CustomerID → Update existing record
- Date parsing errors → Set to 1900-01-01 + log
```

---

### 2️⃣ ETL_2_Load_Products

**Entrée** : `data/raw/products.csv`
**Sortie** : `DIM_PRODUCT` (500 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│  └─ File: products.csv
│
├─ Row Flattener (Handle multi-line products if needed)
│
├─ Calculator
│  ├─ ProductKey = auto_increment()
│  ├─ Price = Round(Price, 2)
│  ├─ Stock = Max(0, Stock)
│  └─ LastModifiedDate = TODAY()
│
├─ Lookup (Check category exists)
│  └─ Validate Category from allowed list
│
├─ Filter
│  └─ Price > 0 AND Price < 50000
│
└─ Database Insert
   ├─ Table: DIM_PRODUCT
   ├─ Key: ProductID
   └─ Log: products_loaded.log
```

#### Business Rules

```
- Price validation: €0.01 - €50,000
- Stock floor: 0 (no negative inventory)
- Product names: Trim whitespace, max 255 chars
- Categories: Predefined list of 20 categories
- Supplier: Max 255 chars
```

---

### 3️⃣ ETL_3_Load_Channels

**Entrée** : `data/raw/channels.csv`
**Sortie** : `DIM_CHANNEL` (4 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│
├─ Map Input to Output
│  ├─ ChannelID → ChannelID
│  ├─ ChannelName → ChannelName
│  └─ ChannelType (Auto-assign based on name)
│
├─ JavaScript
│  ├─ ChannelType = (ChannelName === 'Pop-Up') ? 'Physical' : 'Digital'
│
└─ Database Insert
   └─ Table: DIM_CHANNEL
```

#### Expected Data

```
CHAN00 | Web | Digital
CHAN01 | Mobile | Digital
CHAN02 | Pop-Up | Physical
CHAN03 | Réseaux Sociaux | Digital
```

---

### 4️⃣ ETL_4_Load_Regions

**Entrée** : `data/raw/regions.csv`
**Sortie** : `DIM_REGION` (13 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│
├─ Lookup (Optional - Get population from reference)
│
├─ Database Insert
│  └─ Table: DIM_REGION
│
└─ Log file: regions_loaded.log
```

#### Expected Data

```
REG00 | Île-de-France | France
REG01 | PACA | France
... (11 more regions)
```

---

### 5️⃣ ETL_5_Load_Delivery

**Entrée** : `data/raw/orders.csv` (distinct delivery methods)
**Sortie** : `DIM_DELIVERY` (4 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│
├─ Unique Rows
│  └─ DeliveryMethod field
│
├─ Calculator
│  ├─ DeliveryKey = auto_increment()
│  ├─ DeliveryTimeDays = Extract from method
│  ├─ Cost = Hardcoded per type
│  └─ Reliability = Historical %
│
└─ Database Insert
   └─ Table: DIM_DELIVERY
```

#### Mapping

```
METHOD | DAYS | COST | RELIABILITY
Standard (5-7 jours) | 6 | €5 | 98%
Express (2-3 jours) | 2.5 | €15 | 99%
Urgent (24h) | 1 | €25 | 97%
Retrait en point | 3 | €3 | 100%
```

---

### 6️⃣ ETL_6_Load_Orders (CRITICAL)

**Entrée** : `data/raw/orders.csv`
**Sortie** : `FACT_ORDERS` (50,000 lignes)

#### Architecture

```
Input Step
├─ CSV File Input
│  └─ orders.csv
│
├─ Dimension Lookup (CRITICAL)
│  ├─ Lookup DIM_TIME (TimeKey from OrderDate)
│  ├─ Lookup DIM_PRODUCT (ProductKey from ProductID)
│  ├─ Lookup DIM_CHANNEL (ChannelKey from ChannelID)
│  ├─ Lookup DIM_CUSTOMER (CustomerKey from CustomerID)
│  ├─ Lookup DIM_REGION (RegionKey from RegionID)
│  └─ Lookup DIM_DELIVERY (DeliveryKey from DeliveryMethod)
│
├─ Data Quality Checks
│  ├─ Revenue > 0
│  ├─ Quantity > 0 AND Quantity < 1000
│  ├─ Discount < Revenue
│  └─ Net Revenue (Revenue - Discount) > 0
│
├─ Calculator
│  ├─ OrderKey = auto_increment()
│  ├─ GrossRevenue = Quantity * UnitPrice
│  ├─ NetRevenue = Revenue - Discount
│  └─ CreatedAt = CURRENT_TIMESTAMP
│
├─ Filter (Reject bad data)
│  └─ Send invalid rows to orders_error.csv
│
├─ Database Insert/Update
│  ├─ Table: FACT_ORDERS
│  ├─ Key: OrderID
│  ├─ Batch size: 1000
│  └─ Error file: orders_rejected.csv
│
└─ Log
   └─ Rows inserted, updated, rejected
```

#### Critical Validations

```
✓ All OrderID values must exist and be unique
✓ All ProductID must have matching ProductKey in DIM_PRODUCT
✓ All CustomerID must have matching CustomerKey in DIM_CUSTOMER
✓ All ChannelID must have matching ChannelKey in DIM_CHANNEL
✓ All RegionID must have matching RegionKey in DIM_REGION
✓ OrderDate must be between 2022-01-01 and 2024-02-15
✓ Revenue must be > 0 and <= 10,000
✓ Quantity must be between 1 and 100
```

#### Error Handling

```
Error Type | Action | Log
-----------|--------|-----
Missing ProductKey | Reject row | orders_error_product.csv
Missing CustomerKey | Reject row | orders_error_customer.csv
Negative Revenue | Reject row | orders_error_revenue.csv
Missing DeliveryKey | Use default | orders_warning.csv
Invalid Date | Use today | orders_warning.csv
```

---

### 7️⃣ ETL_7_Load_Returns

**Entrée** : `data/raw/returns.csv`
**Sortie** : `FACT_RETURNS` (~3,500 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│
├─ Lookup
│  └─ OrderKey from FACT_ORDERS using OrderID
│
├─ Filter
│  ├─ OrderKey NOT NULL
│  └─ RefundAmount > 0
│
├─ Calculator
│  ├─ ReturnKey = auto_increment()
│  └─ ReturnDate validation
│
└─ Database Insert
   ├─ Table: FACT_RETURNS
   ├─ Key: ReturnID
   └─ Error file: returns_rejected.csv
```

#### Validations

```
✓ ReturnID must be unique
✓ OrderID must exist in FACT_ORDERS
✓ ReturnDate must be >= OrderDate
✓ RefundAmount must be > 0 and <= Original Order Revenue
✓ ReturnReason must be in allowed list
```

---

### 8️⃣ ETL_8_Load_Feedback

**Entrée** : `data/raw/feedback.csv`
**Sortie** : `FACT_FEEDBACK` (~35,000 lignes)

#### Steps

```
Input Step
├─ CSV File Input
│
├─ Lookup
│  └─ OrderKey from FACT_ORDERS using OrderID
│
├─ Calculator
│  ├─ FeedbackKey = auto_increment()
│  ├─ Satisfaction = Clamp(1, 5, Satisfaction value)
│  └─ FeedbackDate validation
│
├─ Text Processing
│  └─ Comment: Trim, handle special chars
│
└─ Database Insert
   ├─ Table: FACT_FEEDBACK
   ├─ Key: FeedbackID
   └─ Error file: feedback_rejected.csv
```

#### Validations

```
✓ Satisfaction between 1 and 5
✓ OrderID must exist in FACT_ORDERS
✓ FeedbackDate after OrderDate
✓ Comment max 1000 chars
```

---

## Gestion de la Qualité

### 1. Data Quality Rules

#### Pre-Load Checks

```sql
-- Check for NULL critical fields
SELECT COUNT(*) WHERE CustomerID IS NULL;
SELECT COUNT(*) WHERE ProductID IS NULL;
SELECT COUNT(*) WHERE OrderID IS NULL;

-- Check for duplicates
SELECT COUNT(*), COUNT(DISTINCT OrderID) FROM orders;
```

#### Post-Load Reconciliation

```sql
-- Row count comparison
SELECT 'CSV Orders', COUNT(*) FROM csv_orders
UNION ALL
SELECT 'Loaded Orders', COUNT(*) FROM FACT_ORDERS;

-- Revenue check
SELECT SUM(Revenue) as TotalRevenue FROM FACT_ORDERS;

-- Completeness check
SELECT COUNT(*) FROM FACT_ORDERS WHERE ProductKey IS NULL;
```

### 2. Error Handling

All errors are logged to dedicated CSV files:

```
├─ orders_rejected.csv          Failed order insertions
├─ customers_rejected.csv       Customer errors
├─ products_rejected.csv        Product errors
└─ reconciliation_report.csv    Post-load summary
```

### 3. Data Validation Matrix

| Field | Rule | Action |
|-------|------|--------|
| Revenue | > 0 and <= 10,000 | Reject if outside range |
| Quantity | 1-100 | Reject if outside range |
| Satisfaction | 1-5 | Clamp to nearest valid value |
| Date | Between 2022-2024 | Reject if invalid |
| FK Keys | Must exist | Reject order |

---

## Orchestration & Planification

### Master Job Flow

```
Master_Job
├─ START
│
├─ [1] Check Source Files Exist
│   └─ Verify all CSV files present
│
├─ [2] Load Dimensions (Parallel)
│   ├─ ETL_1_Load_Customers
│   ├─ ETL_2_Load_Products
│   ├─ ETL_3_Load_Channels
│   ├─ ETL_4_Load_Regions
│   └─ ETL_5_Load_Delivery
│
├─ [3] Wait for Dimension Completion
│
├─ [4] Populate DIM_TIME (SQL)
│   └─ Execute sp_populate_time_dimension
│
├─ [5] Lookup Test
│   └─ Verify dimension lookups work
│
├─ [6] Load Facts (Sequential)
│   ├─ ETL_6_Load_Orders
│   ├─ ETL_7_Load_Returns
│   └─ ETL_8_Load_Feedback
│
├─ [7] Data Quality Report
│   └─ Run reconciliation checks
│
├─ [8] Generate Summary
│   └─ Report inserted/rejected rows
│
└─ END
```

### Job Configuration

```
Maximum Errors: 1000
Batch Commit: Every 5000 rows
Parallel Threads: 2
Timeout: 2 hours per transformation
```

### Scheduling

```
Daily ETL: 2:00 AM UTC
- Incremental load for new orders
- Updates to customer records
- Refresh dimensions

Weekly Full Load: Sunday 1:00 AM UTC
- Complete reload (truncate & reload)
- Full reconciliation
- Backup creation
```

---

## Monitoring et Logs

### Log Location

```
logs/
├─ etl_master_2024-02-15_020000.log
├─ etl_1_load_customers_2024-02-15_020030.log
├─ etl_6_load_orders_2024-02-15_020530.log
└─ ...
```

### Log Levels

```
[DEBUG]   Detailed transformation steps
[INFO]    Row counts, status updates
[WARN]    Data quality issues, rejections
[ERROR]   Failed transformations, database errors
```

### Monitoring Metrics

```
┌─────────────────────────────────┐
│ ETL Monitoring Dashboard        │
├─────────────────────────────────┤
│ Total Rows Processed: 100,000   │
│ Rows Inserted: 99,500           │
│ Rows Rejected: 500 (0.5%)       │
│ Execution Time: 15 minutes      │
│ Status: SUCCESS ✓               │
└─────────────────────────────────┘
```

### Key Metrics to Track

```
✓ Rows Loaded per Transformation
✓ Error Rate (should be < 1%)
✓ Execution Time per Step
✓ Database Growth
✓ Lookup Performance
✓ Rejected Records
```

---

## Steps to Implement

### 1. Create Pentaho Transformations

For each of the 8 ETL steps:
1. Open Pentaho Data Integration
2. Create new transformation
3. Add input step (CSV)
4. Add transformations (filters, lookups, calculators)
5. Add database output step
6. Configure error handling
7. Test with sample data
8. Save as `.ktr` file

### 2. Create Master Job

1. Create new job in Pentaho
2. Add 8 transformation steps
3. Configure success/failure paths
4. Set parallelization
5. Add logging
6. Save as `.kjb` file

### 3. Test ETL

```
Test Sequence:
1. Load DIM_PRODUCT (simplest)
2. Load DIM_CUSTOMER
3. Load FACT_ORDERS (complex, with lookups)
4. Verify Row Counts
5. Run Reconciliation
```

### 4. Schedule Jobs

Use Pentaho Server or cron/Task Scheduler for scheduling.

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Lookup fails | Dimension not loaded | Verify dimension step ran successfully |
| Memory error | Too large batch | Reduce batch size to 1000 |
| Encoding issues | Special characters | Set UTF-8 encoding in CSV step |
| Duplicate keys | Re-running same data | Add check for existing keys |

### Performance Tuning

```
✓ Use database indexes on FK columns
✓ Batch commit size: 5000 rows
✓ Parallel lookups instead of sequential
✓ Archive processed CSV files
✓ Monitor database disk space
```

---

**End of ETL Documentation**
