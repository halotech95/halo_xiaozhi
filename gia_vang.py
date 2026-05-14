from fastmcp import FastMCP
import requests
import logging
import sys

# =========================================================
# LOGGER
# =========================================================

logger = logging.getLogger("GoldPrice")

if sys.platform == "win32":
    sys.stderr.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

# =========================================================
# MCP SERVER
# =========================================================

mcp = FastMCP("GoldPrice")

# =========================================================
# TOOL
# =========================================================

@mcp.tool()
def get_gold_price() -> dict:
    """
    Get Vietnam gold price (SJC).

    Returns:
        dict
    """

    try:

        response = requests.get(
            "https://www.goldapi.io/api/XAU/USD",
            headers={
                "x-access-token": "goldapi-demo-token",
                "Content-Type": "application/json"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        result = {
            "success": True,
            "metal": data.get("metal"),
            "currency": data.get("currency"),
            "price": data.get("price"),
            "price_gram_24k": data.get("price_gram_24k"),
            "updated_at": data.get("timestamp")
        }

        logger.info(f"Gold result: {result}")

        return result

    except Exception as e:

        logger.exception("Gold tool failed")

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")