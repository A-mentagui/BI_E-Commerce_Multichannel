FROM eclipse-temurin:11-jre-jammy

ARG SAIKU_VERSION=3.17
ARG MYSQL_JDBC_URL=https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.4.0/mysql-connector-j-8.4.0.jar
ARG POSTGRES_JDBC_URL=https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar

ENV MYSQL_JDBC_URL=${MYSQL_JDBC_URL}
ENV POSTGRES_JDBC_URL=${POSTGRES_JDBC_URL}

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash unzip ca-certificates tini \
  && rm -rf /var/lib/apt/lists/*

COPY saiku-server-${SAIKU_VERSION}.zip /tmp/saiku.zip

RUN mkdir -p /opt/saiku \
  && unzip -q /tmp/saiku.zip -d /opt/saiku \
  && rm -f /tmp/saiku.zip

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
EXPOSE 8080
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
