# BI E-Commerce Multichannel

End-to-end Business Intelligence project for multi-channel e-commerce analytics, covering data generation, warehouse modeling, ETL, OLAP, and data mining.

## Project at a Glance

- Synthetic data pipeline (`data/raw/`)
- Dimensional warehouse setup (`sql/setup_database.sql`)
- Pentaho ETL orchestration (`etl/Master_Job.kjb`)
- Mondrian OLAP model (`olap/ecommerce_catalog.xml`)
- Data mining scripts (`scripts/`)
- Analysis outputs (`results/`)

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Generate data:

```bash
python scripts/generate_data.py
```

3. Run data mining analyses:

```bash
python scripts/rfm_analysis.py
python scripts/churn_prediction.py
python scripts/association_rules.py
```

## Canonical Run Guide

Use the final complete guide for all execution methods (local/manual, Docker MySQL/PostgreSQL, Podman):

- `docs/FINAL_PROJECT_GUIDE.md`

## Documentation Map

- `docs/DOCUMENTATION_INDEX.md`
- `docs/ETL_DOCUMENTATION.md`
- `docs/MDX_QUERIES.md`
- `docs/DATA_MINING_GUIDE.md`
- `docs/DOCKER_FULL_ENVIRONMENT.md`

## Notes

- This repository is documentation-consolidated: root-level duplicate summary docs were removed to keep one authoritative runbook.
- For implementation history and architectural reference, see `docs/implementation/`.
