# Power BI Dashboard Quick-Start Checklist

## Pre-Launch Checklist ✓

### Week 1: Planning & Setup
- [ ] **Database Access**
  - [ ] Test MySQL/PostgreSQL connection
  - [ ] Verify all tables exist and contain data
  - [ ] Confirm user has SELECT permissions
  - [ ] Get actual server address, username, password

- [ ] **Environment Setup**
  - [ ] Download & install Power BI Desktop (latest version)
  - [ ] Create dedicated folder for .pbix file
  - [ ] Set up backup location (OneDrive/SharePoint recommended)

- [ ] **Business Requirements**
  - [ ] Identify stakeholders and their needs
  - [ ] Define KPI targets (monthly revenue goals, service levels)
  - [ ] List required dimensions for slicing (channels, regions, products)
  - [ ] Determine refresh frequency (daily, weekly?)

### Week 2: Data & Modeling
- [ ] **Import Data**
  - [ ] Connect to database (MySQL or PostgreSQL)
  - [ ] Import all required tables
  - [ ] Set data types correctly in Power Query
  - [ ] Remove nulls and duplicates

- [ ] **Model Setup**
  - [ ] Create relationships between fact and dimension tables
  - [ ] Verify cardinality (Many:1 for all fact-to-dim)
  - [ ] Mark DIM_TIME as date table
  - [ ] Hide unnecessary business columns

- [ ] **Create Base Measures**
  - [ ] [Total Revenue]
  - [ ] [Total Orders]
  - [ ] [Active Customers]
  - [ ] [Return Rate %]

### Week 3: Dashboard Development
- [ ] **Page 1: Executive Overview** ← START HERE
  - [ ] KPI cards (Revenue, Orders, Avg Basket, Return Rate)
  - [ ] Revenue trend (last 12 months)
  - [ ] Channel performance donut
  - [ ] Add slicers (Date, Channel, Region)

- [ ] **Page 2: Product Performance**
  - [ ] Top 10 products bar chart
  - [ ] Category tree map
  - [ ] Product detail table
  - [ ] Add filters for category, date range

- [ ] **Page 3: Customer Insights**
  - [ ] Customer KPI cards
  - [ ] Segment distribution pie
  - [ ] Top 20 customers table
  - [ ] Churn risk heatmap (optional)

- [ ] **Page 4: Geographic Analysis**
  - [ ] Regional performance map
  - [ ] Regional detail table
  - [ ] Delivery status breakdown
  - [ ] Add region slicer

### Week 4: Refinement
- [ ] **Interactivity**
  - [ ] Configure cross-filtering between pages
  - [ ] Test all slicer combinations
  - [ ] Set drill-down paths
  - [ ] Create bookmarks for quick views

- [ ] **Formatting & Polish**
  - [ ] Apply consistent color scheme
  - [ ] Format numbers (currency, %, whole numbers)
  - [ ] Add descriptive titles and tooltips
  - [ ] Remove clutter, align visuals

- [ ] **Testing**
  - [ ] Test with different date ranges
  - [ ] Verify all calculations are correct
  - [ ] Check performance (load time < 10 seconds)
  - [ ] Review with business stakeholder

- [ ] **Deployment**
  - [ ] Save PBIX file to secure location
  - [ ] Upload to Power BI Service
  - [ ] Configure refresh schedule
  - [ ] Set up sharing & permissions

---

## Quick Formula Reference

### Copy-Paste Ready DAX Formulas

```dax
// KPI: Total Monthly Revenue
Total Revenue = SUM('FACT_ORDERS'[Revenue])

// KPI: Month-over-Month Growth
Revenue MoM Growth % = 
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = CALCULATE([Total Revenue], PREVIOUSMONTH('DIM_TIME'[FullDate]))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)

// KPI: Year-to-Date Revenue
Revenue YTD = CALCULATE([Total Revenue], DATESYTD('DIM_TIME'[FullDate]))

// KPI: Total Orders This Month
Orders This Month = 
CALCULATE(
    DISTINCTCOUNT('FACT_ORDERS'[OrderID]),
    MONTH('DIM_TIME'[FullDate]) = MONTH(TODAY()),
    YEAR('DIM_TIME'[FullDate]) = YEAR(TODAY())
)

// KPI: Customer Count
Active Customers = DISTINCTCOUNT('FACT_ORDERS'[CustomerKey])

// KPI: Return Rate Percentage
Return Rate % = DIVIDE(
    COALESCE(COUNTROWS('FACT_RETURNS'), 0),
    DISTINCTCOUNT('FACT_ORDERS'[OrderID]),
    0
)

// Rank products by revenue (for Top 10 filtering)
Product Rank = RANKX(ALL('DIM_PRODUCT'), [Total Revenue],, DESC)
Top 10 Product = IF([Product Rank] <= 10, "Yes", "No")

// Segment ranking (for Top 20 customers)
Customer Rank = RANKX(ALL('DIM_CUSTOMER'), [Total Revenue],, DESC)
Top 20 Customer = IF([Customer Rank] <= 20, "Yes", "No")
```

### Most Common Dashboard Needs

| Need | Measure | DAX Snippet |
|------|---------|-----------|
| **Compare This vs Last Month** | Revenue MoM Growth % | `DIVIDE([Revenue] - [Revenue Previous Month], [Revenue Previous Month])` |
| **Year-to-Date Total** | Revenue YTD | `CALCULATE([Total Revenue], DATESYTD('DIM_TIME'[FullDate]))` |
| **Top N Entities** | Product Rank | `RANKX(ALL('DIM_PRODUCT'), [Total Revenue],, DESC)` |
| **Percentage Share** | Channel Mix % | `DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL('DIM_CHANNEL')))` |
| **Distinct Count** | Active Customers | `DISTINCTCOUNT('FACT_ORDERS'[CustomerKey])` |
| **Running Total** | Cumulative Revenue | Use Matrix visual with cumulative sum setting |
| **Aggregation Ratio** | Return Rate % | `DIVIDE([Return Count], [Total Orders])` |

---

## Common Mistakes to Avoid

### ❌ Data Model Errors
- **Missing relationships**: Charts show blanks or zeros if tables aren't connected
  - Fix: Go to Model view and verify all Many:1 relationships
  
- **Inactive relationships**: Only first relationship is used by default
  - Fix: Set correct relationship as Active (bold line in diagram)
  
- **Wrong cardinality**: If revenue values double or triple unexpectedly
  - Fix: Data model relationships must be Many(*):1 not Many:Many

### ❌ Calculation Errors
- **Measure sums instead of counts**: Returns 50 instead of 25 customers
  - Fix: Use DISTINCTCOUNT() instead of COUNT()
  
- **Empty/null measures**: Shows blank or #DIV/0!
  - Fix: Use COALESCE() or wrap in IFERROR() for safety
  ```dax
  Safe Measure = IFERROR([Risky Measure], 0)
  ```

- **Context not filtering correctly**: Number doesn't change when slicer is used
  - Fix: Check if relationship is properly configured

### ❌ Performance Issues
- **Dashboard takes >10 seconds to load**: Too complex
  - Fix: Remove unnecessary visuals, aggregate data further, use DAX Studio to profile

- **Refresh fails or takes hours**: Data import is too slow
  - Fix: Filter import (add WHERE clauses), use DirectQuery for large tables, implement incremental refresh

- **Out of memory error**: PBIX file is too large
  - Fix: Archive old data, remove low-value columns, summarize data in SQL layer

### ❌ Design Issues
- **Dashboard too wide**: Users must scroll horizontally
  - Fix: Use 1920x1080 as target, keep to 1 screen width

- **Too many colors used**: Confusing to read
  - Fix: Use max 5-7 colors total across dashboard, consistent color meaning

- **Unreadable text**: Font too small
  - Fix: Minimum font size = 12pt for body, 18pt+ for titles

---

## Advanced Tips & Tricks

### 1. Dynamic Date Filtering (Without Slicers)

Create a "Comparison" measure that always shows previous period:

```dax
// Let users type any date range; automatically compares to prior period
Prior Period Revenue = 
VAR DateRange = MAX('DIM_TIME'[FullDate]) - MIN('DIM_TIME'[FullDate])
RETURN
CALCULATE(
    [Total Revenue],
    DATEADD('DIM_TIME'[FullDate], -DateRange - 1, DAY)
)

Revenue vs Prior = 
DIVIDE(
    [Total Revenue] - [Prior Period Revenue],
    [Prior Period Revenue]
)
```

### 2. Conditional Formatting Rules

Apply data bars to tables:

**In Power BI Table Visual**:
1. Select column (e.g., Revenue)
2. Conditional formatting → Data bars
3. Set colors: Red (negative), Green (positive)
4. Configure minimum/maximum colors

### 3. Bookmarks for Quick Navigation

Create pre-filtered views without UI clutter:

1. **Bookmark 1**: "Latest Month" 
   - Date filter: Last month only
   - Hide legend and unnecessary visuals
   
2. **Bookmark 2**: "Year-to-Date Comparison"
   - Date filter: 1st Jan to Today
   - Show YTD measures

3. **Bookmark 3**: "High-Risk Customers"
   - Customer segment filter: "Dormant"
   - Sort by churn risk score

### 4. Custom Tooltips

Add richer tooltips beyond default values:

**For Revenue Chart**:
- Show: Revenue amount, % of total, growth vs prior year, target

**In Visual properties**:
1. Format pane → Tooltip page
2. Add fields: [Total Revenue], [Revenue YoY Growth %], [Target Revenue]

### 5. Real-Time Alerts (Premium Feature)

If using Power BI Premium:

1. Go to metric card
2. Set alert threshold (e.g., "Alert me if Revenue < $100K")
3. Recipients receive email when threshold is breached

### 6. Paginated Reports (Alternative to Dashboard)

For formal reporting, create Paginated Reports (PBIX + RDL format):
- Better for printing
- Multi-page formats
- Parameter-driven filtering
- Scheduled distribution via email

---

## Sample Dashboard Naming Convention

Save files with this structure:

```
PowerBI/
├── BI_E-Commerce_Dashboard_v1.0.pbix  (Current production)
├── BI_E-Commerce_Dashboard_v0.9.pbix  (Backup)
├── DashboardDesign.pptx                (Screenshots for design review)
├── MeasureLibrary.xlsx                 (Backup of DAX formulas)
└── RefreshLog.xlsx                     (Track refresh errors)
```

**Version numbering**:
- v1.0 = Production ready
- v0.9 = Testing in progress
- v0.5 = Under development

---

## Deployment Checklist

### Step 1: Save & Backup
```
☐ Save as: BI_E-Commerce_Dashboard_v1.0.pbix
☐ Create backup copy (vX.X date format)
☐ Store in OneDrive or SharePoint (version control)
```

### Step 2: Publish to Power BI Service
```
☐ Open BI_E-Commerce_Dashboard_v1.0.pbix
☐ File → Publish → Select Workspace
☐ Workspace name: "E-Commerce Analytics"
☐ Name: "Executive Dashboard" in service
```

### Step 3: Configure Refresh
```
☐ Power BI Service → Semantic Model → Settings
☐ Configure Scheduled Refresh:
   ☐ Frequency: Daily (recommended)
   ☐ Time: 6:00 AM UTC (before business hours)
   ☐ Timezone: Your local timezone
☐ Test refresh: Click "Refresh now"
☐ Check refresh history for errors
```

### Step 4: Set Up Sharing
```
☐ Share with: Finance team, Management
☐ Permissions: View (not Edit)
☐ Individual users or Security groups (recommended)
☐ Send welcome email with dashboard link
```

### Step 5: Validate in Service
```
☐ Test all slicers work
☐ Check data freshness vs. database
☐ Verify drill-down interactions work
☐ Test on mobile view (if needed)
```

---

## 30-Day Refinement Plan

### Week 1
- Dashboard live and refreshing
- Collect stakeholder feedback
- Track any data issues

### Week 2
- Refine visuals based on feedback
- Add missing calculations
- Optimize performance

### Week 3
- Add advanced features (dynamic titles, custom colors)
- Create user guide documentation
- Train business users

### Week 4
- Final testing and sign-off
- Archive feedback log
- Schedule quarterly review

---

## Helpful Resources

**Online Learning**:
- Power BI Desktop tutorial: https://learn.microsoft.com/en-us/power-bi/fundamentals/
- DAX formula cookbook: https://dax.guide/
- Community examples: https://community.powerbi.com/t5/Data-Stories-Gallery/ct-p/DataStoriesGallery

**Tools**:
- DAX Studio (free): Advanced query profiling
- Tabular Editor (free): Edit data model quickly  
- Power BI Performance Analyzer: Built-in (View → Performance Analyzer)

**Database Connection Troubleshooting**:
- MySQL: Check port 3306 is open
- PostgreSQL: Check port 5432 is open
- Test connection: `mysql -u username -p -h server_address` (from command line)

