import os
import streamlit as st

st.set_page_config(page_title="OA Sourcing Hub PRO (clean)", layout="wide")
st.title("OA Sourcing Hub PRO (clean)")

st.success("Add-on is running ✅")

with st.expander("Konfiguration (aus ENV)", expanded=False):
    cfg = {
        "KEEPA_KEY": os.getenv("KEEPA_KEY", ""),
        "DEFAULT_MIN_ROI": os.getenv("DEFAULT_MIN_ROI", ""),
        "DEFAULT_MIN_MARGIN": os.getenv("DEFAULT_MIN_MARGIN", ""),
        "EXCLUDE_AMAZON_SELLER": os.getenv("EXCLUDE_AMAZON_SELLER", ""),
        "CRAWL_CONCURRENCY": os.getenv("CRAWL_CONCURRENCY", ""),
        "EMAIL_ENABLED": os.getenv("EMAIL_ENABLED", ""),
        "EMAIL_SMTP_HOST": os.getenv("EMAIL_SMTP_HOST", ""),
        "EMAIL_SMTP_PORT": os.getenv("EMAIL_SMTP_PORT", ""),
        "EMAIL_USERNAME": os.getenv("EMAIL_USERNAME", ""),
        "EMAIL_PASSWORD": "***" if os.getenv("EMAIL_PASSWORD") else "",
        "EMAIL_FROM": os.getenv("EMAIL_FROM", ""),
        "EMAIL_TO": os.getenv("EMAIL_TO", ""),
    }
    st.json(cfg)

st.write("Dies ist eine Minimal-UI zum Funktionscheck. Crawler/Keepa kannst du später ergänzen.")
