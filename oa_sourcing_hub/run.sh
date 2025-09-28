
#!/bin/sh
set -eu

# Read options from /data/options.json using jq (no bashio, no with-contenv)
getopt() {
  key="$1"; default="$2"
  if [ -f /data/options.json ]; then
    val="$(jq -r --arg k "$key" '.[$k] // empty' /data/options.json 2>/dev/null || true)"
    [ -n "$val" ] && { echo "$val"; return; }
  fi
  echo "$default"
}

export KEEPA_KEY="$(getopt KEEPA_KEY "")"
export DEFAULT_MIN_ROI="$(getopt DEFAULT_MIN_ROI "0.30")"
export DEFAULT_MIN_MARGIN="$(getopt DEFAULT_MIN_MARGIN "0.12")"
export EXCLUDE_AMAZON_SELLER="$(getopt EXCLUDE_AMAZON_SELLER "true")"
export CRAWL_CONCURRENCY="$(getopt CRAWL_CONCURRENCY "6")"

export EMAIL_ENABLED="$(getopt EMAIL_ENABLED "false")"
export EMAIL_SMTP_HOST="$(getopt EMAIL_SMTP_HOST "")"
export EMAIL_SMTP_PORT="$(getopt EMAIL_SMTP_PORT "587")"
export EMAIL_USERNAME="$(getopt EMAIL_USERNAME "")"
export EMAIL_PASSWORD="$(getopt EMAIL_PASSWORD "")"
export EMAIL_FROM="$(getopt EMAIL_FROM "")"
export EMAIL_TO="$(getopt EMAIL_TO "")"

cd /app
exec /opt/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
