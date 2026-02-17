FROM eclipse-temurin:11-jre-jammy

ARG PSW_VERSION=11.0.0.0-237

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash unzip ca-certificates tini \
  && rm -rf /var/lib/apt/lists/*

COPY psw-ce-${PSW_VERSION}.zip /tmp/psw.zip

RUN mkdir -p /opt/psw \
  && unzip -q /tmp/psw.zip -d /opt/psw \
  && rm -f /tmp/psw.zip

ENV PSW_HOME=/opt/psw/workbench-schema
ENV PATH=${PSW_HOME}:${PSW_HOME}/bin:${PATH}

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

WORKDIR /workspace
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD ["shell"]
