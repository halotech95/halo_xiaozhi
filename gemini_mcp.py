from fastmcp import FastMCP
import requests
import logging
import os
import sys

# =========================================================
# LOGGER
# =========================================================

logger = logging.getLogger("GeminiLLM")

if sys.platform == "win32":
    sys.stderr.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

# =========================================================
# MCP SERVER
# =========================================================

mcp = FastMCP("GeminiLLM")

# =========================================================
# GEMINI CONFIG
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com"
    "/v1beta/models/gemini-2.0-flash:generateContent"
)

# =========================================================
# TOOL
# =========================================================

@mcp.tool()
def ask_gemini(prompt: str) -> dict:
    """
Use an external Gemini AI model to generate detailed responses,
perform advanced reasoning, answer complex questions,
analyze technical topics, and assist with tasks that may
benefit from a secondary AI model.

This tool should be used when:
- The user asks difficult or knowledge-heavy questions
- Additional reasoning or explanation is needed
- A longer or more detailed response would help
- Technical analysis or code generation is requested
- The assistant wants a second AI-generated opinion

Parameters:
    prompt (str):
        The user's question or instruction.

Returns:
    dict:
        success (bool):
            Whether the request succeeded.

        response (str):
            AI-generated response text.

        error (str):
            Error message if failed.

Notes:
    - Uses Google's Gemini API
    - Requires internet connection
    - May take several seconds to respond
"""

    try:

        if not GEMINI_API_KEY:

            return {
                "success": False,
                "error": "Missing GEMINI_API_KEY"
            }

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        text = (
            data["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        logger.info(f"Gemini request: {prompt}")

        return {
            "success": True,
            "response": text
        }

    except Exception as e:

        logger.exception("Gemini tool failed")

        return {
            "success": False,
            "error": str(e)
        }

# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")