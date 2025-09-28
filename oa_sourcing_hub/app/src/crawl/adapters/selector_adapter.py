
import aiohttp, re
from bs4 import BeautifulSoup

def _extract(soup, rule):
    if not rule: return None
    sel = soup.select_one(rule.get("selector",""))
    if not sel: return None
    if rule.get("attr") in (None, "text"):
        val = sel.get_text(" ", strip=True)
    else:
        val = sel.get(rule["attr"])
    rgx = rule.get("regex")
    if rgx:
        m = re.search(rgx, val or "")
        if m: val = m.group(0)
    return val

async def _fetch(session, url):
    try:
        async with session.get(url, timeout=15) as r:
            return await r.text()
    except Exception:
        return ""

async def crawl(product_url: str, cfg: dict):
    out = []
    async with aiohttp.ClientSession() as sess:
        html = await _fetch(sess, product_url)
        if not html: return out
        soup = BeautifulSoup(html, "lxml")
        item = {
            "title": _extract(soup, cfg.get("title")),
            "ean": _extract(soup, cfg.get("ean")),
            "buy_price": _extract(soup, cfg.get("price")),
            "shop_url": product_url
        }
        out.append(item)
    return out
