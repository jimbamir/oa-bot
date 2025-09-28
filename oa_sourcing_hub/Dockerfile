
# Home Assistant Add-on Base
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# System Python & tools
RUN apk add --no-cache     jq     python3 py3-pip     py3-numpy py3-pandas py3-lxml     libstdc++ libffi-dev openssl-dev     gcc musl-dev libxml2-dev libxslt-dev

# Virtualenv for Python packages
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"     PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY app /app

# s6 services (pure /bin/sh scripts)
RUN mkdir -p /etc/services.d/oa
COPY run.sh /etc/services.d/oa/run
RUN chmod +x /etc/services.d/oa/run

# cont-init hook (pure /bin/sh)
COPY rootfs/ /
RUN chmod +x /etc/cont-init.d/00-log-config

EXPOSE 8501
