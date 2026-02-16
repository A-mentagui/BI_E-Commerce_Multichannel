# how to deploy and test the OLAP cube using Mondrian Schema Workbench and the tools you need

Using "Create File"

Since I can't create new files, I'll provide you with a clear, comprehensive answer below:

---

## **How to Run OLAP Cube in Mondrian Schema Workbench**

### **What Tools You Need**

| Tool | Purpose | Why |
|------|---------|-----|
| **MySQL 8.0+** | Database engine | Stores your data warehouse |
| **Mondrian Schema Workbench** | OLAP schema designer | Validates & tests ecommerce_catalog.xml |
| **Saiku Analytics 3.x/4.x** | OLAP query & visualization | Run MDX queries, create dashboards |
| **MySQL Connector/J** | JDBC driver | Connects Saiku/Mondrian to MySQL |

**Optional:**

- Pentaho PDI (for ETL automation)
- MySQL Workbench (visual DB management)

---

## **Step-by-Step Deployment**

### **1️⃣ Setup Database**

```bash
# Start MySQL
mysql -u root -p

# Execute inside MySQL:
CREATE DATABASE IF NOT EXISTS ecommerce_bi;
CREATE USER 'bi_user'@'localhost' IDENTIFIED BY 'bi_password';
GRANT ALL PRIVILEGES ON ecommerce_bi.* TO 'bi_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Load schema (from project root)
mysql -u bi_user -p ecommerce_bi < sql/setup_database.sql
# Enter password: bi_password
```

This creates:
- ✅ 6 dimension tables (DIM_TIME, DIM_PRODUCT, DIM_CHANNEL, DIM_CUSTOMER, DIM_REGION, DIM_DELIVERY)
- ✅ 3 fact tables (FACT_ORDERS, FACT_RETURNS, FACT_FEEDBACK)
- ✅ **OLAP view**: `vw_fact_orders_olap` (consolidates returns/feedback at order grain)
- ✅ Stored procedure for time dimension population

---

### **2️⃣ Generate Synthetic Data**

```bash
# From project root
python scripts/generate_data.py
```

Creates raw CSV files:
- customers.csv (10K rows)
- products.csv (500 rows)
- orders.csv (50K rows)
- returns.csv (~5K rows)
- feedback.csv (~8K rows)

---

### **3️⃣ Load Data into Database**

**Option A: Via Pentaho ETL (Recommended)**
```bash
cd C:\pentaho\pdi
pan.bat /file="C:\Users\Small\Desktop\vs\BI2\etl\Master_Job.kjb"
```

**Option B: Manual SQL Load**
```sql
-- In MySQL shell or workbench:
LOAD DATA LOCAL INFILE 'data/raw/customers.csv'
INTO TABLE DIM_CUSTOMER
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- Repeat for other CSV files...
```

---

### **4️⃣ Install & Configure Mondrian Schema Workbench**

**Download:**
1. Go to [Mondrian Releases](https://sourceforge.net/projects/mondrian/files/)
2. Download `mondrian-4.x-workbench.zip`
3. Extract to `C:\mondrian\`

**Start Workbench:**
```bash
cd C:\mondrian\
workbench.bat
```

---

### **5️⃣ Configure Database Connection in Workbench**

1. **File → New Connection**
   - Connection Name: `ecommerce_bi`
   - Driver: `MySQL`
   - Server: `localhost`
   - Port: `3306`
   - Database: `ecommerce_bi`
   - User: `bi_user`
   - Password: `bi_password`

2. **Test Connection** → Should show ✓ **Connection successful**

3. **Click OK** to save

---

### **6️⃣ Open & Validate Schema in Workbench**

1. **File → Open** → Select ecommerce_catalog.xml

2. You should see the schema tree:
```
EcommerceBIOLAP
└── SalesCube
    ├── Dimensions
    │   ├── Time (Year → Quarter → Month → Day)
    │   ├── Product (Category → SubCategory → Product)
    │   ├── Channel (ChannelType → Channel)
    │   ├── Customer (Segment → Country → City → Customer)
    │   ├── Region
    │   └── Delivery
    └── Measures
        ├── Revenue (SUM)
        ├── Quantity (SUM)
        ├── Order_Count (COUNT)
        ├── Return_Count (SUM)
        ├── Refund_Amount (SUM)
        ├── Satisfaction (AVG)
        ├── Avg_Basket (CALCULATED)
        └── Return_Rate_Pct (CALCULATED)
```

3. **Validate Schema**: Tools → Validate Schema
   - Should show: ✓ **Schema is valid**

---

### **7️⃣ Test Cube in Workbench (Optional)**

1. **Tools → Test Cube Connection**
2. Select `SalesCube`
3. Should see: ✓ **Connection to cube successful**

---

### **8️⃣ Deploy to Saiku Analytics**

**Download & Setup:**
1. Download [Saiku Server](https://github.com/meteorite/saiku/releases)
2. Extract to `C:\saiku\`
3. Copy MySQL JDBC driver to: `C:\saiku\server\lib\mysql-connector-java-8.x.x.jar`

**Create Datasource File:**

Create file: `C:\saiku\server\webapps\ROOT\WEB-INF\classes\saiku\repository\datasources\ecommerce_bi_olap.properties`

```properties
type=OLAP
name=ecommerce_bi_olap
driver=mondrian.olap4j.MondrianOlap4jDriver
location=jdbc:mondrian:JdbcDrivers=com.mysql.cj.jdbc.Driver;Jdbc=jdbc:mysql://localhost:3306/ecommerce_bi?useSSL=false&serverTimezone=UTC;JdbcUser=bi_user;JdbcPassword=bi_password;Catalog=file:///C:/Users/Small/Desktop/vs/BI2/olap/ecommerce_catalog.xml;
username=admin
password=admin
security.enabled=false
```

**Start Saiku:**
```bash
cd C:\saiku\server\
startup.bat
```

Open browser: `http://localhost:8080/saiku`

---

### **9️⃣ Test OLAP Queries in Saiku**

**Visual Query Builder:**
1. Click **+ New Query**
2. Select Cube: **SalesCube**
3. Drag to axes:
   - **Rows**: Product → Category
   - **Columns**: Time → Year
   - **Measures**: Revenue, Quantity, Avg_Basket
4. Click **Execute**

**MDX Query (Direct):**
```mdx
SELECT
  NON EMPTY [Product].[Product].Members ON ROWS,
  NON EMPTY [Time].[Time].[Year].Members ON COLUMNS
FROM [SalesCube]
WHERE ([Measures].[Revenue])
```

Expected: Revenue breakdown by product × year

---

## **Quick Reference: Tools & What They Do**

| Tool | What It Does | When to Use |
|------|--------------|------------|
| **MySQL** | Stores data | Always (database foundation) |
| **Workbench** | Design/validate schema XML | Before deploying |
| **Saiku** | Query cube & build dashboards | Final OLAP analytics |
| **Pentaho PDI** | Automate ETL load | Optional (if automating data load) |

---

## **Complete Workflow**

```
1. mysql < setup_database.sql       [Create tables & OLAP view]
   ↓
2. python generate_data.py          [Create CSV files]
   ↓
3. Loading data (Pentaho or manual)  [Populate tables]
   ↓
4. workbench.bat → open schema      [Validate in Workbench]
   ↓
5. startup.bat (Saiku)              [Start OLAP server]
   ↓
6. http://localhost:8080/saiku      [Run MDX queries]
```

**You are now ready to query your OLAP cube!**