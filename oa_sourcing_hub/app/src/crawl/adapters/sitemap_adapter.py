
import aiohttp
from bs4 import BeautifulSoup

async def crawl(sitemap_url: str):
    if not sitemap_url: return []
    async with aiohttp.ClientSession() as sess:
        async with sess.get(sitemap_url, timeout=15) as r:
            text = await r.text()
    soup = BeautifulSoup(text, "xml")
    locs = [loc.text for loc in soup.find_all("loc")]
    product_urls = [u for u in locs if any(x in u.lower() for x in ["/product","/produkt","/artikel","/p/","/prod/","/sku/","/item/","/produkte/","/product-page","/shop/"])]
    return [{"title": None, "ean": None, "buy_price": None, "shop_url": u} for u in product_urls[:500]]
