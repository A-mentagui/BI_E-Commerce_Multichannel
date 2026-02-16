"""
Test database connection for MySQL or PostgreSQL.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict


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
    root = Path(__file__).resolve().parents[1]
    env_values = load_env(Path(args.env_file or (root / ".env")))
    return {
        "db_type": (args.db_type or env_values.get("DB_TYPE") or "mysql").lower(),
        "host": args.host or env_values.get("DB_HOST", "localhost"),
        "port": str(args.port or env_values.get("DB_PORT", "3306")),
        "database": args.database or env_values.get("DB_NAME", "ecommerce_bi"),
        "user": args.user or env_values.get("DB_USER", "root"),
        "password": args.password or env_values.get("DB_PASSWORD", ""),
    }


def test_mysql(cfg: Dict[str, str]) -> None:
    import mysql.connector  # type: ignore

    conn = mysql.connector.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
    )
    cur = conn.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"[OK] MySQL connection successful. Server version: {version}")


def test_postgres(cfg: Dict[str, str]) -> None:
    import psycopg2  # type: ignore

    conn = psycopg2.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        user=cfg["user"],
        password=cfg["password"],
        dbname=cfg["database"],
    )
    cur = conn.cursor()
    cur.execute("SELECT version()")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"[OK] PostgreSQL connection successful. Server version: {version}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Test DB connection")
    parser.add_argument("--env-file", help="Path to .env file")
    parser.add_argument("--db-type", choices=["mysql", "postgresql"], help="Database type")
    parser.add_argument("--host", help="Database host")
    parser.add_argument("--port", type=int, help="Database port")
    parser.add_argument("--database", help="Database name")
    parser.add_argument("--user", help="Database user")
    parser.add_argument("--password", help="Database password")
    args = parser.parse_args()

    try:
        cfg = get_cfg(args)
        print(f"[INFO] Testing {cfg['db_type']}://{cfg['host']}:{cfg['port']}/{cfg['database']}")

        if cfg["db_type"] == "mysql":
            test_mysql(cfg)
        elif cfg["db_type"] in {"postgres", "postgresql"}:
            test_postgres(cfg)
        else:
            raise ValueError("Unsupported db_type. Use mysql or postgresql")

        return 0
    except Exception as exc:
        print(f"[ERROR] Connection test failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
