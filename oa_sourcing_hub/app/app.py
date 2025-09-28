
import os, asyncio, pandas as pd, streamlit as st
from src.calc import compute_metrics, default_fee_model
from src.filters import apply_filters
from src.keepa_client import enrich_with_keepa
from src.gsheets import export_to_gsheet, ensure_sheet
from src.scheduler import schedule_jobs, list_jobs, trigger_job_now, register_email_jobs
from src.crawl.engine import crawl_all_shops

st.set_page_config(page_title="OA Sourcing Hub PRO — HA Add-on", layout="wide")
st.title("🛒 OA Sourcing Hub PRO — Home Assistant Add-on")

min_roi_default = float(os.getenv("DEFAULT_MIN_ROI", "0.30"))
min_margin_default = float(os.getenv("DEFAULT_MIN_MARGIN", "0.12"))
exclude_amz_default = os.getenv("EXCLUDE_AMAZON_SELLER","true").lower()=="true"
keepa_key = os.getenv("KEEPA_KEY","").strip()

email_enabled = os.getenv("EMAIL_ENABLED","false").lower() == "true"
email_to = os.getenv("EMAIL_TO","")

with st.sidebar:
    st.header("Filters & Keepa")
    min_roi = st.number_input("Min ROI", value=min_roi_default, min_value=0.0, max_value=1.0, step=0.01)
    min_margin = st.number_input("Min Margin", value=min_margin_default, min_value=0.0, max_value=1.0, step=0.01)
    exclude_amz = st.checkbox("Exclude Amazon as Seller", value=exclude_amz_default)
    st.caption("Keepa-Key & Mail-Settings über Add-on-Optionen.")

tab1, tab2, tab3, tab4 = st.tabs(["Auto-Crawl", "Results", "Export", "Scheduler"])

with tab1:
    st.subheader("Crawl EU Shops")
    if st.button("Run Crawl Now"):
        with st.spinner("Crawling..."):
            products = asyncio.run(crawl_all_shops())
            df = pd.DataFrame(products)
            st.session_state["crawl_raw"] = df
            st.success(f"Crawled {len(df)} candidates.")
    raw = st.session_state.get("crawl_raw")
    if raw is not None and not raw.empty:
        st.dataframe(raw.head(100), use_container_width=True)
        if st.button("Keepa Enrichment + Metrics"):
            with st.spinner("Keepa + Metrics..."):
                df2 = enrich_with_keepa(raw, keepa_key=keepa_key)
                out = compute_metrics(df2, fee_model=default_fee_model())
                st.session_state["results"] = out
                st.success("Done → Results")

with tab2:
    st.subheader("Filtered Results")
    res = st.session_state.get("results")
    if res is None or res.empty:
        st.info("No results yet.")
    else:
        filtered = apply_filters(res, min_roi=min_roi, min_margin=min_margin, exclude_amazon=exclude_amz)
        st.dataframe(filtered, use_container_width=True)
        st.download_button("Download CSV", filtered.to_csv(index=False).encode("utf-8"), "oa_results.csv", "text/csv")

with tab3:
    st.subheader("Export → Google Sheets")
    sa_path = "./google_sa.json"
    sheet_name = "OA_Sourcing_Results"
    ws_name = "Results"
    if st.button("Export current results"):
        res = st.session_state.get("results")
        if res is None or res.empty:
            st.warning("No results to export.")
        else:
            try:
                sh, ws = ensure_sheet(sa_path, sheet_name, ws_name)
                export_to_gsheet(ws, res)
                st.success(f"Exported to {sheet_name}/{ws_name}.")
            except Exception as e:
                st.error(f"Export failed: {e}")

with tab4:
    st.subheader("Scheduler & Emails")
    col1, col2 = st.columns(2)
    if col1.button("Start scheduler (Daily 06:00)"):
        schedule_jobs()
        if email_enabled and email_to:
            register_email_jobs()
        st.success("Scheduler started.")
    if col2.button("List jobs"):
        st.code("\n".join(list_jobs()) or "No jobs")
    if st.button("Run daily job now"):
        trigger_job_now()
        st.info("Triggered.")
    if email_enabled:
        st.info(f"E-Mail Benachrichtigungen aktiv → {email_to}")
    else:
        st.warning("E-Mail Benachrichtigungen sind deaktiviert (EMAIL_ENABLED=false).")
