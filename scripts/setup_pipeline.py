"""
Setup BI database and ETL source data.
- Creates database if not exists
- Creates all DW tables required by Pentaho ETL
- Generates CSV source files if missing
- Supports MySQL or PostgreSQL
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"


def load_env(env_file: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not env_file.exists():
        return values
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def get_cfg(args: argparse.Namespace) -> Dict[str, str]:
    env_values = load_env(Path(args.env_file))
    cfg = {
        "db_type": (args.db_type or env_values.get("DB_TYPE") or "mysql").lower(),
        "host": args.host or env_values.get("DB_HOST", "localhost"),
        "port": str(args.port or env_values.get("DB_PORT", "3306")),
        "database": args.database or env_values.get("DB_NAME", "ecommerce_bi"),
        "user": args.user or env_values.get("DB_USER", "root"),
        "password": args.password or env_values.get("DB_PASSWORD", ""),
    }
    return cfg


def mysql_connect(host: str, port: int, user: str, password: str, database: str | None = None):
    import mysql.connector  # type: ignore

    kwargs = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
    }
    if database:
        kwargs["database"] = database
    return mysql.connector.connect(**kwargs)


def pg_connect(host: str, port: int, user: str, password: str, database: str):
    import psycopg2  # type: ignore

    return psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=database,
    )


def create_database(cfg: Dict[str, str]) -> None:
    db_type = cfg["db_type"]
    database = cfg["database"]

    if db_type == "mysql":
        conn = mysql_connect(cfg["host"], int(cfg["port"]), cfg["user"], cfg["password"])
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")
        cur.close()
        conn.close()
        return

    if db_type in {"postgres", "postgresql"}:
        conn = pg_connect(cfg["host"], int(cfg["port"]), cfg["user"], cfg["password"], "postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute(f'CREATE DATABASE "{database}"')
        cur.close()
        conn.close()
        return

    raise ValueError("Unsupported db_type. Use mysql or postgresql")


def mysql_schema_sql() -> str:
    return """
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
    LastModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_CHANNEL (
    ChannelKey INT PRIMARY KEY AUTO_INCREMENT,
    ChannelID VARCHAR(10) UNIQUE NOT NULL,
    ChannelName VARCHAR(100) NOT NULL,
    ChannelType VARCHAR(50),
    Description VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_CUSTOMER (
    CustomerKey INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID VARCHAR(20) UNIQUE NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Segment VARCHAR(50),
    RegistrationDate DATE,
    Country VARCHAR(100),
    City VARCHAR(100),
    PostalCode VARCHAR(20),
    LastPurchaseDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_REGION (
    RegionKey INT PRIMARY KEY AUTO_INCREMENT,
    RegionID VARCHAR(10) UNIQUE NOT NULL,
    RegionName VARCHAR(100) NOT NULL,
    Country VARCHAR(100),
    Population BIGINT,
    UrbanRate DECIMAL(5,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_DELIVERY (
    DeliveryKey INT PRIMARY KEY AUTO_INCREMENT,
    DeliveryID VARCHAR(20),
    DeliveryMethod VARCHAR(100) NOT NULL,
    DeliveryTimeDays INT,
    Cost DECIMAL(10,2),
    Reliability DECIMAL(5,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS FACT_ORDERS (
    OrderKey INT PRIMARY KEY AUTO_INCREMENT,
    OrderID VARCHAR(20) UNIQUE NOT NULL,
    TimeKey INT NOT NULL,
    ProductKey INT NOT NULL,
    ChannelKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    RegionKey INT NOT NULL,
    DeliveryKey INT NOT NULL,
    Revenue DECIMAL(10,2) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2),
    Discount DECIMAL(10,2) DEFAULT 0,
    OrderStatus VARCHAR(50),
    OrderDate DATE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (TimeKey) REFERENCES DIM_TIME(TimeKey),
    FOREIGN KEY (ProductKey) REFERENCES DIM_PRODUCT(ProductKey),
    FOREIGN KEY (ChannelKey) REFERENCES DIM_CHANNEL(ChannelKey),
    FOREIGN KEY (CustomerKey) REFERENCES DIM_CUSTOMER(CustomerKey),
    FOREIGN KEY (RegionKey) REFERENCES DIM_REGION(RegionKey),
    FOREIGN KEY (DeliveryKey) REFERENCES DIM_DELIVERY(DeliveryKey)
);

CREATE TABLE IF NOT EXISTS FACT_RETURNS (
    ReturnKey INT PRIMARY KEY AUTO_INCREMENT,
    ReturnID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INT NOT NULL,
    ReturnDate DATE NOT NULL,
    ReturnReason VARCHAR(255),
    RefundAmount DECIMAL(10,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OrderKey) REFERENCES FACT_ORDERS(OrderKey)
);

CREATE TABLE IF NOT EXISTS FACT_FEEDBACK (
    FeedbackKey INT PRIMARY KEY AUTO_INCREMENT,
    FeedbackID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INT NOT NULL,
    Satisfaction INT,
    Comment TEXT,
    FeedbackDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OrderKey) REFERENCES FACT_ORDERS(OrderKey)
);
""".strip()


def postgres_schema_sql() -> str:
    return """
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

CREATE TABLE IF NOT EXISTS DIM_PRODUCT (
    ProductKey SERIAL PRIMARY KEY,
    ProductID VARCHAR(20) UNIQUE NOT NULL,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    Price NUMERIC(10,2),
    Supplier VARCHAR(255),
    Stock INT DEFAULT 0,
    CreatedDate DATE,
    LastModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_CHANNEL (
    ChannelKey SERIAL PRIMARY KEY,
    ChannelID VARCHAR(10) UNIQUE NOT NULL,
    ChannelName VARCHAR(100) NOT NULL,
    ChannelType VARCHAR(50),
    Description VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_CUSTOMER (
    CustomerKey SERIAL PRIMARY KEY,
    CustomerID VARCHAR(20) UNIQUE NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Segment VARCHAR(50),
    RegistrationDate DATE,
    Country VARCHAR(100),
    City VARCHAR(100),
    PostalCode VARCHAR(20),
    LastPurchaseDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_REGION (
    RegionKey SERIAL PRIMARY KEY,
    RegionID VARCHAR(10) UNIQUE NOT NULL,
    RegionName VARCHAR(100) NOT NULL,
    Country VARCHAR(100),
    Population BIGINT,
    UrbanRate NUMERIC(5,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS DIM_DELIVERY (
    DeliveryKey SERIAL PRIMARY KEY,
    DeliveryID VARCHAR(20),
    DeliveryMethod VARCHAR(100) NOT NULL,
    DeliveryTimeDays INT,
    Cost NUMERIC(10,2),
    Reliability NUMERIC(5,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS FACT_ORDERS (
    OrderKey SERIAL PRIMARY KEY,
    OrderID VARCHAR(20) UNIQUE NOT NULL,
    TimeKey INT NOT NULL REFERENCES DIM_TIME(TimeKey),
    ProductKey INT NOT NULL REFERENCES DIM_PRODUCT(ProductKey),
    ChannelKey INT NOT NULL REFERENCES DIM_CHANNEL(ChannelKey),
    CustomerKey INT NOT NULL REFERENCES DIM_CUSTOMER(CustomerKey),
    RegionKey INT NOT NULL REFERENCES DIM_REGION(RegionKey),
    DeliveryKey INT NOT NULL REFERENCES DIM_DELIVERY(DeliveryKey),
    Revenue NUMERIC(10,2) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice NUMERIC(10,2),
    Discount NUMERIC(10,2) DEFAULT 0,
    OrderStatus VARCHAR(50),
    OrderDate DATE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS FACT_RETURNS (
    ReturnKey SERIAL PRIMARY KEY,
    ReturnID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INT NOT NULL REFERENCES FACT_ORDERS(OrderKey),
    ReturnDate DATE NOT NULL,
    ReturnReason VARCHAR(255),
    RefundAmount NUMERIC(10,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS FACT_FEEDBACK (
    FeedbackKey SERIAL PRIMARY KEY,
    FeedbackID VARCHAR(20) UNIQUE NOT NULL,
    OrderKey INT NOT NULL REFERENCES FACT_ORDERS(OrderKey),
    Satisfaction INT,
    Comment TEXT,
    FeedbackDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""".strip()


def split_statements(sql_text: str):
    return [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]


def create_schema(cfg: Dict[str, str]) -> None:
    db_type = cfg["db_type"]

    if db_type == "mysql":
        conn = mysql_connect(
            cfg["host"], int(cfg["port"]), cfg["user"], cfg["password"], cfg["database"]
        )
        conn.autocommit = True
        cur = conn.cursor()
        for stmt in split_statements(mysql_schema_sql()):
            cur.execute(stmt)
        cur.close()
        conn.close()
        return

    if db_type in {"postgres", "postgresql"}:
        conn = pg_connect(cfg["host"], int(cfg["port"]), cfg["user"], cfg["password"], cfg["database"])
        conn.autocommit = True
        cur = conn.cursor()
        for stmt in split_statements(postgres_schema_sql()):
            cur.execute(stmt)
        cur.close()
        conn.close()
        return

    raise ValueError("Unsupported db_type. Use mysql or postgresql")


def generate_source_data(force: bool = False) -> None:
    required = [
        "customers.csv",
        "products.csv",
        "channels.csv",
        "regions.csv",
        "orders.csv",
        "returns.csv",
        "feedback.csv",
    ]
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    missing = [name for name in required if not (DATA_RAW / name).exists()]
    if missing or force:
        print("[INFO] Generating synthetic source CSV files for Pentaho ETL...")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_data.py")], check=True)
    else:
        print("[INFO] Source CSV files already exist. Skipping generation.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize BI database and ETL source data")
    parser.add_argument("--env-file", default=str(ROOT / ".env"), help="Path to .env file")
    parser.add_argument("--db-type", choices=["mysql", "postgresql"], help="Database type")
    parser.add_argument("--host", help="Database host")
    parser.add_argument("--port", type=int, help="Database port")
    parser.add_argument("--database", help="Database name")
    parser.add_argument("--user", help="Database user")
    parser.add_argument("--password", help="Database password")
    parser.add_argument("--skip-data", action="store_true", help="Skip CSV generation")
    parser.add_argument("--force-data", action="store_true", help="Force regenerate CSV files")
    args = parser.parse_args()

    try:
        cfg = get_cfg(args)
        print(f"[INFO] Target database: {cfg['db_type']}://{cfg['host']}:{cfg['port']}/{cfg['database']}")

        if not args.skip_data:
            generate_source_data(force=args.force_data)

        print("[INFO] Creating database if not exists...")
        create_database(cfg)

        print("[INFO] Creating schema/tables for Pentaho ETL targets...")
        create_schema(cfg)

        print("[OK] Setup complete.")
        print("[NEXT] Run Pentaho master job: etl/Master_Job.kjb")
        return 0
    except Exception as exc:
        print(f"[ERROR] Setup failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
