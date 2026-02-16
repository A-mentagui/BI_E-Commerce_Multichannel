#!/usr/bin/env bash
set -euo pipefail

find_saiku_home() {
  local script_path
  script_path="$(find /opt/saiku -type f \( -name startup.sh -o -name start-saiku.sh \) | head -n 1 || true)"
  if [[ -z "${script_path}" ]]; then
    echo "Cannot locate Saiku startup script under /opt/saiku" >&2
    exit 1
  fi
  dirname "${script_path}"
}

find_classes_dir() {
  local base="$1"
  local classes
  classes="$(find "${base}" -type d -path '*/webapps/ROOT/WEB-INF/classes' | head -n 1 || true)"
  if [[ -z "${classes}" ]]; then
    echo "Cannot locate Saiku classes directory" >&2
    exit 1
  fi
  echo "${classes}"
}

find_lib_dir() {
  local base="$1"
  local lib
  lib="$(find "${base}" -type d -path '*/webapps/ROOT/WEB-INF/lib' | head -n 1 || true)"
  if [[ -z "${lib}" ]]; then
    echo "Cannot locate Saiku lib directory" >&2
    exit 1
  fi
  echo "${lib}"
}

SAIKU_HOME="$(find_saiku_home)"
CLASSES_DIR="$(find_classes_dir "${SAIKU_HOME}")"
LIB_DIR="$(find_lib_dir "${SAIKU_HOME}")"
DATASOURCE_DIR="${CLASSES_DIR}/saiku/repository/datasources"

mkdir -p "${DATASOURCE_DIR}"

DB_TYPE="${DB_TYPE:-mysql}"
DB_NAME="${DB_NAME:-ecommerce_bi}"
DB_USER="${DB_USER:-bi_user}"
DB_PASSWORD="${DB_PASSWORD:-bi_password}"
CATALOG_PATH="${CATALOG_PATH:-/workspace/olap/ecommerce_catalog.xml}"

if [[ "${DB_TYPE}" == "postgres" || "${DB_TYPE}" == "postgresql" ]]; then
  JDBC_DRIVER="org.postgresql.Driver"
  JDBC_PROTOCOL="postgresql"
  DB_HOST="${DB_HOST_POSTGRES:-postgres}"
  DB_PORT="${DB_PORT_POSTGRES:-5432}"
  MONDRIAN_PROPERTIES_SOURCE="/workspace/olap/mondrian-postgres.properties"
  if [[ -n "${POSTGRES_JDBC_URL:-}" ]]; then
    curl -fsSL "${POSTGRES_JDBC_URL}" -o "${LIB_DIR}/postgresql.jar"
  fi
else
  JDBC_DRIVER="com.mysql.cj.jdbc.Driver"
  JDBC_PROTOCOL="mysql"
  DB_HOST="${DB_HOST_MYSQL:-mysql}"
  DB_PORT="${DB_PORT_MYSQL:-3306}"
  MONDRIAN_PROPERTIES_SOURCE="/workspace/olap/mondrian.properties"
  if [[ -n "${MYSQL_JDBC_URL:-}" ]]; then
    curl -fsSL "${MYSQL_JDBC_URL}" -o "${LIB_DIR}/mysql-connector-j.jar"
  fi
fi

cat > "${DATASOURCE_DIR}/ecommerce_bi_olap.properties" <<EOF
type=OLAP
name=ecommerce_bi_olap
driver=mondrian.olap4j.MondrianOlap4jDriver
location=jdbc:mondrian:JdbcDrivers=${JDBC_DRIVER};Jdbc=jdbc:${JDBC_PROTOCOL}://${DB_HOST}:${DB_PORT}/${DB_NAME};JdbcUser=${DB_USER};JdbcPassword=${DB_PASSWORD};Catalog=${CATALOG_PATH};
username=admin
password=admin
security.enabled=false
EOF

if [[ -f "${MONDRIAN_PROPERTIES_SOURCE}" ]]; then
  cp "${MONDRIAN_PROPERTIES_SOURCE}" "${CLASSES_DIR}/mondrian.properties"
fi

if [[ -x "${SAIKU_HOME}/startup.sh" ]]; then
  "${SAIKU_HOME}/startup.sh"
elif [[ -x "${SAIKU_HOME}/start-saiku.sh" ]]; then
  "${SAIKU_HOME}/start-saiku.sh"
else
  echo "No executable startup script found in ${SAIKU_HOME}" >&2
  exit 1
fi

if [[ -f "${SAIKU_HOME}/tomcat/logs/catalina.out" ]]; then
  tail -F "${SAIKU_HOME}/tomcat/logs/catalina.out"
else
  tail -f /dev/null
fi
