
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

# cont-init hook (pure /bin/sh)
COPY rootfs/ /

EXPOSE 8501

# Copy runtime script and set as container PID 1
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8501

# s6 services
COPY rootfs/etc/services.d/oa/run /etc/services.d/oa/run
RUN chmod +x /etc/services.d/oa/run

# cont-init hook
COPY rootfs/etc/cont-init.d/00-log-config /etc/cont-init.d/00-log-config
RUN chmod +x /etc/cont-init.d/00-log-config

EXPOSE 8501
