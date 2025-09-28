
import aiohttp
from bs4 import BeautifulSoup

async def crawl(rss_url: str):
    if not rss_url: return []
    async with aiohttp.ClientSession() as sess:
        async with sess.get(rss_url, timeout=15) as r:
            text = await r.text()
    soup = BeautifulSoup(text, "xml")
    items = []
    for item in soup.find_all("item"):
        link = item.find("link").text if item.find("link") else None
        title = item.find("title").text if item.find("title") else None
        items.append({"title": title, "ean": None, "buy_price": None, "shop_url": link})
    return items
