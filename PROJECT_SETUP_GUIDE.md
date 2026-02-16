# BI E-commerce Project Setup Guide

## Overview

This guide provides two setup paths for the BI E-commerce project: **Minimal Setup** (essential tools only for core functionality) and **Optimal Setup** (full stack for advanced features). The project implements a complete BI solution with ETL, OLAP cube, data mining, and visualization.

### Project Components

- **Data Generation**: Python scripts create synthetic e-commerce data
- **ETL**: Pentaho Data Integration loads data into warehouse
- **OLAP Cube**: Mondrian schema for multi-dimensional analysis
- **Data Mining**: Python scripts for RFM analysis, churn prediction, association rules
- **Visualization**: Dashboards and reports

### Prerequisites (Both Setups)

- **OS**: Windows 10/11, Linux, or macOS
- **Java**: JDK 8+ (required for Pentaho and Mondrian)
- **Database**: MySQL 8.0+ or PostgreSQL 12+ (MySQL recommended)
- **Python**: 3.8+ with packages: pandas, numpy, faker, scikit-learn
- **Git**: For version control

---

## Minimal Setup

### What You Get

- Core ETL and OLAP functionality
- Basic data mining and visualization
- Reduced complexity and setup time

### Required Tools

- Pentaho Data Integration (PDI) 9.3+
- Mondrian Schema Workbench 4.0+
- Power BI Desktop (free)
- Python 3.8+

### Step-by-Step Setup

#### 1. Install Prerequisites

```bash
# Install Python and required packages
pip install pandas numpy faker scikit-learn

# Install Java JDK
# Download from: https://adoptium.net/
# Set JAVA_HOME environment variable
```

#### 2. Setup Database

```bash
# MySQL setup
mysql -u root -p
CREATE DATABASE ecommerce_bi;
CREATE USER 'bi_user'@'localhost' IDENTIFIED BY 'bi_password';
GRANT ALL PRIVILEGES ON ecommerce_bi.* TO 'bi_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Load schema
mysql -u bi_user -p ecommerce_bi < sql/setup_database.sql
```

#### 3. Generate Synthetic Data

```bash
cd /path/to/project
python scripts/generate_data.py
```

#### 4. Install and Configure Pentaho PDI

1. Download PDI from: https://pentaho.com/download/
2. Extract to `C:\pentaho\pdi` (Windows) or `/opt/pentaho` (Linux)
3. Set environment: `PENTAHO_HOME=/path/to/pdi`
4. Launch Spoon: `spoon.bat` (Windows) or `spoon.sh` (Linux)

#### 5. Configure Database Connection in PDI

1. Open Spoon
2. View → Database Connections → New
3. Configure:
   - Name: `ecommerce_bi`
   - Type: MySQL
   - Host: `localhost`
   - Database: `ecommerce_bi`
   - User: `bi_user`
   - Password: `bi_password`
4. Test connection

#### 6. Run ETL Jobs

1. Open `etl/Master_Job.kjb`
2. Run the job
3. Verify data loaded:

```sql
SELECT COUNT(*) FROM DIM_CUSTOMER;  -- 10,000
SELECT COUNT(*) FROM FACT_ORDERS;   -- 50,000
```

#### 7. Install Mondrian Schema Workbench

1. Download from: https://sourceforge.net/projects/mondrian/
2. Extract to `C:\mondrian` or `/opt/mondrian`
3. Launch: `workbench.bat` or `workbench.sh`

#### 8. Validate OLAP Schema

1. File → Open → `olap/ecommerce_catalog.xml`
2. Tools → Validate Schema (should pass)
3. Tools → Test Cube Connection (should succeed)

#### 9. Install Power BI Desktop

1. Download from: https://powerbi.microsoft.com/desktop/
2. Install and launch

#### 10. Connect Power BI to Database

1. Get Data → MySQL database
2. Server: `localhost`, Database: `ecommerce_bi`
3. Import tables: DIM*\*, FACT*\*, vw_fact_orders_olap
4. Create relationships between dimensions and facts
5. Build dashboards for:
   - Revenue by channel/product
   - Customer segmentation (RFM)
   - Churn analysis

#### 11. Run Data Mining Scripts

```bash
python scripts/rfm_analysis.py
python scripts/churn_prediction.py
python scripts/association_rules.py
```

### Minimal Setup Verification

- ETL completes without errors
- Cube validates in Workbench
- Power BI connects and shows data
- Python scripts generate results in `results/`

---

## Optimal Setup

### What You Get

- Full BI stack with advanced visualization
- Web-based OLAP querying
- Professional reporting capabilities
- Maximum project features

### Required Tools

- All Minimal Setup tools PLUS:
- Saiku Analytics 3.x
- Pentaho Report Designer
- MySQL Connector/J (JDBC driver)

### Additional Setup Steps

#### 1. Install Saiku Analytics

1. Download from: https://github.com/meteorite/saiku/releases
2. Extract to `C:\saiku` or `/opt/saiku`
3. Copy MySQL JDBC driver to `saiku/server/lib/`
4. Configure datasource in `saiku/repository/datasources/ecommerce_bi.properties`:

```
type=OLAP
name=ecommerce_bi_olap
driver=mondrian.olap4j.MondrianOlap4jDriver
location=jdbc:mondrian:JdbcDrivers=com.mysql.cj.jdbc.Driver;Jdbc=jdbc:mysql://localhost:3306/ecommerce_bi;JdbcUser=bi_user;JdbcPassword=bi_password;Catalog=file:///path/to/olap/ecommerce_catalog.xml
```

5. Start Saiku: `saiku/bin/start-saiku.sh`
6. Access: http://localhost:8080/saiku

#### 2. Test OLAP Queries in Saiku

1. Create New Query → Select SalesCube
2. Build queries:
   - Revenue by Product Category and Year
   - Customer satisfaction by channel
   - Return rates by region

#### 3. Install Pentaho Report Designer

1. Download from Pentaho community edition
2. Install and launch
3. Connect to `ecommerce_bi` database
4. Create reports:
   - Sales summary reports
   - Customer analysis reports
   - Inventory reports

#### 4. Advanced Power BI Configuration

1. Connect to Mondrian cube (if possible via XMLA)
2. Import data mining results from `results/`
3. Create advanced dashboards:
   - Real-time sales monitoring
   - Predictive analytics views
   - Executive summary

#### 5. Docker Environment (Optional)

Use provided `docker-compose.yml` for containerized setup:

```bash
docker-compose up -d
```

### Optimal Setup Features

- Web-based OLAP analysis (Saiku)
- Professional PDF/Excel reports (Report Designer)
- Advanced Power BI visualizations
- Containerized deployment option

---

## Common Issues and Solutions

### Database Connection Issues

- Verify MySQL/PostgreSQL is running
- Check user permissions: `GRANT ALL ON ecommerce_bi.* TO 'bi_user'@'localhost';`
- Test connection: `mysql -u bi_user -p ecommerce_bi`

### ETL Failures

- Check CSV file paths in transformations
- Verify column names match database schema
- Review PDI logs for detailed errors

### Mondrian Schema Issues

- Validate XML syntax
- Ensure table/column names match database
- Check foreign key relationships

### Power BI Connection

- Use MySQL connector for Power BI
- Import fact and dimension tables separately
- Create relationships manually if auto-detect fails

### Saiku Issues

- Verify JDBC driver in correct location
- Check Mondrian catalog path in datasource config
- Review Saiku logs for startup errors

---

## Project Workflow

### Daily Operations

1. Generate/update data: `python scripts/generate_data.py`
2. Run ETL: Execute `Master_Job.kjb` in PDI
3. Validate cube: Open schema in Mondrian Workbench
4. Analyze data: Use Power BI/Saiku for queries
5. Run mining: Execute Python analysis scripts

### Development Workflow

1. Modify data generation in `scripts/generate_data.py`
2. Update ETL transformations in PDI
3. Edit OLAP schema in `olap/ecommerce_catalog.xml`
4. Test changes in Workbench
5. Deploy to production visualization tools

---

## Performance Optimization

### Database

- Add indexes on frequently queried columns
- Partition large fact tables by date
- Use connection pooling

### ETL

- Increase batch sizes for large datasets
- Use parallel processing where possible
- Monitor memory usage

### OLAP

- Create aggregate tables for common queries
- Enable Mondrian caching
- Use Saiku query caching

### Visualization

- Schedule data refreshes during off-peak hours
- Use Power BI dataflows for complex transformations
- Optimize DAX measures for performance

---

## Backup and Recovery

### Database Backup

```bash
mysqldump -u bi_user -p ecommerce_bi > backup.sql
```

### ETL Backup

- Export PDI jobs/transformations as XML
- Version control all .kjb and .ktr files

### Configuration Backup

- Backup database connection settings
- Save Mondrian datasource configurations
- Export Power BI reports as .pbix files

---

## Support and Resources

### Documentation

- `docs/DATA_MODEL.md`: Database schema details
- `docs/ETL_DOCUMENTATION.md`: ETL process guide
- `docs/MDX_QUERIES.md`: OLAP query examples
- `olap_guide.md`: OLAP deployment guide

### External Resources

- Pentaho Wiki: https://pentaho.com/docs
- Mondrian Documentation: http://mondrian.pentaho.com
- Power BI Documentation: https://docs.microsoft.com/power-bi
- Saiku Wiki: https://github.com/meteorite/saiku/wiki

### Community Support

- Pentaho Forums: https://forums.pentaho.com
- Power BI Community: https://community.powerbi.com
- Stack Overflow tags: pentaho, mondrian, powerbi

---

## Next Steps

1. Choose your setup path (Minimal or Optimal)
2. Install prerequisites
3. Follow step-by-step instructions
4. Test each component
5. Start building your BI dashboards

For issues or questions, refer to the troubleshooting section or check the project documentation.
