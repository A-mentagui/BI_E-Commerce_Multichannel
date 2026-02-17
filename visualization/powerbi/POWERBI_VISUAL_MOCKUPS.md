# Power BI Dashboard Layout & Visual Reference Guide

## Dashboard Overview

This guide provides visual mockups and specific recommendations for each dashboard page.

---

## Page 1: Executive Overview / KPI Dashboard

### Full Page Layout (1920x1080)

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║  EXECUTIVE SUMMARY - E-Commerce Performance                                        ║
║  Filters: [Date Range ▼] [Channel ▼] [Region ▼]         Last Updated: Today 6 AM  ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                     ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  ┌─────────────┐ ║
║  │  Total Revenue   │  │  Total Orders    │  │ Avg Basket Val  │  │ Return Rate │ ║
║  │ $2,345,678       │  │ 12,456           │  │ $188.30         │  │   3.2%      │ ║
║  │ ↑ 12.5% vs prev  │  │ ↑ 8.3% vs prev   │  │ ↑ 2.1% vs prev  │  │ ↓ 0.5% vs p │ ║
║  └──────────────────┘  └──────────────────┘  └─────────────────┘  └─────────────┘ ║
║                                                                                     ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │ Revenue Trend - Last 12 Months                                              │  ║
║  │                                                                            $ │  ║
║  │  2.5M  ╱╲                                         ╱╲                       ▲ │  ║
║  │  2.0M  ║ ╲      ╱╲                        ╱╲    ╱  ╲                       │ ║
║  │  1.5M  ║  ╲╱╲  ║  ╲  ╱╲                 ╱  │╲  ╱    ╲                      │ ║
║  │  1.0M  ║     ╲ ║   ╲╱  ╲    ╱╲      ╱╲╱   │ ╲╱      ╲  ← 12-month trend  │ ║
║  │        ├──────────────────────────────────────────────────                 │  ║
║  │        J F M A M J J A S O N D              Average: $2.1M                │  ║
║  │        Goal: $2.5M (currently 94% of target)                              │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                     ║
║  ┌──────────────────────────────┐  ┌───────────────────────────────────────────┐  ║
║  │ Revenue by Channel           │  │ Orders by Month                           │  ║
║  │ ┌────────────────────────────┤  │ Orders                                    │  ║
║  │ │ Online   45% ████████████  │  │ 1,200 ┌──┐  ┌──┐  ┌──┐           ┌──┐   │  ║
║  │ │ Retail   35% ██████████    │  │ 1,000 │  │  │  │  │  │  ┌──┐    │  │   │  ║
║  │ │ Mobile   15% ████          │  │   800 │  │  │  │  │  │  │  │    │  │   │  ║
║  │ │ Wholesale 5% █             │  │   600 │  │  │  │  │  │  │  │    │  │   │  ║
║  │ │                            │  │   400 └──┘  └──┘  └──┘  └──┘    └──┘   │  ║
║  │ │ Total: $2.3M               │  │       J F M A M J J A S O N D          │  ║
║  │ └────────────────────────────┤  │                                         │  ║
║  └──────────────────────────────┘  └───────────────────────────────────────────┘  ║
║                                                                                     ║
╚════════════════════════════════════════════════════════════════════════════════════╝
```

### Specific Visualization Details

#### KPI Cards (Top Section)

```
Card 1: Total Revenue
├─ Title: "Total Revenue"
├─ Main Value: $2,345,678
├─ Subtitle: "vs Previous Month"
├─ Trend Value: +$265,432 (↑ 12.5%)
├─ Background Color: Light blue
├─ Accent Color: Green (positive trend)
└─ Icon: Dollar sign ($)

Card 2: Total Orders
├─ Main Value: 12,456
├─ Subtitle: "Current Month YTD"
├─ Trend: ↑ 8.3% vs previous month
├─ Target: 12,000 (104% of target) ✓
└─ Icon: Shopping cart

Card 3: Avg Basket Value
├─ Main Value: $188.30
├─ Calc: Revenue / Orders
├─ Trend: ↑ 2.1%
└─ Icon: Basket

Card 4: Return Rate
├─ Main Value: 3.2%
├─ Calc: Returns / Orders
├─ Trend: ↓ 0.5% (GOOD! Lower is better)
├─ Background Color: Light green (good metric)
└─ Icon: Box/Return symbol
```

#### Revenue Trend Chart

```
Chart Type: Line Chart with Area
├─ X-Axis: Month (Jan - Dec)
├─ Y-Axis: Revenue ($0 - $3,000,000)
├─ Line Color: Royal Blue
├─ Area Fill: Light blue (40% opacity)
├─ Features:
│   ├─ Data labels: Show every other month value
│   ├─ Trend line: Linear (optional)
│   ├─ Target line: Horizontal at $2.5M (dashed red)
│   └─ Tooltip: Show exact value, % of target, growth %
├─ Sorting: January to December (time order)
└─ Data Source: FACT_ORDERS, grouped by Month/Year

Measures:
├─ [Total Revenue] per month
└─ Optional: [Revenue YTD] as secondary line
```

#### Channel Performance (Donut/Pie Chart)

```
Chart Type: Donut Chart (Pie also acceptable)
├─ Legend Position: Right side
├─ Legend Items:
│   ├─ Online: 45% (Royal Blue)
│   ├─ Retail: 35% (Forest Green)
│   ├─ Mobile: 15% (Orange)
│   └─ Wholesale: 5% (Gray)
├─ Data Labels:
│   ├─ Category name: "Online"
│   └─ Percentage: "45%"
│   ├─ Revenue amount: "$1,045,461"
├─ Interactions:
│   ├─ Click a segment → All charts filter to that channel
│   └─ Tooltip shows: Channel, Revenue, Orders, % of total
└─ Colors: Use distinct colors, avoid red/green combo

Data Source: FACT_ORDERS grouped by DIM_CHANNEL[ChannelName]
Measure: [Total Revenue]
```

#### Orders by Month (Column Chart with Color Encoding)

```
Chart Type: Clustered Column Chart
├─ X-Axis: Month (Jan - Dec)
├─ Y-Axis: Order Count (0 - 1,500)
├─ Column Color: Gradient based on [Return Rate %]
│   ├─ Green: Low return rate (1-2%)
│   ├─ Yellow: Medium (2.5-3.5%)
│   └─ Red: High (>4%)
├─ Data Labels: Show count on top of column (optional)
├─ Sorting: Time order (January → December)
└─ Tooltip: Order count, Revenue, Return Rate %, Avg Order Value

Data Source: FACT_ORDERS
Dimension: DIM_TIME[Month]
Measures:
├─ [Total Orders]
└─ Color by [Return Rate %]

Alternative Color Scheme: By Channel instead of Return Rate
```

### Slicer Configuration

```
DATE RANGE SLICER (Top Left)
├─ Type: Timeline (visual, scrollable)
├─ Field: DIM_TIME[FullDate]
├─ Default: Last 12 months
├─ Selection: Between (range selection enabled)
└─ Position: Top-left corner

CHANNEL SLICER (Top, Below Date)
├─ Type: Buttons or List
├─ Field: DIM_CHANNEL[ChannelName]
├─ Multi-select: Enabled
├─ Default: All selected
├─ Width: 50% of page
└─ Items: Online, Retail, Mobile, Wholesale

REGION SLICER (Top Right)
├─ Type: Dropdown
├─ Field: DIM_REGION[Country]
├─ Multi-select: Enabled
├─ Default: All selected
├─ Search enabled: Yes
└─ Width: 25% of page
```

---

## Page 2: Product Performance

### Full Page Layout

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║  PRODUCT PERFORMANCE ANALYSIS                                                      ║
║  Filter by: [Product Category ▼]  [Date Range ▼]                                  ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                     ║
║  Top 10 Products by Revenue                                                        ║
║  ┌──────────────────────────────────────────────────────────────────────────────┐  ║
║  │  Product Z          $456,789  ████████████████████████░  Orange  23% return   │  ║
║  │  Product X          $398,234  ███████████████████░░░░░░  Green   2% return    │  ║
║  │  Product Y          $387,654  ██████████████████░░░░░░░  Blue    5% return    │  ║
║  │  Product W          $325,678  ████████████████░░░░░░░░░  Red     8% return    │  ║
║  │  Product V          $298,456  ███████████████░░░░░░░░░░  Orange  4% return    │  ║
║  │  Product U          $267,894  ██████████░░░░░░░░░░░░░░░  Green   1% return    │  ║
║  │  Product T          $245,123  ███████████░░░░░░░░░░░░░░  Green   3% return    │  ║
║  │  Product S          $234,567  ██████████░░░░░░░░░░░░░░░  Blue    1% return    │  ║
║  │  Product R          $198,765  █████████░░░░░░░░░░░░░░░░  Orange  6% return    │  ║
║  │  Product Q          $178,543  ████████░░░░░░░░░░░░░░░░░  Green   2% return    │  ║
║  └──────────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                     ║
║  ┌──────────────────────────────────┐  ┌────────────────────────────────────────┐ ║
║  │ Revenue by Category (TreeMap)    │  │ Product Summary Table                  │ ║
║  │                                  │  │ ┌─────────────────────────────────────┐│ ║
║  │  ┌─────────┐  ┌──────────┐      │  │ │ Category  │ Revenue │ Qty│ Return % ││ ║
║  │  │       A │  │  B       │      │  │ │───────────├─────────├────├──────────│ ║
║  │  │  27%    │  │   18%    │      │  │ │ Electronics                        ││ ║
║  │  │$623K    │  │ $414K    │      │  │ │  - Phones   $456K  1.2K    3.2%  ││ ║
║  │  │ 45 items│  │ 67 items │      │  │ │  - Tablets  $328K  0.8K    5.1%  ││ ║
║  │  └─────────┘  │          │      │  │ │  - Laptops  $298K  0.4K    2.8%  ││ ║
║  │               │ (more..) │      │  │ │ Clothing                          ││ ║
║  │               └──────────┘      │  │ │  - Shirts   $234K  8.9K    1.2%  ││ ║
║  │  ┌─────────┐  ┌──────────┐      │  │ │  - Pants    $198K  4.2K    0.9%  ││ ║
║  │  │    C    │  │  D       │      │  │ │ Home & Garden                     ││ ║
║  │  │  15%    │  │   12%    │      │  │ │  - Furniture$289K  0.3K    4.5%  ││ ║
║  │  │$345K    │  │ $276K    │      │  │ │  - Decor    $145K  2.1K    2.3%  ││ ║
║  │  │ 23 items│  │ 34 items │      │  │ │                                  ││ ║
║  │  └─────────┘  └──────────┘      │  │ └─────────────────────────────────────┘│ ║
║  │  Click category to drill down    │  │ → Hover for full product names        │ ║
║  │     to subcategories             │  │ → Click product for details           │ ║
║  └──────────────────────────────────┘  └────────────────────────────────────────┘ ║
║                                                                                     ║
╚════════════════════════════════════════════════════════════════════════════════════╝
```

### Chart Specifications

#### Top 10 Products (Horizontal Bar)

```
Chart Type: Horizontal Bar Chart (100% better than vertical for long names)
├─ Y-Axis: Product Name (10 items max)
├─ X-Axis: Revenue (Descending, highest at top)
├─ Bar Color: Encoded by [Return Rate %]
│   ├─ Green: 0-2% return rate
│   ├─ Yellow: 2-5%
│   └─ Red: 5%+
├─ Data Labels: Show $ amount at end of bar
├─ Sorting: Revenue descending
├─ Tooltip: 
│   ├─ Product Name
│   ├─ Revenue amount
│   ├─ Units sold
│   ├─ Return %
│   └─ Avg Order Value
└─ Filter Applied: [Top 10 Product Flag] = "Yes"

Measure: [Total Revenue] per DIM_PRODUCT[ProductName]
```

#### Category TreeMap

```
Chart Type: TreeMap (enables drill-down)
├─ Legend: DIM_PRODUCT[Category]
├─ Size: [Total Revenue]
├─ Color Saturation: [Total Quantity]
├─ Tooltip:
│   ├─ Category Name
│   ├─ Revenue & %
│   └─ Item Count
├─ Enable Drill-Down:
│   ├─ Level 1: Category (27% of total, $623K)
│   ├─ Level 2: SubCategory (tap to expand)
│   └─ Breadcrumb: "All > Electronics" (can go back up)
├─ Colors: Use 6-8 distinct colors for main categories
└─ Click behavior: Filter other charts to selected category

Hierarchical Data:
├─ Electronics
│   ├─ Phones  (27% of Electronics)
│   ├─ Tablets (18% of Electronics)
│   └─ Laptops (15% of Electronics)
├─ Clothing
│   ├─ Shirts  (12%)
│   └─ Pants   (10%)
└─ Home & Garden
    ├─ Furniture (8%)
    └─ Decor     (5%)
```

#### Product Detail Table (Matrix Visual)

```
Chart Type: Matrix (or Pivot Table)
├─ Rows:
│   ├─ Level 1: Category (expand/collapse enabled)
│   ├─ Level 2: SubCategory
│   └─ Level 3: ProductName (optional)
├─ Columns: None (or Day if analyzing by date)
├─ Values:
│   ├─ [Total Revenue] (SUM) - formatted as $#,##0
│   ├─ [Total Quantity] (SUM) - formatted as #,##0
│   ├─ [Avg Order Value] - formatted as $#,##0.00
│   └─ [Return Rate %] - formatted as 0.00%
├─ Sorting:
│   ├─ Primary: By [Total Revenue] descending
│   └─ Secondary: By Quantity descending
├─ Conditional Formatting:
│   ├─ Return Rate %: Red/Green gradient (red=high, green=low)
│   └─ Revenue: Data bars in background
├─ Grand Totals: Show at bottom
└─ Subtotals: Show category-level subtotals

Example Output:
┌─ Electronics              $1,082,123   2.5K    $432.58   3.8%
│  ├─ Phones                 $456,789   1.2K    $380.65   3.2%
│  │   - iPhone 14 Pro       $234,567    0.6K    $391.28   2.9%
│  │   - Samsung Galaxy      $145,230    0.4K    $363.08   3.5%
│  ├─ Tablets                $398,234    0.8K    $497.54   5.1%
│  └─ Laptops                $287,100    0.4K    $717.75   2.8%
├─ Clothing               $432,456  13.1K      $32.99    1.0%
│  ├─ Shirts                $234,567    8.9K    $26.35    1.2%
│  └─ Pants                 $197,889    4.2K    $47.12    0.9%
└─ TOTAL                $1,514,579  15.6K     $97.03    2.1%
```

---

## Page 3: Customer Insights

### Full Page Layout

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║  CUSTOMER INTELLIGENCE & RFM ANALYSIS                                              ║
║  Filter by: [Customer Segment ▼] [Date Range ▼]                                   ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                     ║
║  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ║
║  │ Active Cust    │  │ New Cust       │  │ Repeat Cust    │  │ Avg Cust Value │  ║
║  │ 8,234          │  │ 432            │  │ 3,456          │  │ $284.81        │  ║
║  │ ↑ 5.2%         │  │ ↑ 12.1%        │  │ ↑ 8.3%         │  │ ↑ 3.2%         │  ║
║  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘  ║
║                                                                                     ║
║  Customer Segments Distribution               │ Churn Risk by Region (Heatmap)    ║
║  ┌──────────────────────────────┐            │ ┌──────────────────────────────┐  ║
║  │                              │            │ │         Low  Med  High       │  ║
║  │        Loyal                 │            │ │ North   23   45   8          │  ║
║  │       ╱╲ 45%                 │            │ │ South   34   56   12         │  ║
║  │      ╱  ╲  3,710 customers   │            │ │ East    18   34   6          │  ║
║  │     ╱────╲                   │            │ │ West    27   48   15         │  ║
║  │            Regular 32%       │            │ │ Central 42   67   20         │  ║
║  │            2,630 customers   │            │ │ Cost:   -Low   -- Med  +High │  ║
║  │  New  ╲    ╱                 │            │ └──────────────────────────────┘  ║
║  │   16%  ╲  ╱                  │            │ [Dark shades = higher risk]        ║
║  │  1,316 ╲╱   Dormant 7%       │            │                                   ║
║  │           576 customers      │            │ Click cell to see details          ║
║  │ (Hover to see value details) │            │                                   ║
║  └──────────────────────────────┘            │                                   ║
║                                                                                     ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │ Top 20 Customers by Lifetime Value                                          │  ║
║  │ ┌───────────────────────────────────────────────────────────────────────────┐ ║
║  │ │ Customer Name      │  Segment  │ Region │ CLV      │ Orders │ Last Order  │ ║
║  │ │────────────────────┼───────────┼────────┼──────────┼────────┼─────────────│ ║
║  │ │ John Smith         │ Loyal     │ North  │ $18,456  │   47   │ 2 days ago  │ ║
║  │ │ Sarah Johnson      │ Loyal     │ East   │ $16,789  │   42   │ 1 week ago  │ ║
║  │ │ Mike Davis        │ Regular   │ South  │ $14,234  │   28   │ 3 days ago  │ ║
║  │ │ Jennifer Lee      │ Loyal     │ North  │ $13,567  │   35   │ Today       │ ║
║  │ │ Robert Martinez   │ Loyal     │ West   │ $12,890  │   31   │ 5 days ago  │ ║
║  │ │ ...               │ ...       │ ...    │ ...      │ ...    │ ...         │ ║
║  │ │ (20 rows shown)                                                           │ ║
║  │ └───────────────────────────────────────────────────────────────────────────┘ ║
║  │                                                                               │ ║
║  │ → Click customer name to drill to order history                              │ ║
║  │ → Segment colors indicate loyalty level                                      │ ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                     ║
╚════════════════════════════════════════════════════════════════════════════════════╝
```

### Chart Specifications

#### Customer Segment Pie Chart

```
Chart Type: Pie Chart (or Donut with center label)
├─ Legend Fields: DIM_CUSTOMER[Segment]
│   ├─ Loyal      (45%, 3,710 customers)
│   ├─ Regular    (32%, 2,630 customers)
│   ├─ New        (16%, 1,316 customers)
│   └─ Dormant     (7%, 576 customers)
├─ Values: [Active Customers] (count)
├─ Colors: Distinct per segment
│   ├─ Loyal      = Dark Green (best)
│   ├─ Regular    = Light Green
│   ├─ New        = Blue
│   └─ Dormant    = Red (at risk)
├─ Data Labels: Show name + percentage
├─ Legend Position: Right side
├─ Tooltip:
│   ├─ Segment name
│   ├─ Customer count
│   ├─ % of total
│   ├─ Revenue generated
│   └─ Avg spend per customer
└─ Interaction: Click segment to filter other charts

Segments Definition (RFM-based):
├─ Loyal: Purchased in last 30 days, 5+ orders total
├─ Regular: Purchased in last 90 days, 2-4 orders
├─ New: First purchase in last 30 days
└─ Dormant: No purchase in last 365 days
```

#### Churn Risk Heatmap (Matrix)

```
Chart Type: Matrix (Heatmap)
├─ Rows: DIM_REGION[RegionName] (5-10 regions)
├─ Columns: DIM_CUSTOMER[Segment] (4 segments)
├─ Values: [Active Customers] (count, heat intensity)
├─ Color Gradient:
│   ├─ Light Green = Low risk (Loyal, high count)
│   ├─ Yellow = Medium risk (Regular)
│   └─ Dark Red = High risk (Dormant, low count)
│   
│ Interpretation:
│ Dark red cells = Many dormant customers in that region
│ Growth opportunity = Many new customers
│ Stable = Mostly loyal + regular
├─ Data Labels: Show count in each cell
├─ Formatting: Center text, bold numbers
└─ Tooltip:
    ├─ Region
    ├─ Segment
    ├─ Customer count
    └─ % of region total

Example Heat Pattern:
           Loyal  Regular  New  Dormant
North       23      45     8      5
South       34      56    12      8      ← High at-risk (many dormant)
East        18      34     6      3
West        27      48    15      6
Central     42      67    20      9      ← Growth opportunity (many new)
```

#### Top 20 Customers Table

```
Chart Type: Table Visual (or Matrix for more control)
├─ Columns (in order):
│   ├─ DIM_CUSTOMER[CustomerName] - text, left-aligned
│   ├─ DIM_CUSTOMER[Segment] - text (colored badges)
│   ├─ DIM_CUSTOMER[Region] - text
│   ├─ [Total Revenue] - formatted as $#,##0
│   ├─ [Total Orders] - whole number
│   └─ [Last Order Date] - MM/DD/YYYY or "X days ago"
├─ Sorting:
│   ├─ Primary: [Total Revenue] descending
│   └─ Secondary: [Total Orders] descending
├─ Filter Applied: [Top 20 Customer Flag] = "Yes"
├─ Conditional Formatting:
│   ├─ Segment: Color-coded backgrounds
│   │   ├─ Loyal = Green background
│   │   ├─ Regular = Light green
│   │   ├─ New = Blue
│   │   └─ Dormant = Red
│   └─ Revenue: Data bars in background
├─ Row Count Display: "Showing 1-20 of top 20 customers"
└─ Paginated: Up to 20 rows visible (one screen)

Example Table:
┌──────────────────┬─────────┬────────┬──────────┬────────┬─────────────┐
│ Customer         │ Segment │ Region │ Revenue  │ Orders │ Last Order  │
├──────────────────┼─────────┼────────┼──────────┼────────┼─────────────┤
│ John Smith       │ Loyal   │ North  │ $18,456  │  47    │ 2 days ago  │
│ Sarah Johnson    │ Loyal   │ East   │ $16,789  │  42    │ 1 week ago  │
│ Mike Davis       │ Regular │ South  │ $14,234  │  28    │ 3 days ago  │
│ Jennifer Lee     │ Loyal   │ North  │ $13,567  │  35    │ Today       │
│ Robert Martinez  │ Loyal   │ West   │ $12,890  │  31    │ 5 days ago  │
│ ...              │ ...     │ ...    │ ...      │ ...    │ ...         │
└──────────────────┴─────────┴────────┴──────────┴────────┴─────────────┘
```

---

## Page 4: Geographic & Delivery Analysis

### Full Page Layout

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║  GEOGRAPHIC & OPERATIONAL PERFORMANCE                                              ║
║  Filter by: [Country ▼] [Delivery Status ▼] [Date Range ▼]                        ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                     ║
║                                                                                     ║
║   GEO MAP: Revenue & Order Distribution by Region                                  ║
║                                                                                     ║
║         ┌────────────────────────────────────┐                                     ║
║         │ USA (Bubble size = $456K revenue)  │                                     ║
║         │  ◉ New York     (Bubble: $123K)    │                                     ║
║         │  ◉ California   (Bubble: $145K)    │                                     ║
║         │  ◉ Texas        (Bubble: $89K)     │                                     ║
║         │  ◉ Florida      (Bubble: $99K)     │                                     ║
║         │ Canada (Bubble: $234K)             │                                     ║
║         │ Mexico (Bubble: $178K)             │                                     ║
║         │ [Map legend shows bubble intensity]│                                     ║
║         │ Tooltip: Region, Revenue, Orders   │                                     ║
║         └────────────────────────────────────┘                                     ║
║                                                                                     ║
├─────────────────────────────────────────────────────────────────────────────────────┤
║                                                                                     ║
║  Regional Performance Table        │  Delivery Status Distribution                ║
║  ┌────────────────────────────────┐│  ┌──────────────────────────────┐           ║
║  │ Region  │Revenue│ Orders │Cust ││  │ On-Time      68%  ████████░ │           ║
║  │─────────┼───────┼────────┼─────││  │ Late         22%  ██████░░░ │           ║
║  │ North   │$456K  │ 2,345  │ 789 ││  │ Exception     8%  █░░░░░░░░ │           ║
║  │ South   │$398K  │ 2,034  │ 654 ││  │ Cancelled     2%  ░░░░░░░░░ │           ║
║  │ East    │$345K  │ 1,789  │ 567 ││  │                              │           ║
║  │ West    │$289K  │ 1,456  │ 478 ││  │ Goal: 95% On-Time (at 68%)   │           ║
║  │ Central │$267K  │ 1,323  │ 434 ││  │ (Opportunity: Improve ops)   │           ║
║  │─────────┼───────┼────────┼─────││  │                              │           ║
║  │ TOTAL   │$1.76M │ 8,947  │ 2,922│ │ Click to filter details      │           ║
║  │         │ $187  │per ord │ avg  │ │ by delivery status           │           ║
║  └────────────────────────────────┘│  └──────────────────────────────┘           ║
║                                                                                     ║
║  Sort by: Revenue (↑ or ↓)                                                         ║
║  Drill-down: Click region → Expand to City level                                   ║
║  [+ indicators show when expandable]                                               ║
║                                                                                     ║
╚════════════════════════════════════════════════════════════════════════════════════╝
```

### Chart Specifications

#### Geographic Revenue Map

```
Chart Type: ArcGIS Maps or Filled Map
├─ Location Fields:
│   ├─ DIM_REGION[Country] (primary)
│   └─ DIM_REGION[City] (secondary, for drill-down)
├─ Bubble Size: [Total Revenue]
│   ├─ Min bubble: $50K (smallest city)
│   └─ Max bubble: $200K (largest city)
├─ Bubble Color: [Total Orders] (intensity)
│   ├─ Light color = Fewer orders
│   └─ Dark color = More orders
├─ Tooltip:
│   ├─ Location (City, Country)
│   ├─ Revenue amount & % of total
│   ├─ Order count
│   └─ Active customers
├─ Interactions:
│   ├─ Zoom in/out: Enabled
│   ├─ Click location: Filter other charts to that region
│   └─ Hover: Show tooltip
├─ Color Scheme: Blue tone (light=low, dark=high activity)
└─ Legend: Show bubble size scale + color intensity

Data Source: FACT_ORDERS
Dimensions: DIM_REGION[Country], DIM_REGION[City]
Measures: [Total Revenue], [Total Orders]

Example Interpretation:
- Large dark bubble = High-value market with many orders
- Small light bubble = Emerging/new market
- Growth opportunity = Cities with orders but lower revenue
```

#### Regional Performance Table

```
Chart Type: Matrix (with drill-down enabled)
├─ Rows:
│   ├─ Level 1: Country (expandable +)
│   ├─ Level 2: State/Province
│   └─ Level 3: City (optional)
├─ Values (Columns):
│   ├─ [Total Revenue] - formatted $#,##0, data bars
│   ├─ [Total Orders] - whole number
│   ├─ [Active Customers] - whole number
│   ├─ [Avg Order Value] - $#,##0.00
│   └─ [Return Rate %] - 0.00%
├─ Sorting: By Revenue descending
├─ Subtotals:
│   ├─ Country subtotal: Show
│   ├─ Grand total: Show at bottom
│   └─ Bold formatting for subtotal rows
├─ Conditional Formatting:
│   ├─ Revenue: Green data bars
│   └─ Return Rate: Red for high values
└─ Interaction: Click + to expand region details

Example Structure:
┌─ USA                          $1,234,567   6,345  2,123  $194.55   3.2%
│  ├─ California                 $456,789   2,345    789   $194.90   2.8%
│  │  ├─ Los Angeles             $234,567   1,234    412   $190.12   2.5%
│  │  ├─ San Francisco           $156,234     834    254   $187.25   3.1%
│  │  └─ San Diego                $65,988     277    123   $238.23   3.2%
│  ├─ Texas                      $398,234   2,034    678   $195.80   3.5%
│  └─ New York                   $289,756   1,256    412   $230.65   2.9%
├─ Canada                        $234,567   1,456    456   $161.06   4.2%
│  ├─ Ontario                    $143,567     876    276   $163.77   3.9%
│  └─ British Columbia            $91,000     580    180   $156.90   4.8%
└─ TOTAL                       $1,469,134   7,801  2,579  $188.28   3.5%
```

#### Delivery Status Distribution

```
Chart Type: Pie or Donut Chart
├─ Legend Fields: DIM_DELIVERY[DeliveryStatus]
│   ├─ On-Time       (68%, 5,349 orders)
│   ├─ Late          (22%, 1,726 orders)
│   ├─ Exception      (8%, 628 orders)
│   └─ Cancelled      (2%, 157 orders)
├─ Values: Count of orders per status
├─ Colors:
│   ├─ On-Time = Green (good)
│   ├─ Late = Orange (warning)
│   ├─ Exception = Red (problem)
│   └─ Cancelled = Gray
├─ Data Labels: Show status + percentage + order count
├─ Tooltip:
│   ├─ Status name
│   ├─ Order count
│   ├─ % of total
│   └─ Revenue impact (lost for cancelled)
└─ Context: Show goal (95% on-time target)
   Add comparison line: "Goal 95% (Current 68%)"

Alternative: Clustered Bar by Region
├─ Y-axis: DIM_REGION[Region]
├─ X-axis: Order count
├─ Multiple bars per region: On-Time, Late, Exception
├─ Stacked bars show 100% composition
└─ Sorts by On-Time % (highest first = best regions)
```

---

## Color Palette Recommendations

### Primary Colors (Use Consistently)
```
Revenue/Success      = #2E7D32 (Forest Green)    RGB(46, 125, 50)
Warning/Caution      = #F57C00 (Orange)          RGB(245, 124, 0)
Error/Risk           = #C62828 (Dark Red)        RGB(198, 40, 40)
Neutral/Info         = #1976D2 (Royal Blue)      RGB(25, 118, 210)
Background/Light     = #F5F5F5 (Light Gray)      RGB(245, 245, 245)
Text/Dark            = #212121 (Very Dark Gray)  RGB(33, 33, 33)
```

### Segment Specific Colors
```
Loyal Customers       = #2E7D32 (Dark Green)
Regular Customers     = #66BB6A (Light Green)
New Customers         = #1976D2 (Royal Blue)
Dormant Customers     = #C62828 (Dark Red)
```

### Channel Specific Colors
```
Online                = #007AFF (Bright Blue)
Retail                = #34C759 (Green)
Mobile                = #FF9500 (Orange)
Wholesale             = #8E8E93 (Gray)
```

---

## Font & Size Standards

```
Page Title            = 24pt Bold, Dark Gray
Section Title         = 18pt Bold, Dark Gray
Visual Title          = 16pt Bold, Dark Gray
Legend/Labels         = 11pt Regular, Dark Gray
Tooltip Text          = 11pt Regular, Dark Gray
Data Values in Chart  = 10pt Regular, Dark Gray
Table Header          = 12pt Bold, White on Dark Background
Table Data            = 11pt Regular, Dark Gray
KPI Value             = 32pt Bold, Dark Gray
KPI Subtitle          = 12pt Regular, Light Gray
```

---

## Summary: What to Build First

**Week 1 Priority Order:**
1. ✓ Page 1 (Executive Overview) - Simplest, shows value immediately
2. ✓ Page 2 (Products) - Adds depth, product team understands quickly
3. ✓ Page 3 (Customers) - More complex, add week 2
4. ✓ Page 4 (Geography) - Optional, add week 3

**Quick Win**: Start with KPI cards + Revenue Trend on Page 1. This takes 30 minutes and shows immediate ROI.

