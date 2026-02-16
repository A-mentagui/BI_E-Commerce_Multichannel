# Full Container Environment (Pentaho + Saiku + Report Designer)

This project now includes a full containerized stack compatible with **Docker Compose** and **Podman Compose**.

## Included Tools

- **MySQL 8** (default profile) for warehouse storage
- **PostgreSQL 16** (optional profile) for alternative warehouse backend
- **Pentaho Data Integration (PDI / Kitchen/Pan)** for ETL execution
- **Saiku + Mondrian** for OLAP querying and dashboards
- **Pentaho Report Designer (PRD)** exposed via **noVNC** in browser

## Added Files

- `docker-compose.yml`
- `docker/pdi/Dockerfile`
- `docker/pdi/entrypoint.sh`
- `docker/saiku/Dockerfile`
- `docker/saiku/entrypoint.sh`
- `docker/prd/Dockerfile`
- `docker/prd/entrypoint.sh`
- `sql/setup_database_postgres.sql`
- `.env.container.example`

## Prerequisites

- Docker Engine + Docker Compose plugin **or** Podman + podman-compose
- Internet access for first build (downloads PDI, Saiku, PRD archives)
- Ports available: `3306`, `5432`, `8080`, `6080`, `5900`

## Quick Start (MySQL)

1. Copy env template:

```bash
cp .env.container.example .env.container
```

1. Export file in shell session:

```bash
set -a; source .env.container; set +a
```

1. Start stack (MySQL profile):

```bash
docker compose --profile mysql up -d --build
```

1. Open tools:

- Saiku: `http://localhost:8080`
- Report Designer (noVNC): `http://localhost:6080/vnc.html`

1. Run ETL once:

```bash
docker compose --profile etl run --rm pdi-runner
```

## Quick Start (PostgreSQL)

1. In `.env.container`, set:

```dotenv
STACK_DB_TYPE=postgresql
```

1. Start stack (PostgreSQL profile):

```bash
docker compose --profile postgres up -d --build
```

1. Run ETL once:

```bash
docker compose --profile etl run --rm pdi-runner
```

## Podman Usage

Use the same compose file and profiles:

```bash
podman compose --profile mysql up -d --build
podman compose --profile etl run --rm pdi-runner
```

For SELinux hosts, if bind mounts are denied, append `:Z` to local bind mounts in `docker-compose.yml`.

## Notes

- `etl/transformations/ETL_1_Load_Customers.ktr` was updated to use a relative CSV path for container portability.
- PDI creates a runtime `shared.xml` connection named `BI`, so existing `.ktr/.kjb` files can run without manual connection recreation.
- Saiku datasource is generated at startup from environment variables and points to `olap/ecommerce_catalog.xml`.
