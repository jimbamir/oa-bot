
import os, asyncio, json
from .adapters import sitemap_adapter, rss_adapter, selector_adapter
from src.config_loader import load_shops_config

async def crawl_shop(row):
    shop = dict(row)
    stype = (shop.get("type") or "").strip().lower()
    base_url = shop.get("base_url")
    sconf = shop.get("selector_config")
    if stype == "sitemap":
        return await sitemap_adapter.crawl(base_url)
    elif stype == "rss":
        return await rss_adapter.crawl(base_url)
    elif stype == "selector":
        cfg = json.loads(sconf) if sconf else {}
        return await selector_adapter.crawl(base_url, cfg)
    else:
        return []

async def crawl_all_shops():
    cfg = load_shops_config()
    tasks = [crawl_shop(r) for _, r in cfg.iterrows()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    products = []
    for res in results:
        if isinstance(res, list):
            products.extend(res)
    seen = set()
    out = []
    for p in products:
        key = (p.get("ean"), p.get("shop_url"))
        if key in seen: continue
        seen.add(key)
        out.append(p)
    return out
