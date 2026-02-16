# Pentaho and Mondrian Setup Guide

## Quick Start

### Prerequisites

- Pentaho Data Integration 9.3+ installed
- Mondrian 4.0+ OR Saiku Analytics 3.x installed
- MySQL 5.7+ or PostgreSQL 12+ for data warehouse
- Java 8+ runtime
- Network connectivity to database server

---

## Part 1: Pentaho ETL Setup

### Step 1: Installation

1. Extract Pentaho PDI to a location (e.g., `C:\pentaho\pdi`)
2. Set environment variable: `PENTAHO_HOME=C:\pentaho\pdi`
3. Test: Run `pdi\spoon.bat` (Windows) or `pdi/spoon.sh` (Linux)

### Step 2: Configure Database Connection

1. Open Pentaho Data Integration (PDI)
2. Go to **View → Database Connections**
3. Click **New Database Connection**
4. Configure for ecommerce_bi:
   - **Connection Name**: `ecommerce_bi`
   - **Database Type**: MySQL (or PostgreSQL)
   - **Server**: `localhost` (or your DB server)
   - **Port**: `3306` (MySQL) or `5432` (PostgreSQL)
   - **Database Name**: `ecommerce_bi`
   - **User Name**: `bi_user` (must have DML+DDL permissions)
   - **Password**: `[your_password]`
5. Click **Test Connection** → Should show "Connection Successful"
6. Click **OK** to save

### Step 3: Import ETL Transformations

1. Create folder structure in Pentaho:

   ```
   pentaho_workspace/
   ├── transformations/
   │   ├── ETL_1_Load_Customers.ktr
   │   ├── ETL_2_Load_Products.ktr
   │   ├── ETL_3_Load_Channels.ktr
   │   ├── ETL_4_Load_Regions.ktr
   │   ├── ETL_5_Load_Delivery.ktr
   │   ├── ETL_0_Load_Time.ktr
   │   ├── ETL_6_Load_Orders.ktr
   │   ├── ETL_7_Load_Returns.ktr
   │   └── ETL_8_Load_Feedback.ktr
   └── Master_Job.kjb
   ```

2. Copy provided .ktr files to transformations/ folder
3. Copy Master_Job.kjb to project root

### Step 4: Create CSV Data Files

1. Run Python data generator:

   ```bash
   python scripts/generate_data.py
   ```

   This creates files in `data/raw/`:
   - customers.csv
   - products.csv
   - channels.csv
   - regions.csv
   - orders.csv
   - returns.csv
   - feedback.csv

   > Note: `DIM_DELIVERY` is loaded via `ETL_5_Load_Delivery.ktr` from controlled reference values.

2. Update CSV file paths in each transformation if needed:
   - Right-click transformation → Edit
   - Double-click "CSV File Input" step
   - Update "Filename" field to point to actual file location
   - Example: `data/raw/customers.csv`

### Step 5: Configure Environment Variables

1. Edit `.env` file with your settings:

   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ecommerce_bi
   DB_USER=bi_user
   DB_PASSWORD=your_password

   CSV_FILE_PATH=data/raw/
   BATCH_SIZE=1000
   COMMIT_SIZE=500

   PENTAHO_HOME=/opt/pentaho
   ```

2. Reference in transformations via ${VARIABLE_NAME}

### Step 6: Test Individual Transformations

Before running the master job:

1. **Load Customers Test:**
   - Open ETL_1_Load_Customers.ktr
   - Click **Run** button (or Ctrl+F5)
   - Verify: DIM_CUSTOMER table populated with 10,000 records
   - Check logs for errors

2. **Load Products Test:**
   - Open ETL_2_Load_Products.ktr
   - Run and verify 500 products loaded

3. **Repeat for each transformation in order**

### Step 7: Run Master Job

1. Open Master_Job.kjb
2. Set job parameters:
   - Right-click job → **Job Settings**
   - Set parameter values if different from defaults
3. Click **Run** button
4. Monitor job execution in real-time
5. Check logs after completion

### Step 8: Monitor Execution

**Real-time monitoring:**

- Watch Job Execution Results window
- View step-by-step execution progress
- Check parallel dimension loads

**Post-execution:**

1. Check logs in `logs/transformations/`:
   - `load_customers.log`
   - `load_orders_detailed.log`
   - `errors/*.csv` (rejected records)

2. Verify data in database:
   ```sql
   SELECT COUNT(*) FROM DIM_CUSTOMER;      -- Should be 10,000
   SELECT COUNT(*) FROM DIM_PRODUCT;       -- Should be 500
   SELECT COUNT(*) FROM FACT_ORDERS;       -- Should be 50,000
   SELECT COUNT(*) FROM FACT_RETURNS;      -- Should be ~5,000
   SELECT COUNT(*) FROM FACT_FEEDBACK;     -- Should be ~8,000
   ```

### Step 9: Schedule ETL Jobs

**Windows Task Scheduler:**

1. Create batch file `run_etl.bat`:
   ```batch
   @echo off
   cd C:\pentaho\pdi
   pan.bat /file="C:\pentaho\workspace\Master_Job.kjb"
   ```
2. Open Task Scheduler
3. Create task to run batch file daily at 2 AM
4. Add email notification on completion/failure

**Linux Cron:**

```bash
0 2 * * * /opt/pentaho/pdi/sh/pan.sh -file /home/user/workspace/Master_Job.kjb
```

---

## Part 2: Mondrian OLAP Setup

### Step 1: Installation

**Option 1: Standalone Mondrian with Saiku Analytics**

1. Download Saiku Analytics 3.x
2. Extract to `/opt/saiku` or `C:\saiku`
3. Mondrian is bundled with Saiku

**Option 2: Mondrian in Application Server**

1. Install Mondrian 4.0+ JAR files
2. Place in Tomcat `lib/` folder
3. Configure webapp

### Step 2: Configure Mondrian Connection

1. Locate `mondrian.properties` file:
   - Saiku: `/opt/saiku/server/webapps/ROOT/WEB-INF/classes/`
   - Tomcat: `/var/lib/tomcat/webapps/mondrian/WEB-INF/classes/`

2. Update with provided `mondrian.properties`:

   ```properties
   mondrian.jdbcURL=jdbc:mysql://localhost:3306/ecommerce_bi
   mondrian.jdbcUser=bi_user
   mondrian.jdbcPassword=your_password
   mondrian.catalogContent=file://./olap/ecommerce_catalog.xml
   ```

3. Place schema file:
   - Copy `ecommerce_catalog.xml` to mondrian classpath directory

4. (Recommended) Use provided Saiku datasource template:
   - File: `olap/saiku-datasource.properties`
   - Replace `${PROJECT_DIR}` and credentials
   - Copy to Saiku datasources folder (e.g., `saiku/repository/datasources/`)
   - Restart Saiku server

### Step 3: Deploy Schema

1. **Validate schema:**

   ```bash
   java -jar mondrian.jar -validate ecommerce_catalog.xml
   ```

2. **Register with Saiku:**
   - Start Saiku: `/opt/saiku/bin/start-saiku.sh`
   - Open browser: `http://localhost:8080/saiku`
   - Click **Data Sources**
   - Add new Mondrian connection
   - Name: `ecommerce_bi_olap`
   - Schema: `ecommerce_catalog.xml`
   - JDBC URL: `jdbc:mysql://localhost:3306/ecommerce_bi`
   - Test connection

3. **Verify schema loaded:**
   - Go to **Browse** in Saiku
   - Should see `SalesCube` available for querying

### Step 4: Test OLAP Cube

1. **Create new query in Saiku:**
   - Click **Create Query**
   - Select `SalesCube`
   - Drag dimensions to axes:
     - Rows: Product → Category
     - Columns: Time → Year
   - Measures: Revenue, Quantity, Avg_Basket

2. **Execute sample MDX query:**

   ```mdx
   SELECT
   NON EMPTY [Product].[Product].Members ON ROWS,
   NON EMPTY [Time].[Time].[Year].Members ON COLUMNS
   FROM [SalesCube]
   WHERE ([Measures].[Revenue])
   ```

3. **Expected results:**
   - Product revenue aggregated correctly with no duplication
   - Measures available: Revenue, Quantity, Order_Count, Return_Count, Refund_Amount, Satisfaction, Avg_Basket

### Step 5: Create Dashboards

**In Saiku Analytics:**

1. Create new dashboard
2. Add query results as visualizations:
   - Bar chart: Revenue by Region
   - Line chart: Revenue trend over time
   - Heat map: Revenue by Channel × Category
   - KPI cards: Total Revenue, Avg Satisfaction

3. Save dashboard as "Sales Analytics Dashboard"

### Step 6: Performance Tuning

**Aggregate optimization:**

1. In Saiku, generate aggregate suggestions:

   ```sql
   SELECT * FROM MONDRIAN_AGGREGATES
   WHERE AGGREGATE_USAGE > 1000
   ORDER BY AGGREGATE_USAGE DESC;
   ```

2. Create physical aggregate tables for top queries:

   ```sql
   CREATE TABLE AGG_SALES_BY_CHANNEL_MONTH AS
   SELECT
     ChannelKey, TimeKey,
       SUM(Revenue) as Revenue,
       SUM(Quantity) as Quantity,
       SUM(ReturnCount) as ReturnCount,
       SUM(RefundAmount) as RefundAmount
    FROM vw_fact_orders_olap
   GROUP BY ChannelKey, TimeKey;
   ```

3. Register aggregate usage in Mondrian only after validating base cube queries.

**Cache management:**

```properties
mondrian.cell.cacheSize=50000
mondrian.query.cacheSize=1000
mondrian.rolap.agg.compileCacheSize=50
```

---

## Integration Checklist

- [ ] Database created (ecommerce_bi)
- [ ] Pentaho database connection configured
- [ ] Data generator run successfully
- [ ] All ETL transformations tested individually
- [ ] Master job executes without errors
- [ ] Data in all dimension and fact tables verified
- [ ] Mondrian connection configured
- [ ] Schema file validated
- [ ] Saiku cube available for queries
- [ ] Sample MDX queries execute successfully
- [ ] Dashboards created and working
- [ ] Performance baseline established
- [ ] Error handling and emails tested
- [ ] Backup procedures documented
- [ ] Team training completed

---

## Troubleshooting

### Pentaho Issues

**Connection fails:**

- Check database server is running
- Verify credentials in connection settings
- Test with MySQL client: `mysql -u bi_user -p ecommerce_bi`
- Check firewall ports (3306 for MySQL, 5432 for PostgreSQL)

**Transformation fails:**

- Check CSV files exist in correct paths
- Verify column names match in transformations
- Check log files for detailed error messages
- Run single steps to isolate problems

**Performance slow:**

- Check batch size (too large = memory issues, too small = slow)
- Monitor database server resources
- Add indexes to fact tables
- Consider parallel processing

### Mondrian Issues

**Schema validation fails:**

- Check all dimension and fact table names exist
- Verify foreign key relationships
- Check column name spelling
- Review mondrian.log for details

**No data in cube:**

- Verify ETL completed successfully
- Check Mondrian JDBC connection
- Validate schema references correct tables
- Try manual MDX query in query analyzer

**Slow OLAP queries:**

- Check cache settings
- Consider aggregate tables
- Review database indexes
- Monitor SQL queries in logs

---

## Support Resources

- Data Model: `docs/DATA_MODEL.md`
- ETL Documentation: `docs/ETL_DOCUMENTATION.md`
- MDX Queries: `docs/MDX_QUERIES.md`
- Pentaho Documentation: https://pentaho.com/docs
- Mondrian Documentation: http://mondrian.pentaho.com/documentation/
- Saiku Wiki: https://github.com/meteorite/saiku/wiki
