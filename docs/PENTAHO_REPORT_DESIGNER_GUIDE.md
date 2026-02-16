# Pentaho Report Designer vs Power BI - Complete Comparison

## Quick Answer

**Pentaho Report Designer (PRD)** is better if you need:

- Pixel-perfect, formatted reports for printing/PDF export
- Enterprise-grade scheduling and distribution
- Open-source solution with no licensing costs
- Integration with existing Pentaho ecosystem (PDI, Mondrian)

**Power BI** is better if you need:

- Interactive self-service dashboards
- Real-time data refresh
- Advanced AI insights and recommendations
- Better mobile experience

---

## How to Use Pentaho Report Designer Instead of Power BI

### 1. Installation

**Windows:**

```bash
# Download from: https://sourceforge.net/projects/pentaho/files/Report%20Designer/
# Extract to C:\report-designer
# Set JAVA_HOME environment variable
# Run: C:\report-designer\report-designer.bat
```

**Linux:**

```bash
cd /opt
sudo unzip prd-ce-10.2.0.0-218.zip
sudo mv prd-ce-10.2.0.0-218 report-designer
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
cd /opt/report-designer && ./report-designer.sh
```

**Docker:** Use provided docker-compose.yml:

```bash
docker-compose up report-designer -d
# Access at http://localhost:6080
```

### 2. Configure Database Connection

1. Launch PRD
2. **Admin → Data Sources → New**
3. Configure:
   - **Name**: `ecommerce_bi`
   - **Driver Class**: `com.mysql.cj.jdbc.Driver`
   - **Connection URL**: `jdbc:mysql://localhost:3306/ecommerce_bi?useSSL=false&serverTimezone=UTC`
   - **User**: `bi_user`
   - **Password**: `bi_password`
4. Click **Test Connection**

### 3. Create a Report

**Step 1: New Report**

- File → New Report → Blank Report

**Step 2: Add Data Source**

- Data → Add Data Source → Select `ecommerce_bi`
- Enter SQL query:

```sql
SELECT
  p.ProductName,
  c.ChannelName,
  SUM(f.OrderAmount) as Revenue,
  COUNT(f.OrderID) as Orders,
  AVG(f.OrderAmount) as AvgOrder
FROM vw_fact_orders_olap f
JOIN DIM_PRODUCT p ON f.ProductKey = p.ProductKey
JOIN DIM_CHANNEL c ON f.ChannelKey = c.ChannelKey
GROUP BY p.ProductName, c.ChannelName
ORDER BY Revenue DESC
```

**Step 3: Design Layout**

- Drag title, table, and charts from palette
- Format with colors, fonts, borders
- Add parameters for interactive filtering

**Step 4: Preview & Export**

- File → Preview → Select format (PDF, Excel, HTML)
- Save to location

### 4. Build Reports for Your Project

**Report 1: Sales Summary Dashboard**

- Tables: Revenue by product, channel, region
- Charts: Revenue trend, channel distribution, regional performance
- Metrics: Total revenue, order count, avg order value

**Report 2: Customer RFM Analysis**

```sql
SELECT
  cust.CustomerName,
  cust.Segment,
  COUNT(DISTINCT f.OrderID) as Frequency,
  MAX(f.OrderDate) as LastPurchase,
  SUM(f.OrderAmount) as TotalValue,
  DATEDIFF(NOW(), MAX(f.OrderDate)) as RecencyDays
FROM DIM_CUSTOMER cust
LEFT JOIN vw_fact_orders_olap f ON cust.CustomerKey = f.CustomerKey
GROUP BY cust.CustomerID, cust.CustomerName, cust.Segment
ORDER BY TotalValue DESC
```

**Report 3: Returns & Refund Analysis**

```sql
SELECT
  p.ProductName,
  COUNT(f.ReturnCount) as Returns,
  SUM(f.RefundAmount) as RefundAmount,
  ROUND(100.0 * COUNT(f.ReturnCount) / COUNT(f.OrderID), 2) as ReturnRate,
  AVG(f.Satisfaction) as AvgSatisfaction
FROM vw_fact_orders_olap f
JOIN DIM_PRODUCT p ON f.ProductKey = p.ProductKey
WHERE f.ReturnCount > 0
GROUP BY p.ProductName
ORDER BY Returns DESC
```

**Report 4: Regional Performance**

```sql
SELECT
  r.RegionName,
  COUNT(f.OrderID) as Orders,
  SUM(f.OrderAmount) as Revenue,
  AVG(f.Satisfaction) as Satisfaction
FROM vw_fact_orders_olap f
JOIN DIM_REGION r ON f.RegionKey = r.RegionKey
GROUP BY r.RegionName
ORDER BY Revenue DESC
```

### 5. Advanced Features

**Parameterized Reports (Interactive Filters)**

- Data → Report Parameters → Add Parameter
- Name: `SelectedChannel`, Type: String
- Use in query: `WHERE ChannelName = ${SelectedChannel}`

**Scheduled Report Distribution**

- Schedule → New Schedule
- Set frequency (daily, weekly, monthly)
- Configure email recipients
- Select output format (PDF, Excel)

**Conditional Formatting**

- Select element → Properties
- Add conditional highlighting (e.g., revenue > $100K = green)

**Subreports**

- Embed smaller reports within main report
- Create linked/drill-through functionality

### 6. Export and Distribution

**Manual Export:**

- File → Preview → Choose format (PDF, Excel, HTML)

**Command Line Export:**

```bash
prd-run.bat ^
  -input "Sales_Summary.prpt" ^
  -output "Sales_Summary.pdf" ^
  -file-type pdf
```

**Email Distribution:**

- Set up SMTP in PRD settings
- Configure scheduled report runs
- Automatically email to stakeholders

**Web Embedding:**

```html
<iframe
  src="http://pentaho-server:8080/pentaho/api/repos/reports/Sales_Summary.prpt/viewer"
  width="100%"
  height="600"
></iframe>
```

### 7. Comparison Table

| Feature                    | PRD              | Power BI         |
| -------------------------- | ---------------- | ---------------- |
| **Cost**                   | Free             | $10/user/month   |
| **PDF Reports**            | ⭐⭐⭐ Excellent | ⭐⭐ Good        |
| **Interactive Dashboards** | ⭐⭐ Moderate    | ⭐⭐⭐ Excellent |
| **Real-time Analytics**    | Scheduled        | Real-time        |
| **Learning Curve**         | Moderate         | Moderate         |
| **Enterprise Features**    | ⭐⭐⭐           | ⭐⭐⭐           |
| **Mobile Support**         | Limited          | ⭐⭐⭐           |
| **Embedding**              | Yes              | Yes              |
| **Self-Service BI**        | Limited          | Excellent        |

### 8. Integration Steps with Your Project

1. **After ETL runs successfully** (Master_Job.kjb completes):
   - Data is in database tables

2. **In Mondrian Workbench** (validate cube):
   - Verify all dimensions and facts load correctly

3. **Create PRD reports** instead of Power BI:
   - Use database views and tables directly
   - Create formatted reports for stakeholders
   - Schedule daily/weekly distribution

4. **Import data mining results**:
   - RFM analysis → Create customer segmentation report
   - Churn predictions → Create high-risk customer alert report
   - Association rules → Create product recommendation report

### 9. Workflow Comparison

**With Power BI:**

```
ETL → Database → Power BI (Import Data) → Dashboard
      (Direct connection, real-time refresh)
```

**With Pentaho Report Designer:**

```
ETL → Database → PRD (Query via JDBC) → PDF/Excel Reports
      (Scheduled export, formatted for distribution)
```

### 10. When to Choose Each

**Choose PRD if:**

- You need professional PDF reports for printing
- You want enterprise scheduling/distribution
- Your stakeholders prefer formatted documents
- You need pixel-perfect layouts
- You want open-source, no licensing costs
- You're using other Pentaho tools

**Choose Power BI if:**

- You need interactive, self-service dashboards
- Stakeholders want real-time data views
- You need advanced AI/ML analytics
- You need strong mobile support
- Your organization has Microsoft licensing

**Hybrid Approach (Recommended):**

- Use PDI for ETL (data loading)
- Use Mundrian Workbench for OLAP cube design
- Use **PRD for official report distribution** (formal reporting)
- Use **Power BI for interactive exploration** (self-service BI)

This gives you the best of both worlds: structured reports for management + interactive dashboards for analysts.

---

Save the comprehensive guide I provided (the long markdown block) to a new file in your docs folder. You now have all the information needed to replace Power BI with Pentaho Report Designer!
