FROM debian:bookworm-slim

ARG PRD_VERSION=10.2.0.0-218
ARG PRD_DOWNLOAD_URL=https://downloads.sourceforge.net/project/pentaho/Report%20Designer/${PRD_VERSION}/prd-ce-${PRD_VERSION}.zip

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      bash curl unzip ca-certificates tini \
      openjdk-11-jre \
      xvfb x11vnc fluxbox novnc websockify xterm \
      fonts-dejavu \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/prd \
  && curl -fsSL "${PRD_DOWNLOAD_URL}" -o /tmp/prd.zip \
  && unzip -q /tmp/prd.zip -d /opt/prd \
  && rm -f /tmp/prd.zip

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
EXPOSE 5900 6080
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
