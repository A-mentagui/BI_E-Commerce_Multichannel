-- =============================================
-- Pentaho Report Designer - Data Sources
-- =============================================

-- ---------------------------------------------------------
-- Query 1: Executive KPIs (Top of Report)
-- Use in "Header" or "Summary" band
-- ---------------------------------------------------------
SELECT 
    SUM(f.Revenue) as TotalRevenue,
    COUNT(DISTINCT f.OrderID) as TotalOrders,
    AVG(f.Revenue) as AvgTicket,
    (SELECT COUNT(*) FROM FACT_RETURNS) / COUNT(DISTINCT f.OrderID) * 100 as ReturnRatePct
FROM vw_fact_orders_olap f
WHERE f.OrderDate BETWEEN ${StartDate} AND ${EndDate};

-- ---------------------------------------------------------
-- Query 2: Revenue Trend (Line Chart)
-- ---------------------------------------------------------
SELECT 
    CONCAT(t.Year, '-', t.Month) as Period,
    SUM(f.Revenue) as Revenue
FROM vw_fact_orders_olap f
JOIN DIM_TIME t ON f.TimeKey = t.TimeKey
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;

-- ---------------------------------------------------------
-- Query 3: Top 10 Products (Bar Chart / Table)
-- ---------------------------------------------------------
SELECT 
    p.ProductName,
    p.Category,
    SUM(f.Revenue) as Revenue
FROM vw_fact_orders_olap f
JOIN DIM_PRODUCT p ON f.ProductKey = p.ProductKey
WHERE f.OrderDate BETWEEN ${StartDate} AND ${EndDate}
GROUP BY p.ProductName, p.Category
ORDER BY Revenue DESC
LIMIT 10;

-- ---------------------------------------------------------
-- Query 4: Customer Segmentation (Pie Chart data)
-- ---------------------------------------------------------
SELECT 
    c.Segment,
    COUNT(DISTINCT c.CustomerKey) as CustomerCount,
    SUM(f.Revenue) as RevenueContribution
FROM vw_fact_orders_olap f
JOIN DIM_CUSTOMER c ON f.CustomerKey = c.CustomerKey
GROUP BY c.Segment;

-- ---------------------------------------------------------
-- Query 5: Detailed Sales Table (Main Detail Band)
-- ---------------------------------------------------------
SELECT 
    f.OrderDate,
    p.ProductName,
    c.CustomerName,
    ch.ChannelName,
    r.RegionName,
    f.Revenue,
    f.Quantity
FROM vw_fact_orders_olap f
JOIN DIM_PRODUCT p ON f.ProductKey = p.ProductKey
JOIN DIM_CUSTOMER c ON f.CustomerKey = c.CustomerKey
JOIN DIM_CHANNEL ch ON f.ChannelKey = ch.ChannelKey
JOIN DIM_REGION r ON f.RegionKey = r.RegionKey
WHERE f.OrderDate BETWEEN ${StartDate} AND ${EndDate}
ORDER BY f.OrderDate DESC
LIMIT 200;
