
import asyncio, datetime as dt, pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from src.crawl.engine import crawl_all_shops
from src.keepa_client import enrich_with_keepa
from src.calc import compute_metrics, default_fee_model
from src.filters import apply_filters
from src.emailer import send_mail
import os

_scheduler = None
_last_results = None

def _hourly_job():
    global _last_results
    products = asyncio.run(crawl_all_shops())
    df = pd.DataFrame(products)
    # Optionally, enrich + filter immediately for "hits"
    keepa_key = os.getenv("KEEPA_KEY","").strip()
    if keepa_key and not df.empty:
        df = enrich_with_keepa(df, keepa_key=keepa_key)
        df = compute_metrics(df, default_fee_model())
        filtered = apply_filters(df,
            min_roi=float(os.getenv("DEFAULT_MIN_ROI","0.30")),
            min_margin=float(os.getenv("DEFAULT_MIN_MARGIN","0.12")),
            exclude_amazon=os.getenv("EXCLUDE_AMAZON_SELLER","true").lower()=="true"
        )
        _last_results = filtered
        if not filtered.empty:
            top = filtered.head(10)[["title","ean","buy_price","amazon_price","roi","margin"]]
            body = "Top Treffer (stündlich):\n\n" + top.to_string(index=False)
            send_mail("OA Hub – Stündliche Treffer", body)

def _daily_summary():
    global _last_results
    if _last_results is None or _last_results.empty:
        send_mail("OA Hub – Tageszusammenfassung", "Heute keine Treffer nach Deinen Filtern.")
    else:
        top = _last_results.head(50)[["title","ean","buy_price","amazon_price","roi","margin"]]
        body = "Tageszusammenfassung:\n\n" + top.to_string(index=False)
        send_mail("OA Hub – Tageszusammenfassung", body)

def schedule_jobs():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler(timezone="Europe/Vienna")
        _scheduler.add_job(_daily_job, trigger="cron", hour=6, minute=0, id="daily_crawl", replace_existing=True)
        _scheduler.start()

def _daily_job():
    # keep minimal daily crawl as base
    _hourly_job()

def list_jobs():
    if _scheduler is None: return []
    return [str(j) for j in _scheduler.get_jobs()]

def trigger_job_now():
    _hourly_job()

def register_email_jobs():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler(timezone="Europe/Vienna")
        _scheduler.start()
    # Hourly hits (at minute 5 every hour)
    if not _scheduler.get_job("hourly_hits"):
        _scheduler.add_job(_hourly_job, trigger="cron", minute=5, id="hourly_hits", replace_existing=True)
    # Daily summary at 20:00
    if not _scheduler.get_job("daily_summary"):
        _scheduler.add_job(_daily_summary, trigger="cron", hour=20, minute=0, id="daily_summary", replace_existing=True)
