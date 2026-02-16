FROM eclipse-temurin:11-jre-jammy

ARG PDI_VERSION=9.4.0.0-343
ARG PDI_DOWNLOAD_URL=https://downloads.sourceforge.net/project/pentaho/Data%20Integration/${PDI_VERSION}/pdi-ce-${PDI_VERSION}.zip

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash curl unzip ca-certificates tini \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/pdi \
  && curl -fsSL "${PDI_DOWNLOAD_URL}" -o /tmp/pdi.zip \
  && unzip -q /tmp/pdi.zip -d /opt/pdi \
  && rm -f /tmp/pdi.zip

ENV PDI_HOME=/opt/pdi/data-integration
ENV PATH=${PDI_HOME}:${PDI_HOME}/kitchen.sh:${PDI_HOME}/pan.sh:${PATH}

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD ["shell"]
