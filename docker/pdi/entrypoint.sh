#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"
KETTLE_HOME="${KETTLE_HOME:-/root/.kettle}"
PDI_HOME="${PDI_HOME:-/opt/pdi/data-integration}"

DB_TYPE="${DB_TYPE:-mysql}"
DB_NAME="${DB_NAME:-ecommerce_bi}"
DB_USER="${DB_USER:-bi_user}"
DB_PASSWORD="${DB_PASSWORD:-bi_password}"
DB_SCHEMA="${DB_SCHEMA:-public}"

if [[ "${DB_TYPE}" == "postgres" || "${DB_TYPE}" == "postgresql" ]]; then
  DB_CONN_TYPE="POSTGRESQL"
  DB_HOST="${DB_HOST_POSTGRES:-postgres}"
  DB_PORT="${DB_PORT_POSTGRES:-5432}"
else
  DB_CONN_TYPE="MYSQL"
  DB_HOST="${DB_HOST_MYSQL:-mysql}"
  DB_PORT="${DB_PORT_MYSQL:-3306}"
fi

mkdir -p "${KETTLE_HOME}"

cat > "${KETTLE_HOME}/shared.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<sharedobjects>
  <connection>
    <name>BI</name>
    <server>${DB_HOST}</server>
    <type>${DB_CONN_TYPE}</type>
    <access>Native</access>
    <database>${DB_NAME}</database>
    <port>${DB_PORT}</port>
    <username>${DB_USER}</username>
    <password>${DB_PASSWORD}</password>
    <servername/>
    <data_tablespace/>
    <index_tablespace/>
    <attributes>
      <attribute><code>EXTRA_OPTION_MYSQL.useSSL</code><attribute>false</attribute></attribute>
      <attribute><code>EXTRA_OPTION_MYSQL.serverTimezone</code><attribute>UTC</attribute></attribute>
      <attribute><code>EXTRA_OPTION_POSTGRESQL.currentSchema</code><attribute>${DB_SCHEMA}</attribute></attribute>
    </attributes>
  </connection>
</sharedobjects>
EOF

if [[ "${1:-shell}" == "run-job" ]]; then
  JOB_FILE="${PDI_JOB_FILE:-${WORKSPACE_DIR}/etl/Master_Job.kjb}"
  shift || true
  exec "${PDI_HOME}/kitchen.sh" -file="${JOB_FILE}" "$@"
elif [[ "${1:-shell}" == "run-trans" ]]; then
  TRANS_FILE="${PDI_TRANS_FILE:-${WORKSPACE_DIR}/etl/transformations/ETL_1_Load_Customers.ktr}"
  shift || true
  exec "${PDI_HOME}/pan.sh" -file="${TRANS_FILE}" "$@"
elif [[ "${1:-shell}" == "shell" ]]; then
  exec bash
else
  exec "$@"
fi
