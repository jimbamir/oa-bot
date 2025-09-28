
import requests, pandas as pd
from tenacity import retry, wait_exponential, stop_after_attempt

KEEPA_ENDPOINT = "https://api.keepa.com/product"

@retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(3))
def keepa_lookup_by_ean(ean: str, keepa_key: str):
    if not ean or not keepa_key: return {}
    params = {"key": keepa_key, "domain": 3, "code": ean, "buybox": 1, "history": 0}
    r = requests.get(KEEPA_ENDPOINT, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if not data.get("products"): return {}
    prod = data["products"][0]
    out = {
        "asin": prod.get("asin"),
        "category": (prod.get("categoryTree") or [{}])[-1].get("name") if prod.get("categoryTree") else None,
        "bsr": (prod.get("stats") or {}).get("salesRankDrops30", None),
        "amazon_seller": "Amazon" if prod.get("isAmazon") else None,
    }
    stats = prod.get("stats") or {}
    bb = stats.get("buyBoxPrice")
    amz = stats.get("current") if isinstance(stats.get("current"), dict) else {}
    price_cents = None
    if isinstance(bb, (int, float)) and bb > 0: price_cents = bb
    elif isinstance(amz, dict) and isinstance(amz.get("priceAmazon"), (int, float)) and amz.get("priceAmazon") > 0:
        price_cents = amz.get("priceAmazon")
    if price_cents: out["amazon_price"] = round(price_cents / 100.0, 2)
    return out

def enrich_with_keepa(df: pd.DataFrame, keepa_key: str):
    df = df.copy()
    for i, row in df.iterrows():
        needs_price = pd.isna(row.get("amazon_price")) or float(row.get("amazon_price") or 0) == 0.0
        if needs_price:
            info = keepa_lookup_by_ean(str(row.get("ean") or "").strip(), keepa_key)
            for k, v in (info or {}).items():
                df.at[i, k] = v
    return df
