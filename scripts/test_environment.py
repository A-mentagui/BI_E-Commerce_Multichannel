"""
Validate runtime environment for BI + Pentaho ETL pipeline.
"""

from __future__ import annotations

import importlib
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def check_path(path: Path, label: str) -> bool:
    if path.exists():
        print(f"[OK] {label}: {path}")
        return True
    print(f"[ERROR] Missing {label}: {path}")
    return False


def check_package(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        print(f"[OK] Package available: {module_name}")
        return True
    except Exception:
        print(f"[ERROR] Package missing: {module_name}")
        return False


def main() -> int:
    print("=" * 60)
    print("BI ENVIRONMENT VALIDATION")
    print("=" * 60)

    ok = True

    print(f"[INFO] Python: {sys.version.split()[0]} ({platform.system()})")
    if sys.version_info < (3, 9):
        print("[ERROR] Python 3.9+ required")
        ok = False

    print("\n[INFO] Checking required folders/files...")
    ok &= check_path(ROOT / "scripts" / "generate_data.py", "data generator")
    ok &= check_path(ROOT / "sql" / "setup_database.sql", "SQL schema")
    ok &= check_path(ROOT / "etl" / "Master_Job.kjb", "Pentaho master job")
    ok &= check_path(ROOT / "etl" / "transformations", "Pentaho transformations folder")
    ok &= check_path(ROOT / "olap" / "ecommerce_catalog.xml", "Mondrian schema")

    print("\n[INFO] Checking Python packages...")
    for module in [
        "pandas",
        "numpy",
        "faker",
        "matplotlib",
        "seaborn",
        "sklearn",
    ]:
        ok &= check_package(module)

    print("\n[INFO] Checking optional DB connectors...")
    mysql_ok = check_package("mysql.connector")
    pg_ok = check_package("psycopg2")
    if not (mysql_ok or pg_ok):
        print("[ERROR] Install at least one DB connector: mysql-connector-python or psycopg2-binary")
        ok = False

    env_file = ROOT / ".env"
    env_example = ROOT / ".env.example"
    print("\n[INFO] Checking environment files...")
    if env_file.exists():
        print(f"[OK] .env found: {env_file}")
    elif env_example.exists():
        print(f"[WARN] .env not found, use template: {env_example}")
    else:
        print("[ERROR] No .env or .env.example found")
        ok = False

    print("\n" + "=" * 60)
    if ok:
        print("[OK] Environment is ready")
        return 0

    print("[ERROR] Environment check failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
