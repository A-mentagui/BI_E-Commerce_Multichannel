-- ============================================================================
-- E-COMMERCE BI PROJECT - DATABASE SETUP
-- Creates dimensional model schema for multi-channel sales analysis
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS ecommerce_bi;
USE ecommerce_bi;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- DIM_TIME: Time dimension for temporal analysis
CREATE TABLE IF NOT EXISTS DIM_TIME (
    TimeKey INT PRIMARY KEY,
    FullDate DATE UNIQUE NOT NULL,
    Year INT,
    Quarter INT,
    Month INT,
    MonthName VARCHAR(20),
    DayOfMonth INT,
    DayOfWeek INT,
    DayName VARCHAR(20),
    WeekOfYear INT,
    Season VARCHAR(20),
    IsWeekend BOOLEAN,
    IsHoliday BOOLEAN,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_PRODUCT: Product dimension
CREATE TABLE IF NOT EXISTS DIM_PRODUCT (
    ProductKey INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20) UNIQUE NOT NULL,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    Price DECIMAL(10,2),
    Supplier VARCHAR(255),
    Stock INT DEFAULT 0,
    CreatedDate DATE,
    LastModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_category (Category),
    INDEX idx_product_supplier (Supplier)
);

-- DIM_CHANNEL: Sales channel dimension
CREATE TABLE IF NOT EXISTS DIM_CHANNEL (
    ChannelKey INT PRIMARY KEY AUTO_INCREMENT,
    ChannelID VARCHAR(10) UNIQUE NOT NULL,
    ChannelName VARCHAR(100) NOT NULL,
    ChannelType VARCHAR(50),  -- 'Digital' or 'Physical'
    Description VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_CUSTOMER: Customer dimension
CREATE TABLE IF NOT EXISTS DIM_CUSTOMER (
    CustomerKey INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID VARCHAR(20) UNIQUE NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Segment VARCHAR(50),  -- 'Nouveau', 'Régulier', 'Fidèle'
    RegistrationDate DATE,
    Country VARCHAR(100),
    City VARCHAR(100),
    PostalCode VARCHAR(20),
    LastPurchaseDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer_segment (Segment),
    INDEX idx_customer_registration (RegistrationDate)
);

-- DIM_REGION: Geographic region dimension
CREATE TABLE IF NOT EXISTS DIM_REGION (
    RegionKey INT PRIMARY KEY AUTO_INCREMENT,
    RegionID VARCHAR(10) UNIQUE NOT NULL,
    RegionName VARCHAR(100) NOT NULL,
    Country VARCHAR(100),
    Population BIGINT,
    UrbanRate DECIMAL(5,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_DELIVERY: Delivery method dimension
CREATE TABLE IF NOT EXISTS DIM_DELIVERY (
    DeliveryKey INT PRIMARY KEY AUTO_INCREMENT,
    DeliveryID VARCHAR(20),
    DeliveryMethod VARCHAR(100) NOT NULL,
    DeliveryTimeDays INT,
    Cost DECIMAL(10,2),
    Reliability DECIMAL(5,2),  -- Percentage of on-time deliveries
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FACT TABLES
-- ============================================================================

-- FACT_ORDERS: Main fact table for sales transactions
CREATE TABLE IF NOT EXISTS FACT_ORDERS (
    OrderKey INT PRIMARY KEY AUTO_INCREMENT,
    OrderID VARCHAR(20) UNIQUE NOT NULL,
    TimeKey INT NOT NULL,
    ProductKey INT NOT NULL,
    ChannelKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    RegionKey INT NOT NULL,
    DeliveryKey INT NOT NULL,
    
    -- Additive Measures
    Revenue DECIMAL(10,2) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2),
    Discount DECIMAL(10,2) DEFAULT 0,
    
    -- Status
    OrderStatus VARCHAR(50),
    
    OrderDate DATE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for query performance
    INDEX idx_order_timekey (TimeKey),
    INDEX idx_order_productkey (ProductKey),
    INDEX idx_order_channelkey (ChannelKey),
    INDEX idx_order_customerkey (CustomerKey),
    INDEX idx_order_regionkey (RegionKey),
    INDEX idx_order_orderdate (OrderDate),
    
    -- Foreign Keys
    FOREIGN KEY (TimeKey) REFERENCES DIM_TIME(TimeKey),
    FOREIGN KEY (ProductKey) REFERENCES DIM_PRODUCT(ProductKey),
    FOREIGN KEY (ChannelKey) REFERENCES DIM_CHANNEL(ChannelKey),
    FOREIGN KEY (CustomerKey) REFERENCES DIM_CUSTOMER(CustomerKey),
    FOREIGN KEY (RegionKey) REFERENCES DIM_REGION(RegionKey),
    FOREIGN KEY (DeliveryKey) REFERENCES DIM_DELIVERY(DeliveryKey)
);

-- FACT_RETURNS: Returns and refunds transactions
CREATE TABLE IF NOT EXISTS FACT_RETURNS (
    ReturnKey INT PRIMARY KEY AUTO_INCREMENT,
    ReturnID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INT NOT NULL,
    ReturnDate DATE NOT NULL,
    ReturnReason VARCHAR(255),
    RefundAmount DECIMAL(10,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_return_orderkey (OrderKey),
    INDEX idx_return_date (ReturnDate),
    
    FOREIGN KEY (OrderKey) REFERENCES FACT_ORDERS(OrderKey)
);

-- FACT_FEEDBACK: Customer satisfaction and feedback
CREATE TABLE IF NOT EXISTS FACT_FEEDBACK (
    FeedbackKey INT PRIMARY KEY AUTO_INCREMENT,
    FeedbackID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INT NOT NULL,
    Satisfaction INT,  -- 1-5 scale
    Comment TEXT,
    FeedbackDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_feedback_orderkey (OrderKey),
    INDEX idx_feedback_satisfaction (Satisfaction),
    
    FOREIGN KEY (OrderKey) REFERENCES FACT_ORDERS(OrderKey)
);

-- ============================================================================
-- VIEWS FOR ANALYSIS
-- ============================================================================

-- View: OLAP fact at order grain (pre-aggregates returns/feedback to avoid double counting)
CREATE OR REPLACE VIEW vw_fact_orders_olap AS
SELECT
    f.OrderKey,
    f.OrderID,
    f.TimeKey,
    f.ProductKey,
    f.ChannelKey,
    f.CustomerKey,
    f.RegionKey,
    f.DeliveryKey,
    f.Revenue,
    f.Quantity,
    f.UnitPrice,
    f.Discount,
    COALESCE(r.ReturnCount, 0) AS return_count,
    COALESCE(r.RefundAmount, 0) AS refund_amount,
    COALESCE(fb.FeedbackCount, 0) AS feedback_count,
    COALESCE(fb.SatisfactionTotal, 0) AS satisfaction_sum,
    f.OrderDate,
    f.CreatedAt
FROM FACT_ORDERS f
LEFT JOIN (
    SELECT
        OrderKey,
        COUNT(*) AS ReturnCount,
        SUM(COALESCE(RefundAmount, 0)) AS RefundAmount
    FROM FACT_RETURNS
    GROUP BY OrderKey
) r ON f.OrderKey = r.OrderKey
LEFT JOIN (
    SELECT
        OrderKey,
        COUNT(*) AS FeedbackCount,
        SUM(COALESCE(Satisfaction, 0)) AS SatisfactionTotal
    FROM FACT_FEEDBACK
    GROUP BY OrderKey
) fb ON f.OrderKey = fb.OrderKey;

-- View: Order Summary with Dimensions
CREATE OR REPLACE VIEW vw_orders_summary AS
SELECT 
    f.OrderID,
    f.OrderDate,
    c.CustomerName,
    c.Segment as CustomerSegment,
    ch.ChannelName,
    p.ProductName,
    p.Category,
    r.RegionName,
    f.Quantity,
    f.UnitPrice,
    f.Revenue,
    f.Discount,
    f.OrderStatus,
    d.DeliveryMethod
FROM FACT_ORDERS f
JOIN DIM_TIME t ON f.TimeKey = t.TimeKey
JOIN DIM_PRODUCT p ON f.ProductKey = p.ProductKey
JOIN DIM_CHANNEL ch ON f.ChannelKey = ch.ChannelKey
JOIN DIM_CUSTOMER c ON f.CustomerKey = c.CustomerKey
JOIN DIM_REGION r ON f.RegionKey = r.RegionKey
JOIN DIM_DELIVERY d ON f.DeliveryKey = d.DeliveryKey;

-- View: Revenue by Channel
CREATE OR REPLACE VIEW vw_revenue_by_channel AS
SELECT 
    ch.ChannelName,
    SUM(f.Revenue) as TotalRevenue,
    SUM(f.Quantity) as TotalQuantity,
    COUNT(f.OrderID) as OrderCount,
    AVG(f.Revenue) as AvgBasket,
    COUNT(ret.ReturnID) as ReturnCount,
    ROUND(COUNT(ret.ReturnID) / COUNT(f.OrderID) * 100, 2) as ReturnRatePercent
FROM FACT_ORDERS f
LEFT JOIN FACT_RETURNS ret ON f.OrderKey = ret.OrderKey
JOIN DIM_CHANNEL ch ON f.ChannelKey = ch.ChannelKey
GROUP BY ch.ChannelName;

-- View: Customer Segment Analysis
CREATE OR REPLACE VIEW vw_customer_segment_analysis AS
SELECT 
    c.Segment,
    COUNT(DISTINCT c.CustomerKey) as CustomerCount,
    SUM(f.Revenue) as TotalRevenue,
    AVG(f.Revenue) as AvgOrderValue,
    COUNT(f.OrderID) as TotalOrders,
    AVG(fb.Satisfaction) as AvgSatisfaction
FROM DIM_CUSTOMER c
LEFT JOIN FACT_ORDERS f ON c.CustomerKey = f.CustomerKey
LEFT JOIN FACT_FEEDBACK fb ON f.OrderKey = fb.OrderKey
GROUP BY c.Segment;

-- View: Regional Performance
CREATE OR REPLACE VIEW vw_regional_performance AS
SELECT 
    r.RegionName,
    COUNT(DISTINCT f.CustomerKey) as UniqueCustomers,
    SUM(f.Revenue) as TotalRevenue,
    COUNT(f.OrderID) as OrderCount,
    AVG(f.Revenue) as AvgBasket,
    ROUND(COUNT(ret.ReturnID) / COUNT(f.OrderID) * 100, 2) as ReturnRatePercent,
    AVG(fb.Satisfaction) as AvgSatisfaction
FROM FACT_ORDERS f
LEFT JOIN FACT_RETURNS ret ON f.OrderKey = ret.OrderKey
LEFT JOIN FACT_FEEDBACK fb ON f.OrderKey = fb.OrderKey
JOIN DIM_REGION r ON f.RegionKey = r.RegionKey
GROUP BY r.RegionName;

-- ============================================================================
-- STORED PROCEDURES
-- ============================================================================

-- Procedure to populate DIM_TIME from a date range
DELIMITER $$

CREATE PROCEDURE sp_populate_time_dimension(IN start_date DATE, IN end_date DATE)
BEGIN
    DECLARE current_date DATE;
    DECLARE time_key INT;
    
    SET current_date = start_date;
    
    WHILE current_date <= end_date DO
        SET time_key = YEAR(current_date) * 10000 + 
                       MONTH(current_date) * 100 + 
                       DAY(current_date);
        
        INSERT IGNORE INTO DIM_TIME (
            TimeKey, FullDate, Year, Quarter, Month, MonthName,
            DayOfMonth, DayOfWeek, DayName, WeekOfYear, Season,
            IsWeekend, IsHoliday
        ) VALUES (
            time_key,
            current_date,
            YEAR(current_date),
            QUARTER(current_date),
            MONTH(current_date),
            DATE_FORMAT(current_date, '%B'),
            DAY(current_date),
            DAYOFWEEK(current_date),
            DATE_FORMAT(current_date, '%W'),
            WEEK(current_date),
            CASE 
                WHEN MONTH(current_date) IN (12, 1, 2) THEN 'Hiver'
                WHEN MONTH(current_date) IN (3, 4, 5) THEN 'Printemps'
                WHEN MONTH(current_date) IN (6, 7, 8) THEN 'Été'
                ELSE 'Automne'
            END,
            DAYOFWEEK(current_date) IN (1, 7),
            FALSE
        );
        
        SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
    END WHILE;
END$$

DELIMITER ;

-- ============================================================================
-- GRANT PERMISSIONS (Optional, modify as needed)
-- ============================================================================

-- GRANT ALL PRIVILEGES ON ecommerce_bi.* TO 'bi_user'@'localhost' IDENTIFIED BY 'password';
-- FLUSH PRIVILEGES;

-- ============================================================================
-- INITIALIZATION
-- ============================================================================

-- Populate TIME dimension for 2022-2024
CALL sp_populate_time_dimension('2022-01-01', '2024-12-31');

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify dimensions created
SELECT 'DIM_TIME' AS TableName, COUNT(*) AS RowCount FROM DIM_TIME
UNION ALL
SELECT 'DIM_PRODUCT', COUNT(*) FROM DIM_PRODUCT
UNION ALL
SELECT 'DIM_CHANNEL', COUNT(*) FROM DIM_CHANNEL
UNION ALL
SELECT 'DIM_CUSTOMER', COUNT(*) FROM DIM_CUSTOMER
UNION ALL
SELECT 'DIM_REGION', COUNT(*) FROM DIM_REGION
UNION ALL
SELECT 'DIM_DELIVERY', COUNT(*) FROM DIM_DELIVERY;
