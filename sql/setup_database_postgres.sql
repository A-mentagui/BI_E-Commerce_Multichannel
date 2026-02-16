-- ============================================================================
-- E-COMMERCE BI PROJECT - DATABASE SETUP (PostgreSQL)
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS public;
SET search_path TO public;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS dim_time (
    timekey INT PRIMARY KEY,
    fulldate DATE UNIQUE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    monthname VARCHAR(20),
    dayofmonth INT,
    dayofweek INT,
    dayname VARCHAR(20),
    weekofyear INT,
    season VARCHAR(20),
    isweekend BOOLEAN,
    isholiday BOOLEAN,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_product (
    productkey SERIAL PRIMARY KEY,
    productid VARCHAR(20) UNIQUE NOT NULL,
    productname VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    price NUMERIC(10,2),
    supplier VARCHAR(255),
    stock INT DEFAULT 0,
    createddate DATE,
    lastmodifieddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_product_category ON dim_product(category);
CREATE INDEX IF NOT EXISTS idx_product_supplier ON dim_product(supplier);

CREATE TABLE IF NOT EXISTS dim_channel (
    channelkey SERIAL PRIMARY KEY,
    channelid VARCHAR(10) UNIQUE NOT NULL,
    channelname VARCHAR(100) NOT NULL,
    channeltype VARCHAR(50),
    description VARCHAR(255),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customerkey SERIAL PRIMARY KEY,
    customerid VARCHAR(20) UNIQUE NOT NULL,
    customername VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    segment VARCHAR(50),
    registrationdate DATE,
    country VARCHAR(100),
    city VARCHAR(100),
    postalcode VARCHAR(20),
    lastpurchasedate DATE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_customer_segment ON dim_customer(segment);
CREATE INDEX IF NOT EXISTS idx_customer_registration ON dim_customer(registrationdate);

CREATE TABLE IF NOT EXISTS dim_region (
    regionkey SERIAL PRIMARY KEY,
    regionid VARCHAR(10) UNIQUE NOT NULL,
    regionname VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    population BIGINT,
    urbanrate NUMERIC(5,2),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_delivery (
    deliverykey SERIAL PRIMARY KEY,
    deliveryid VARCHAR(20),
    deliverymethod VARCHAR(100) NOT NULL,
    deliverytimedays INT,
    cost NUMERIC(10,2),
    reliability NUMERIC(5,2),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FACT TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS fact_orders (
    orderkey SERIAL PRIMARY KEY,
    orderid VARCHAR(20) UNIQUE NOT NULL,
    timekey INT NOT NULL REFERENCES dim_time(timekey),
    productkey INT NOT NULL REFERENCES dim_product(productkey),
    channelkey INT NOT NULL REFERENCES dim_channel(channelkey),
    customerkey INT NOT NULL REFERENCES dim_customer(customerkey),
    regionkey INT NOT NULL REFERENCES dim_region(regionkey),
    deliverykey INT NOT NULL REFERENCES dim_delivery(deliverykey),
    revenue NUMERIC(10,2) NOT NULL,
    quantity INT NOT NULL,
    unitprice NUMERIC(10,2),
    discount NUMERIC(10,2) DEFAULT 0,
    orderstatus VARCHAR(50),
    orderdate DATE NOT NULL,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_order_timekey ON fact_orders(timekey);
CREATE INDEX IF NOT EXISTS idx_order_productkey ON fact_orders(productkey);
CREATE INDEX IF NOT EXISTS idx_order_channelkey ON fact_orders(channelkey);
CREATE INDEX IF NOT EXISTS idx_order_customerkey ON fact_orders(customerkey);
CREATE INDEX IF NOT EXISTS idx_order_regionkey ON fact_orders(regionkey);
CREATE INDEX IF NOT EXISTS idx_order_orderdate ON fact_orders(orderdate);

CREATE TABLE IF NOT EXISTS fact_returns (
    returnkey SERIAL PRIMARY KEY,
    returnid VARCHAR(20) UNIQUE NOT NULL,
    orderkey INT NOT NULL REFERENCES fact_orders(orderkey),
    returndate DATE NOT NULL,
    returnreason VARCHAR(255),
    refundamount NUMERIC(10,2),
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_return_orderkey ON fact_returns(orderkey);
CREATE INDEX IF NOT EXISTS idx_return_date ON fact_returns(returndate);

CREATE TABLE IF NOT EXISTS fact_feedback (
    feedbackkey SERIAL PRIMARY KEY,
    feedbackid VARCHAR(20) UNIQUE NOT NULL,
    orderkey INT NOT NULL REFERENCES fact_orders(orderkey),
    satisfaction INT,
    comment TEXT,
    feedbackdate DATE,
    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_feedback_orderkey ON fact_feedback(orderkey);
CREATE INDEX IF NOT EXISTS idx_feedback_satisfaction ON fact_feedback(satisfaction);

-- ============================================================================
-- VIEWS FOR ANALYSIS
-- ============================================================================

CREATE OR REPLACE VIEW vw_fact_orders_olap AS
SELECT
    f.orderkey,
    f.orderid,
    f.timekey,
    f.productkey,
    f.channelkey,
    f.customerkey,
    f.regionkey,
    f.deliverykey,
    f.revenue,
    f.quantity,
    f.unitprice,
    f.discount,
    COALESCE(r.returncount, 0) AS return_count,
    COALESCE(r.refundamount, 0) AS refund_amount,
    COALESCE(fb.feedbackcount, 0) AS feedback_count,
    COALESCE(fb.satisfactiontotal, 0) AS satisfaction_sum,
    f.orderdate,
    f.createdat
FROM fact_orders f
LEFT JOIN (
    SELECT orderkey, COUNT(*) AS returncount, SUM(COALESCE(refundamount, 0)) AS refundamount
    FROM fact_returns
    GROUP BY orderkey
) r ON f.orderkey = r.orderkey
LEFT JOIN (
    SELECT orderkey, COUNT(*) AS feedbackcount, SUM(COALESCE(satisfaction, 0)) AS satisfactiontotal
    FROM fact_feedback
    GROUP BY orderkey
) fb ON f.orderkey = fb.orderkey;

-- ============================================================================
-- INITIALIZATION - Populate DIM_TIME (2022-2024)
-- ============================================================================

INSERT INTO dim_time (
  timekey, fulldate, year, quarter, month, monthname,
  dayofmonth, dayofweek, dayname, weekofyear, season,
  isweekend, isholiday
)
SELECT
  (EXTRACT(YEAR FROM d)::INT * 10000) + (EXTRACT(MONTH FROM d)::INT * 100) + EXTRACT(DAY FROM d)::INT AS timekey,
  d::DATE,
  EXTRACT(YEAR FROM d)::INT,
  EXTRACT(QUARTER FROM d)::INT,
  EXTRACT(MONTH FROM d)::INT,
  TO_CHAR(d, 'FMMonth')::VARCHAR(20),
  EXTRACT(DAY FROM d)::INT,
  EXTRACT(ISODOW FROM d)::INT,
  TO_CHAR(d, 'FMDay')::VARCHAR(20),
  EXTRACT(WEEK FROM d)::INT,
  CASE
    WHEN EXTRACT(MONTH FROM d)::INT IN (12, 1, 2) THEN 'Hiver'
    WHEN EXTRACT(MONTH FROM d)::INT IN (3, 4, 5) THEN 'Printemps'
    WHEN EXTRACT(MONTH FROM d)::INT IN (6, 7, 8) THEN 'Été'
    ELSE 'Automne'
  END,
  EXTRACT(ISODOW FROM d)::INT IN (6, 7),
  FALSE
FROM generate_series('2022-01-01'::date, '2024-12-31'::date, '1 day'::interval) d
ON CONFLICT (timekey) DO NOTHING;
