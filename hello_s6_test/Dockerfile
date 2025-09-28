ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.2.3
FROM ${BUILD_FROM}

# Just a tiny runtime tool
RUN apk add --no-cache bash

# Copy s6 service (pure /bin/sh; no bashio/with-contenv)
COPY rootfs/ /
RUN chmod 0755 /etc/services.d/hello/run
