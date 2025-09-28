#!/command/with-contenv bashio
#!/usr/bin/with-contenv bash
# shellcheck shell=bash
set -e

# Load bashio library
if [ -f /usr/lib/bashio/bashio.sh ]; then
  # shellcheck disable=SC1091
  . /usr/lib/bashio/bashio.sh
fi

# Read addon options via bashio if available; else fallback to env (empty)
export KEEPA_KEY="$(bashio::config 'KEEPA_KEY' || echo "${KEEPA_KEY}")"
export DEFAULT_MIN_ROI="$(bashio::config 'DEFAULT_MIN_ROI' || echo "${DEFAULT_MIN_ROI:-0.30}")"
export DEFAULT_MIN_MARGIN="$(bashio::config 'DEFAULT_MIN_MARGIN' || echo "${DEFAULT_MIN_MARGIN:-0.12}")"
export EXCLUDE_AMAZON_SELLER="$(bashio::config 'EXCLUDE_AMAZON_SELLER' || echo "${EXCLUDE_AMAZON_SELLER:-true}")"
export CRAWL_CONCURRENCY="$(bashio::config 'CRAWL_CONCURRENCY' || echo "${CRAWL_CONCURRENCY:-6}")"

export EMAIL_ENABLED="$(bashio::config 'EMAIL_ENABLED' || echo "${EMAIL_ENABLED:-false}")"
export EMAIL_SMTP_HOST="$(bashio::config 'EMAIL_SMTP_HOST' || echo "${EMAIL_SMTP_HOST}")"
export EMAIL_SMTP_PORT="$(bashio::config 'EMAIL_SMTP_PORT' || echo "${EMAIL_SMTP_PORT:-587}")"
export EMAIL_USERNAME="$(bashio::config 'EMAIL_USERNAME' || echo "${EMAIL_USERNAME}")"
export EMAIL_PASSWORD="$(bashio::config 'EMAIL_PASSWORD' || echo "${EMAIL_PASSWORD}")"
export EMAIL_FROM="$(bashio::config 'EMAIL_FROM' || echo "${EMAIL_FROM}")"
export EMAIL_TO="$(bashio::config 'EMAIL_TO' || echo "${EMAIL_TO}")"

cd /app
exec /opt/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0