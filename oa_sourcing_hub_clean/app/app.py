
import os
import streamlit as st

st.set_page_config(page_title="OA Sourcing Hub PRO", layout="wide")

st.title("OA Sourcing Hub PRO — Test UI")
st.write("Add-on läuft! 🎉")

keepa = os.environ.get("KEEPA_KEY", "")
st.info(f"KEEPA_KEY gesetzt: {'ja' if keepa else 'nein'}")

st.subheader("Environment")
for k in [
    "DEFAULT_MIN_ROI","DEFAULT_MIN_MARGIN","EXCLUDE_AMAZON_SELLER",
    "CRAWL_CONCURRENCY","EMAIL_ENABLED","EMAIL_SMTP_HOST","EMAIL_TO"
]:
    st.write(k, os.environ.get(k))
