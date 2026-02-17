FROM eclipse-temurin:17-jre-jammy

ARG PRD_VERSION=11.0.0.0-237

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      bash unzip ca-certificates tini \
      xvfb x11vnc fluxbox novnc websockify xterm \
      fonts-dejavu \
  && rm -rf /var/lib/apt/lists/*

COPY prd-ce-${PRD_VERSION}.zip /tmp/prd.zip

RUN mkdir -p /opt/prd \
  && unzip -q /tmp/prd.zip -d /opt/prd \
  && rm -f /tmp/prd.zip

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

WORKDIR /workspace
EXPOSE 5900 6080
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
