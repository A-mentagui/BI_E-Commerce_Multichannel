# Full BI Project Report Specification

## Executive Summary

This document defines the structure, metrics, and data sources for the "E-commerce Performance 360" report. This specification applies across all visualization tools (Pentaho Report Designer, Power BI, Saiku).

## 1. Report Pages / tabs

### Page 1: Executive Overview

**Goal**: High-level KPI monitoring for C-level executives.
**Visuals**:

1.  **KPI Cards**:
    - Total Revenue (Current Month vs Last Month)
    - Total Orders
    - Average Basket Size
    - Return Rate %
2.  **Revenue Trend**: Line chart (Last 12 months).
3.  **Channel Performance**: Donut chart (Revenue by Channel).

### Page 2: Product Performance

**Goal**: Inventory and sales analysis by category.
**Visuals**:

1.  **Top 10 Products**: Bar chart (Revenue).
2.  **Category Tree Map**: Revenue by Category > SubCategory.
3.  **Table**: Detailed product list with Sales, Qty, Margin, Return Rate.

### Page 3: Customer Insights

**Goal**: RFM Segmentation and Churn Risk.
**Visuals**:

1.  **Customer Distribution**: Pie chart (Loyal, Regular, New, Dormant).
2.  **Churn Risk Heatmap**: Region vs Churn Risk Score.
3.  **Top Spenders**: Table showing top 20 customers by CLV (Customer Lifetime Value).

### Page 4: Geographic Analysis

**Goal**: Performance by Region.
**Visuals**:

1.  **Map**: Sales by Country/City.
2.  **Regional performance**: Table with Revenue, Shipping Cost, Delivery Time.

---

## 2. Data Definitions (Common)

### Measures

| Metric | Calculation |
|BC|---|
| **Revenue** | `SUM(FACT_ORDERS.OrderAmount)` |
| **Orders** | `COUNT(DISTINCT FACT_ORDERS.OrderID)` |
| **Avg Basket** | `Revenue / Orders` |
| **Return Rate** | `COUNT(FACT_RETURNS) / Orders` |
| **Margin** | `(Revenue - Cost) / Revenue` (Estimated as 35% of Revenue for this project) |
| **CLV** | `SUM(Revenue) per Customer` across all time |

---

## 3. Implementation Guide

### A. Pentaho Report Designer (PRD)

**Format**: Paginated PDF Report.

- **Page 1**: Executive Summary (Grid layout).
- **Page 2**: Detailed tables with grouped headers by Category.
- **Files provided**: `visualization/prd/report_queries.sql`

### B. Power BI

**Format**: Interactive Dashboard.

- **Interaction**: Clicking a Month filters all charts. Drill-down enabled on Category.
- **Files provided**: `visualization/powerbi/DAX_Measures.dax`

### C. Saiku Analytics

**Format**: OLAP Pivot Tables (Crosstabs) + Charts.

- **Usage**: Ad-hoc analysis.
- **Files provided**: `visualization/saiku/executive_summary.saiku`
