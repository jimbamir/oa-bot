
#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -euo pipefail

# Read options via bashio
export KEEPA_KEY="$(bashio::config 'KEEPA_KEY')"
export DEFAULT_MIN_ROI="$(bashio::config 'DEFAULT_MIN_ROI')"
export DEFAULT_MIN_MARGIN="$(bashio::config 'DEFAULT_MIN_MARGIN')"
export EXCLUDE_AMAZON_SELLER="$(bashio::config 'EXCLUDE_AMAZON_SELLER')"
export CRAWL_CONCURRENCY="$(bashio::config 'CRAWL_CONCURRENCY')"

export EMAIL_ENABLED="$(bashio::config 'EMAIL_ENABLED')"
export EMAIL_SMTP_HOST="$(bashio::config 'EMAIL_SMTP_HOST')"
export EMAIL_SMTP_PORT="$(bashio::config 'EMAIL_SMTP_PORT')"
export EMAIL_USERNAME="$(bashio::config 'EMAIL_USERNAME')"
export EMAIL_PASSWORD="$(bashio::config 'EMAIL_PASSWORD')"
export EMAIL_FROM="$(bashio::config 'EMAIL_FROM')"
export EMAIL_TO="$(bashio::config 'EMAIL_TO')"

cd /app
exec /opt/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
