FROM eclipse-temurin:11-jre-jammy

ARG SAIKU_VERSION=3.17
ARG SAIKU_DOWNLOAD_URL=https://downloads.sourceforge.net/project/saiku/saiku-server/saiku-server-${SAIKU_VERSION}.zip
ARG MYSQL_JDBC_URL=https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.4.0/mysql-connector-j-8.4.0.jar
ARG POSTGRES_JDBC_URL=https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar

ENV MYSQL_JDBC_URL=${MYSQL_JDBC_URL}
ENV POSTGRES_JDBC_URL=${POSTGRES_JDBC_URL}

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash curl unzip ca-certificates tini \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/saiku \
  && curl -fsSL "${SAIKU_DOWNLOAD_URL}" -o /tmp/saiku.zip \
  && unzip -q /tmp/saiku.zip -d /opt/saiku \
  && rm -f /tmp/saiku.zip

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
EXPOSE 8080
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
