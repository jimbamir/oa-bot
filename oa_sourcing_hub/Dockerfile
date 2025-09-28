
# Home Assistant Add-on Base (Alpine + s6-overlay)
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

RUN apk add --no-cache     python3 py3-pip     py3-numpy py3-pandas py3-lxml     libstdc++ libffi-dev openssl-dev     gcc musl-dev libxml2-dev libxslt-dev

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"     PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY app /app
COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8501
CMD [ "/run.sh" ]
