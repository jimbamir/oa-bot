ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.2.3
FROM ${BUILD_FROM}

RUN apk add --no-cache bash dos2unix
COPY rootfs/ /
RUN dos2unix /etc/services.d/hello/run || true && chmod 0755 /etc/services.d/hello/run
