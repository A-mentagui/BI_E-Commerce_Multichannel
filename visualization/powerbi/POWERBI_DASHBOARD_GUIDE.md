# Complete Power BI Dashboard Guide - E-Commerce Analytics

## Table of Contents
1. [Prerequisites & Setup](#prerequisites--setup)
2. [Data Source Connection](#data-source-connection)
3. [Data Modeling](#data-modeling)
4. [DAX Measures & Calculations](#dax-measures--calculations)
5. [Dashboard Pages](#dashboard-pages)
6. [Interactivity & Filters](#interactivity--filters)
7. [Performance Optimization](#performance-optimization)
8. [Best Practices](#best-practices)

---

## Prerequisites & Setup

### 1. Install Power BI Desktop
- Download from: https://powerbi.microsoft.com/en-us/desktop/
- Minimum requirements: Windows 10/11, 4GB RAM, 2GB disk space
- Latest version recommended for best DAX and visualization features

### 2. Database Access
Ensure you have access to one of:
- **MySQL Database** (default setup)
- **PostgreSQL Database** (alternative setup)

Get connection details:
- **Server**: localhost or your server IP
- **Database**: `ecommerce_warehouse` (or your database name)
- **Username**: Your DB username
- **Password**: Your DB password

### 3. Required Tables
Verify these tables exist in your warehouse:
```
FACT_ORDERS
DIM_TIME
DIM_PRODUCT
DIM_CUSTOMER
DIM_CHANNEL
DIM_REGION
DIM_DELIVERY
FACT_RETURNS
DIM_FEEDBACK
```

---

## Data Source Connection

### Step 1: Open Power BI Desktop

### Step 2: Get Data from Database

1. **Click**: Home > Get Data > Database > MySQL Database (or PostgreSQL)
2. **Server**: Enter your database server address
3. **Database**: Enter `ecommerce_warehouse`
4. **Data Connectivity Mode**: Select **Import** (recommended for performance)
   - Import = Data loaded into Power BI (faster, larger file size)
   - DirectQuery = Real-time queries (slower, smaller file size)

### Step 3: Select Tables

Select all required tables:
- ✓ FACT_ORDERS
- ✓ DIM_TIME
- ✓ DIM_PRODUCT
- ✓ DIM_CUSTOMER
- ✓ DIM_CHANNEL
- ✓ DIM_REGION
- ✓ DIM_DELIVERY
- ✓ FACT_RETURNS
- ✓ DIM_FEEDBACK

### Step 4: Load & Transform (Power Query)

1. Click **Transform Data** to open Power Query Editor
2. **Remove unnecessary columns** from each table:
   - Keep only business-relevant columns
   - Remove intermediate keys if business keys exist

3. **Clean Data**:
   - Change column types (dates as Date, currencies as Decimal)
   - Remove duplicates if any
   - Handle null values

4. **Example transformations for DIM_TIME**:
   ```
   - FullDate: Change to Date type
   - IsWeekend: Change to Boolean
   - Quarter: Change to Whole Number
   - Ensure Sort By Order: Month Name sorted by Month number
   ```

5. Click **Close & Apply** to load data

---

## Data Modeling

### Step 1: Manage Relationships

Navigate to: **Model** view (top toolbar)

#### Create Relationships (Fact to Dimensions):

| From | To | Cardinality | Active |
|------|----|-----------  |--------|
| FACT_ORDERS[TimeKey] | DIM_TIME[TimeKey] | Many:1 | ✓ |
| FACT_ORDERS[ProductKey] | DIM_PRODUCT[ProductKey] | Many:1 | ✓ |
| FACT_ORDERS[CustomerKey] | DIM_CUSTOMER[CustomerKey] | Many:1 | ✓ |
| FACT_ORDERS[ChannelKey] | DIM_CHANNEL[ChannelKey] | Many:1 | ✓ |
| FACT_ORDERS[RegionKey] | DIM_REGION[RegionKey] | Many:1 | ✓ |
| FACT_ORDERS[DeliveryKey] | DIM_DELIVERY[DeliveryKey] | Many:1 | ✓ |
| FACT_RETURNS[OrderKey] | FACT_ORDERS[OrderKey] | Many:1 | ✓ |

**Steps to create relationship**:
1. Drag key column from one table to another
2. Verify: **Cardinality** = Many (*) to One (1)
3. **Cross filter direction** = Single (star schema best practice)
4. Click **OK**

### Step 2: Organize Tables

Create table groups for better navigation:
- **Fact Tables**: FACT_ORDERS, FACT_RETURNS
- **Dimensions**: All DIM_* tables
- **Calculations**: Create dedicated "Measures" table for DAX calculations

### Step 3: Configure Column Properties

For each dimension table:

1. **Mark as Date Table** (for DIM_TIME):
   - Right-click DIM_TIME > Mark as Date Table
   - Set FullDate as date column
   - Enables time intelligence functions

2. **Set Data Categories**:
   - DIM_REGION[CountryName] → Category = Geography > Country/Region
   - DIM_REGION[City] → Category = Geography > City
   - Enables map visualizations

3. **Hide unnecessary columns**:
   - Right-click column > Hide in Report View
   - Keep only business-friendly columns visible

---

## DAX Measures & Calculations

### Create Measures Table

1. In Model view, right-click on a table name
2. Select **New Table**
3. Enter: `Measures = ROW()`
4. Add all measures below to this table

### Core Revenue Measures

```dax
// TOTAL REVENUE
Total Revenue = SUM('FACT_ORDERS'[Revenue])

// REVENUE COMPARISON
Revenue Current Month = 
CALCULATE(
    [Total Revenue],
    MONTH('DIM_TIME'[FullDate]) = MONTH(TODAY()),
    YEAR('DIM_TIME'[FullDate]) = YEAR(TODAY())
)

Revenue Previous Month = 
CALCULATE(
    [Total Revenue],
    PREVIOUSMONTH('DIM_TIME'[FullDate])
)

Revenue MoM Growth = 
[Total Revenue] - [Revenue Previous Month]

Revenue MoM Growth % = 
DIVIDE(
    [Revenue MoM Growth],
    [Revenue Previous Month],
    0
)

// YTD REVENUE
Revenue YTD = 
CALCULATE(
    [Total Revenue],
    DATESYTD('DIM_TIME'[FullDate])
)

// LY COMPARISON
Revenue Last Year = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR('DIM_TIME'[FullDate])
)

Revenue YoY Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Last Year],
    [Revenue Last Year],
    0
)
```

### Order & Quantity Measures

```dax
// ORDERS
Total Orders = DISTINCTCOUNT('FACT_ORDERS'[OrderID])

Orders This Month = 
CALCULATE(
    [Total Orders],
    MONTH('DIM_TIME'[FullDate]) = MONTH(TODAY()),
    YEAR('DIM_TIME'[FullDate]) = YEAR(TODAY())
)

// QUANTITY
Total Quantity = SUM('FACT_ORDERS'[Quantity])

Avg Quantity per Order = DIVIDE([Total Quantity], [Total Orders], 0)

// BASKET METRICS
Avg Basket Value = DIVIDE([Total Revenue], [Total Orders], 0)

Avg Order Value = [Avg Basket Value]
```

### Returns & Quality Metrics

```dax
// RETURNS
Total Returns = COALESCE(COUNTROWS('FACT_RETURNS'), 0)

Return Rate % = 
DIVIDE(
    [Total Returns],
    [Total Orders],
    0
)

Return Rate % Formatted = 
FORMAT([Return Rate %], "0.00%")

// QUALITY SCORE
Quality Score = 1 - [Return Rate %]

Revenue from Returned Orders = 
CALCULATE(
    [Total Revenue],
    FILTER(
        'FACT_ORDERS',
        [OrderKey] IN VALUES('FACT_RETURNS'[OrderKey])
    )
)

Lost Revenue from Returns = 
[Revenue from Returned Orders]
```

### Customer Metrics

```dax
// CUSTOMERS
Active Customers = DISTINCTCOUNT('FACT_ORDERS'[CustomerKey])

New Customers This Month = 
CALCULATE(
    DISTINCTCOUNT('FACT_ORDERS'[CustomerKey]),
    MONTH('DIM_TIME'[FullDate]) = MONTH(TODAY()),
    YEAR('DIM_TIME'[FullDate]) = YEAR(TODAY())
)

Repeat Customers = 
CALCULATE(
    DISTINCTCOUNT('FACT_ORDERS'[CustomerKey]),
    FILTER(
        ALL('FACT_ORDERS'),
        COUNTROWS(
            FILTER(
                ALL('FACT_ORDERS'),
                'FACT_ORDERS'[CustomerKey] = EARLIER('FACT_ORDERS'[CustomerKey])
            )
        ) > 1
    )
)

// CUSTOMER VALUE
Revenue per Customer = 
DIVIDE(
    [Total Revenue],
    [Active Customers],
    0
)

Customers with Repeat Purchases = 
VAR CustomerOrders = 
    ADDCOLUMNS(
        SUMMARIZE('FACT_ORDERS', 'FACT_ORDERS'[CustomerKey]),
        "OrderCount", COUNTX(
            FILTER('FACT_ORDERS', 'FACT_ORDERS'[CustomerKey] = EARLIER('FACT_ORDERS'[CustomerKey])),
            'FACT_ORDERS'[OrderID]
        )
    )
RETURN
    COUNTX(FILTER(CustomerOrders, [OrderCount] > 1), [CustomerKey])
```

### Channel Performance

```dax
// CHANNEL ANALYSIS
Channel Count = DISTINCTCOUNT('DIM_CHANNEL'[ChannelKey])

Revenue by Channel = 
CALCULATE(
    [Total Revenue],
    ALL('FACT_ORDERS')
)

Top Channel = 
MAXX(
    SUMMARIZE('FACT_ORDERS', 'DIM_CHANNEL'[ChannelName]),
    [Total Revenue]
)

Channel Mix % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL('DIM_CHANNEL')),
    0
)
```

### Time Intelligence Measures

```dax
// PERIOD COMPARISONS
Revenue QTD = 
CALCULATE(
    [Total Revenue],
    DATESQTD('DIM_TIME'[FullDate])
)

Revenue Last 12 Months = 
CALCULATE(
    [Total Revenue],
    DATESBETWEEN(
        'DIM_TIME'[FullDate],
        TODAY()-365,
        TODAY()
    )
)

Days Sales Outstanding = 
DIVIDE(
    [Avg Basket Value],
    CALCULATE([Total Revenue], ALL('DIM_TIME')) / 365,
    0
)
```

### Discount & Margin (if applicable)

```dax
// DISCOUNT
Total Discount = SUM('FACT_ORDERS'[Discount])

Discount Rate % = 
DIVIDE(
    [Total Discount],
    [Total Revenue],
    0
)

// MARGIN (estimated 35% base margin)
Est. Cost = [Total Revenue] * 0.65

Est. Gross Margin = [Total Revenue] - [Est. Cost]

Est. Margin % = 
DIVIDE(
    [Est. Gross Margin],
    [Total Revenue],
    0
)

Net Margin After Discount = 
DIVIDE(
    [Est. Gross Margin] - [Total Discount],
    [Total Revenue],
    0
)
```

### Ranking & Top Items

```dax
// PRODUCT RANKING
Product Rank = 
RANKX(
    ALL('DIM_PRODUCT'),
    [Total Revenue],,
    DESC
)

Top 10 Product Flag = 
IF([Product Rank] <= 10, "Yes", "No")

// CUSTOMER RANKING
Customer Rank = 
RANKX(
    ALL('DIM_CUSTOMER'),
    [Total Revenue],,
    DESC
)

Top 20 Customer Flag = 
IF([Customer Rank] <= 20, "Yes", "No")

// REGION RANKING
Region Rank = 
RANKX(
    ALL('DIM_REGION'),
    [Total Revenue],,
    DESC
)
```

---

## Dashboard Pages

### Page 1: Executive Overview / KPI Dashboard

**Purpose**: High-level metrics for C-suite executives

#### Layout:
```
┌─────────────────────────────────────────────────┐
│  Executive Summary - E-Commerce Performance     │
├─────────────┬──────────────┬──────────────┬─────┤
│   Revenue   │  Total Orders│  Avg Basket  │Return│
│   [KPI]     │    [KPI]     │   Value      │ Rate │
│             │              │   [KPI]      │[KPI] │
├─────────────────────────────────────────────────┤
│                                                 │
│  Revenue Trend (Last 12 Months)                │
│  [Line Chart showing monthly trend]            │
│                                                 │
├─────────────────────────────────────────────────┤
│ Channel Mix      │      Orders by Month        │
│ [Donut Chart]    │      [Column Chart]         │
└─────────────────────────────────────────────────┘
```

#### Visualizations:

**1. KPI Cards** (Top Section)
- **Total Revenue**
  - Measure: [Total Revenue]
  - Format: $#,##0.00
  - Add trend indicator: MoM Growth %
  
- **Total Orders**
  - Measure: [Total Orders]
  - Format: #,##0
  - Add comparison: vs Last Month
  
- **Avg Basket Value**
  - Measure: [Avg Basket Value]
  - Format: $#,##0.00
  
- **Return Rate**
  - Measure: [Return Rate % Formatted]
  - Format: 0.00%

**2. Revenue Trend** (Line Chart)
- **X-axis**: DIM_TIME[MonthName] (sorted by Month number)
- **Y-axis**: [Total Revenue]
- **Legend**: None (single line)
- **Add**: Goal line for target revenue
- **Features**: 
  - Enable data labels
  - Add trend line
  - Show forecast (optional)

**3. Channel Performance** (Donut/Pie Chart)
- **Legend**: DIM_CHANNEL[ChannelName]
- **Values**: [Total Revenue]
- **Data labels**: Show %
- **Tooltip**: Include revenue amount

**4. Orders by Month** (Column Chart)
- **X-axis**: DIM_TIME[Month]
- **Y-axis**: [Total Orders]
- **Color**: By [Return Rate %] (gradient)
- **Tooltip**: Include revenue, orders, return rate

### Page 2: Product Performance

**Purpose**: Inventory and sales analysis by category

```
┌─────────────────────────────────────────────────┐
│  Product Performance Analysis                   │
├─────────────────────────────────────────────────┤
│  Top 10 Products (By Revenue)                  │
│  [Horizontal Bar Chart]                        │
│                                                 │
├─────────────────────────────────────────────────┤
│ Category TreeMap  │  Product Performance Table  │
│ [TreeMap Chart]   │  [Matrix Visual]            │
│                   │                             │
└─────────────────────────────────────────────────┘
```

#### Visualizations:

**1. Top 10 Products** (Horizontal Bar Chart)
- **X-axis**: [Total Revenue] (descending)
- **Y-axis**: DIM_PRODUCT[ProductName] (top 10)
- **Color**: By [Return Rate %]
- **Data labels**: Revenue amount
- **Filter**: [Top 10 Product Flag] = "Yes"

**2. Category TreeMap**
- **Legend**: DIM_PRODUCT[Category]
- **Values**: [Total Revenue]
- **Size**: [Total Quantity]
- **Color**: [Margin %]
- **Enable drill-down** to Sub-category level

**3. Product Performance Table** (Matrix)
- **Rows**: 
  - DIM_PRODUCT[Category]
  - DIM_PRODUCT[SubCategory]
  - DIM_PRODUCT[ProductName]
- **Values**:
  - [Total Revenue]
  - [Total Quantity]
  - [Return Rate %]
  - [Avg Basket Value]
- **Sort**: By Revenue descending
- **Subtotals**: Hide row subtotals for cleaner view

**4. Product Summary Card** (Alternative)
- **Measure**: [Active SKUs] (count of products with sales)
- Add comparison vs previous period

### Page 3: Customer Insights

**Purpose**: Customer segmentation, RFM analysis, and churn risk

```
┌─────────────────────────────────────────────────┐
│  Customer Intelligence & RFM Analysis           │
├─────────────┬──────────────┬──────────────────┤
│ Active Cust │ New Cust     │  Repeat Cust     │
│ [KPI]       │ [KPI]        │  [KPI]           │
├─────────────────────────────────────────────────┤
│  Customer Segment Distribution                 │
│  [Pie Chart showing RFM segments]              │
│                                                 │
├─────────────────────────────────────────────────┤
│ Top 20 Customers by Value                      │
│ [Table with Customer, Revenue, Segment]        │
│                                                 │
├─────────────────────────────────────────────────┤
│ Churn Risk by Region (Heatmap)                │
│ [Heatmap: Rows=Region, Cols=Segment]          │
└─────────────────────────────────────────────────┘
```

#### Visualizations:

**1. Customer KPI Cards**
- **Active Customers**: [Active Customers]
- **New This Month**: [New Customers This Month]
- **Repeat Customers**: [Customers with Repeat Purchases]
- **Avg Customer Value**: [Revenue per Customer]

**2. Customer Segment Distribution** (Pie Chart)
- **Legend**: DIM_CUSTOMER[Segment]
  - (Assuming segments: Loyal, Regular, New, Dormant)
- **Values**: [Active Customers]
- **Data labels**: Count and %

**3. Top 20 Customers** (Table/Matrix)
- **Columns**:
  - DIM_CUSTOMER[CustomerName]
  - DIM_CUSTOMER[Segment]
  - DIM_CUSTOMER[Region]
  - [Total Revenue]
  - [Total Orders]
  - [Avg Order Value]
- **Filter**: [Top 20 Customer Flag] = "Yes"
- **Sort**: Revenue descending

**4. Churn Risk Heatmap** (Matrix Visual)
- **Rows**: DIM_REGION[RegionName]
- **Columns**: DIM_CUSTOMER[Segment]
- **Values**: [Active Customers]
- **Color gradient**: 
  - Green = Low churn (Loyal)
  - Red = High churn (Dormant/New)

**5. Customer Lifetime Value Distribution** (Scatter/Bubble)
- **X-axis**: [Avg Order Value]
- **Y-axis**: [Total Orders] per customer
- **Size**: [Total Revenue]
- **Legend**: DIM_CUSTOMER[Segment]
- **Identify**: High-value targets

### Page 4: Geographic & Operations Analysis
 
**Purpose**: Regional performance and delivery metrics

```
┌─────────────────────────────────────────────────┐
│  Geographic & Operational Performance           │
├─────────────────────────────────────────────────┤
│  Map: Revenue by Region/City                   │
│  [Map Visual showing revenue bubbles]          │
│                                                 │
├─────────────────────────────────────────────────┤
│ Regional Performance Table         │ Delivery   │
│ [Table by Region]                  │ by Status  │
│                                    │ [Pie Chart]│
└─────────────────────────────────────────────────┘
```

#### Visualizations:

**1. Revenue Map** (ArcGIS Map or Filled Map)
- **Location**: DIM_REGION[Country], DIM_REGION[City]
- **Bubble size**: [Total Revenue]
- **Color**: [Order Count]
- **Tooltip**: Region, Revenue, Orders, Customers

**2. Regional Performance Table** (Matrix)
- **Rows**: 
  - DIM_REGION[Country]
  - DIM_REGION[State/Region]
- **Values**:
  - [Total Revenue]
  - [Total Orders]
  - [Active Customers]
  - [Return Rate %]
  - [Avg Basket Value]
- **Conditional formatting**: Green/Red for revenue trends

**3. Delivery Status Distribution** (Pie/Donut Chart)
- **Legend**: DIM_DELIVERY[DeliveryStatus]
  - (On-Time, Late, Returned, Cancelled)
- **Values**: [Count of Orders]
- **Enable drill-down**: Show by region

**4. Delivery Performance by Region** (Clustered Bar)
- **X-axis**: [Delivery On-Time %]
- **Y-axis**: DIM_REGION[RegionName]
- **Additional bars**: Avg Delivery Days

---

## Interactivity & Filters

### Add Global Filters (Slicers)

**Slicers to add to each page**:

1. **Date Range Slicer** (Top of Page)
   - Field: DIM_TIME[FullDate]
   - Type: Between
   - Style: Timeline (visual, scrollable)
   - Applies to: All charts except year-over-year

2. **Channel Slicer**
   - Field: DIM_CHANNEL[ChannelName]
   - Type: List
   - Allows multiple selection ✓
   - Default: All selected

3. **Region Slicer**
   - Field: DIM_REGION[Country] or [Region]
   - Type: Dropdown
   - Allows multiple selection ✓

4. **Category Slicer** (Page 2 & 3 only)
   - Field: DIM_PRODUCT[Category]
   - Type: List with search

5. **Segment Slicer** (Page 3 only)
   - Field: DIM_CUSTOMER[Segment]
   - Type: Buttons
   - Options: All, Loyal, Regular, New, Dormant

### Enable Drill-Down Behaviors

**Page 1 - Executive Overview**:
- Click on Month → Drill to Week
- Click on Channel → Show detailed metrics

**Page 2 - Products**:
- TreeMap: Click Category → Expand to Subcategory → Product

**Page 4 - Geographic**:
- Map: Click Region → Zoom to cities
- Table: Expand Country → City level

### Configure Tooltip Behaviors

**Cross-filtering rules**:
1. Date filter affects ALL pages (time dimension)
2. Channel filter affects ALL pages  
3. Region filter affects ALL pages
4. Product filter affects only Product & Orders (not Customer)

**Disable cross-filter** between:
- Customer metrics ←→ Product metrics
- Non-related dimensions

### Page Navigation (Bookmarks)

Create bookmarks for quick views:

1. **Executive Summary** (Default)
   - All slicers visible
   - Current month data

2. **Deep Dive - Last Quarter**
   - Date range: Last 3 months
   - All dimensions visible

3. **Competitor Comparison** (Optional)
   - Show external benchmarks
   - Custom date selection

---

## Performance Optimization

### 1. Data Model Optimization

**Reduce file size**:
- Hide columns not needed for reports
- Remove duplicate data before import
- Use INT instead of BIGINT where possible
- Archive old data (> 3 years)

### 2. DAX Query Optimization

**Best practices**:
```dax
// ❌ Inefficient - Evaluates for every row
Bad Measure = COUNTROWS(
    FILTER(
        ALL('DIM_CUSTOMER'),
        [Total Revenue] > 1000
    )
)

// ✓ Efficient - Uses aggregation
Better Measure = 
VAR HighValueCustomers = 
    CALCULATE(
        DISTINCTCOUNT('FACT_ORDERS'[CustomerKey]),
        FILTER(ALL('FACT_ORDERS'), [Total Revenue] > 1000)
    )
RETURN
    HighValueCustomers
```

**Key rules**:
- Use SUMMARIZE instead of nested FILTER where possible
- Avoid CONTAINS() in large datasets; use IN VALUES() instead
- Use variable assignments (VAR) for complex calculations
- Minimize CALCULATE contexts

### 3. Report Performance

**Reduce visual clutter**:
- Limit visuals per page to 6-8 (avoid >10)
- Use summarized tables (not detail rows)
- Remove unnecessary columns from tables
- Use sampling for very large datasets (100k+ rows)

**Aggregation levels**:
- KPI page: Month level
- Detail pages: Day level max
- Avoid showing all 1000+ products; use Top N

### 4. Caching Strategy

- **Import mode**: Refresh daily (off-peak hours)
- **DirectQuery**: Not recommended for this dashboard
- **Incremental refresh**: For fact tables > 1GB

### 5. Refresh Schedule

In Power BI Service:
1. **Semantic Model** > **Settings** > **Refresh**
2. Set schedule:
   - Morning: 6 AM (before business hours)
   - Afternoon: 2 PM (mid-day check)
   - Frequency: 1-2x daily recommended

---

## Best Practices

### 1. Naming Conventions

- **Tables**: FACT_ORDERS, DIM_PRODUCT (follow database names)
- **Measures**: [Total Revenue], [Revenue YoY Growth %] (brackets)
- **Columns**: Avoid underscores; use spaces for display

### 2. Formatting Standards

| Data Type | Format | Example |
|-----------|--------|---------|
| Currency | $#,##0.00 | $15,234.99 |
| Percentage | 0.00% | 12.34% |
| Whole Number | #,##0 | 1,234 |
| Decimal | 0.0 | 1.5 |
| Date | MMM DD, YYYY | Jan 15, 2024 |

### 3. Color Scheme

- **Recommended**: Use corporate/brand colors
- **Diverging scales**: 
  - Revenue trends: Green (positive) to Amber (neutral) to Red (negative)
  - Return rates: Green (low) to Red (high)
- **Avoid**: Too many colors; max 5-7 distinct colors per visual

### 4. Dashboard Design Principles

✓ **DO:**
- Use white space effectively
- Arrange visuals by importance (top-left = most critical)
- Consistent font sizes and colors
- Clear, descriptive titles
- Provide context (vs. target, vs. last period)
- Use consistent chart types for same metric types

✗ **DON'T:**
- Clutter with every possible metric
- Use pie charts for >5 categories (use bar instead)
- Mix different color schemes randomly
- Create reports wider than screen (force scrolling)
- Use "fancy" visualizations that obscure data

### 5. Security & Sharing

**In Power BI Service**:

1. **Row-Level Security (RLS)** (Optional):
   - If users should only see their region
   - Configure in Modeling > Manage Roles

2. **Sharing**:
   - Share specific reports with teams
   - Use workspaces for collaboration
   - Set permissions: View, Edit, Reshare

3. **Data Governance**:
   - Refresh schedule aligned with data availability
   - Version control: Keep backup PBIX files
   - Document changes in metadata

### 6. Maintenance Checklist

**Monthly**:
- [ ] Review refresh logs for errors
- [ ] Check data freshness vs. accuracy
- [ ] Monitor overall file size (should be < 1GB)

**Quarterly**:
- [ ] Review KPI targets vs. actuals
- [ ] Update forecast models if needed
- [ ] Archive old data slices

**Annually**:
- [ ] Performance review of all measures
- [ ] Update dimension tables (new categories, regions)
- [ ] Complete redesign if business needs change

### 7. Troubleshooting Common Issues

**Problem**: Slow dashboard / high load times
- **Solution**: 
  - Check data model relationships
  - Profile DAX queries (Performance Analyzer)
  - Remove unnecessary visuals
  - Use aggregate tables for pre-calculated summaries

**Problem**: Incorrect sums/measures showing
- **Solution**:
  - Verify fact table grain (one row = one order?)
  - Check relationships (Many:1 correct?)
  - Review filter context in measures

**Problem**: "This visual exceeds the query complexity limit"
- **Solution**:
  - Simplify measure (remove FILTER, use SUMMARIZE)
  - Remove unnecessary sorting
  - Separate complex logic into multiple measures

---

## Sample DAX Template Structure

Create a new Power BI file with this measure structure:

```dax
// ==============================
// 1. FACT TABLE MEASURES
// ==============================

// Revenue family
Total Revenue = SUM('FACT_ORDERS'[Revenue])
Revenue MoM Growth % = DIVIDE([Total Revenue] - [Revenue Previous Month], [Revenue Previous Month], 0)

// Orders family
Total Orders = DISTINCTCOUNT('FACT_ORDERS'[OrderID])
Orders MoM Change = [Total Orders] - [Orders Previous Month]

// ==============================
// 2. TIME INTELLIGENCE
// ==============================

Revenue YTD = CALCULATE([Total Revenue], DATESYTD('DIM_TIME'[FullDate]))
Revenue Last Year = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('DIM_TIME'[FullDate]))

// ==============================
// 3. DIMENSIONAL METRICS
// ==============================

Active Customers = DISTINCTCOUNT('FACT_ORDERS'[CustomerKey])
Return Rate % = DIVIDE([Total Returns], [Total Orders], 0)
Revenue per Customer = DIVIDE([Total Revenue], [Active Customers], 0)

// ==============================
// 4. RANKING & FILTERING
// ==============================

Product Rank = RANKX(ALL('DIM_PRODUCT'), [Total Revenue],, DESC)
Top 10 Flag = IF([Product Rank] <= 10, "Yes", "No")
```

---

## Next Steps

1. ✓ Set up database connection
2. ✓ Load and model data tables
3. ✓ Create all DAX measures in "Measures" table
4. ✓ Build Page 1 (Executive Overview)
5. ✓ Build Page 2 (Product Performance)
6. ✓ Build Page 3 (Customer Insights)
7. ✓ Build Page 4 (Geographic Analysis)
8. ✓ Configure slicers and cross-filtering
9. ✓ Format colors, fonts, and layout
10. ✓ Test all interactions and drill-downs
11. ✓ Publish to Power BI Service
12. ✓ Set refresh schedule
13. ✓ Share with stakeholders

---

## Resources

- **Power BI Documentation**: https://docs.microsoft.com/en-us/power-bi/
- **DAX Function Reference**: https://dax.guide/
- **Best Practices**: https://powerbi.microsoft.com/en-us/blog/
- **Community Forum**: https://community.powerbi.com/

---

## Support & Contact

For database connection issues or data model questions, refer to:
- `docs/DOCUMENTATION_INDEX.md` - Complete documentation map
- `docs/ETL_DOCUMENTATION.md` - Data pipeline details
- `docs/implementation/DATA_MODEL.md` - Detailed schema description

