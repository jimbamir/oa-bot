# Use the official hassio-addons base which includes bashio + s6
ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.2.3
FROM ${BUILD_FROM}

# System packages & python
RUN apk add --no-cache     jq     python3 py3-pip     py3-numpy py3-pandas py3-lxml     libstdc++ libffi-dev openssl-dev     gcc musl-dev libxml2-dev libxslt-dev

# Virtualenv to avoid PEP 668 issues
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r /app/requirements.txt

COPY app /app

# Copy s6 service (no cont-init scripts)
COPY rootfs/ /
RUN chmod 0755 /etc/services.d/oa/run

EXPOSE 8501
