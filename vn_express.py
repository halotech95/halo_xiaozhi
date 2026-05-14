# server.py

from fastmcp import FastMCP
import sys
import logging
import requests
import xml.etree.ElementTree as ET


logger = logging.getLogger("VNExpressNews")


# Fix UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stderr.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


# Create MCP server
mcp = FastMCP("VNExpressNews")


# RSS categories
RSS_FEEDS = {
    "latest": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "technology": "https://vnexpress.net/rss/so-hoa.rss",
    "news": "https://vnexpress.net/rss/thoi-su.rss",
    "business": "https://vnexpress.net/rss/kinh-doanh.rss",
    "sports": "https://vnexpress.net/rss/the-thao.rss",
    "world": "https://vnexpress.net/rss/the-gioi.rss"
}


@mcp.tool()
def get_news(category: str = "latest", limit: int = 5) -> dict:
    """
Get latest news from VNExpress RSS feed.

Parameters:
    category (str):
        News category.

        Supported values:
        - latest
        - technology
        - news
        - business
        - sports
        - world

    limit (int):
        Number of news articles to return.

Returns:
    dict:
        {
            "success": bool,
            "category": str,
            "articles": [
                {
                    "title": str,
                    "link": str,
                    "published": str,
                    "summary": str
                }
            ]
        }
"""

    try:

        if category not in RSS_FEEDS:
            return {
                "success": False,
                "error": f"Invalid category: {category}"
            }

        rss_url = RSS_FEEDS[category]

        response = requests.get(
            rss_url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        root = ET.fromstring(response.content)

        channel = root.find("channel")

        items = channel.findall("item")

        articles = []

        for item in items[:limit]:

            title = item.findtext("title", default="")

            link = item.findtext("link", default="")

            pub_date = item.findtext("pubDate", default="")

            description = item.findtext("description", default="")

            articles.append({
                "title": title,
                "link": link,
                "published": pub_date,
                "summary": description
            })

        result = {
            "success": True,
            "category": category,
            "total": len(articles),
            "articles": articles
        }

        logger.info(
            f"News request: {category}, total: {len(articles)}"
        )

        return result

    except Exception as e:

        logger.exception("News tool failed")

        return {
            "success": False,
            "error": str(e)
        }


# Start server
if __name__ == "__main__":
    mcp.run(transport="stdio")