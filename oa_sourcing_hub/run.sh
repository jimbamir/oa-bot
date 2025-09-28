
#!/command/with-contenv bash
# shellcheck shell=bash
set -euo pipefail

# Load bashio (no suexec)
if [ -f /usr/lib/bashio/bashio.sh ]; then
  # shellcheck disable=SC1091
  . /usr/lib/bashio/bashio.sh
else
  echo "bashio library not found; continuing without (env-only mode)"
fi

# Read config (fallback to env defaults if bashio not present)
getcfg() {
  local key="$1" default="$2"
  if command -v bashio >/dev/null 2>&1; then
    bashio::config "${key}" || echo "${default}"
  else
    val="$(eval echo "\${key}")"
    echo "${val:-${default}}"
  fi
}

export KEEPA_KEY="$(getcfg 'KEEPA_KEY' '')"
export DEFAULT_MIN_ROI="$(getcfg 'DEFAULT_MIN_ROI' '0.30')"
export DEFAULT_MIN_MARGIN="$(getcfg 'DEFAULT_MIN_MARGIN' '0.12')"
export EXCLUDE_AMAZON_SELLER="$(getcfg 'EXCLUDE_AMAZON_SELLER' 'true')"
export CRAWL_CONCURRENCY="$(getcfg 'CRAWL_CONCURRENCY' '6')"

export EMAIL_ENABLED="$(getcfg 'EMAIL_ENABLED' 'false')"
export EMAIL_SMTP_HOST="$(getcfg 'EMAIL_SMTP_HOST' '')"
export EMAIL_SMTP_PORT="$(getcfg 'EMAIL_SMTP_PORT' '587')"
export EMAIL_USERNAME="$(getcfg 'EMAIL_USERNAME' '')"
export EMAIL_PASSWORD="$(getcfg 'EMAIL_PASSWORD' '')"
export EMAIL_FROM="$(getcfg 'EMAIL_FROM' '')"
export EMAIL_TO="$(getcfg 'EMAIL_TO' '')"

cd /app
exec /opt/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
