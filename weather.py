# server.py

from fastmcp import FastMCP
import sys
import logging
import requests

logger = logging.getLogger("Weather")


# Fix UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stderr.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


# Create MCP server
mcp = FastMCP("Weather")


# Weather code mapping
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm"
}


# Add weather tool
@mcp.tool()
def get_weather(city: str) -> dict:
    """
Get real-time weather information for a specific city using the Open-Meteo API.

Parameters:
    city (str):
        Name of the city to query weather data for.
        Examples:
        - "Ha Noi"
        - "Tokyo"
        - "New York"

Returns:
    dict:
        A dictionary containing:
        - success (bool):
            True if request succeeded, False otherwise.

        - city (str):
            Requested city name.

        - country (str):
            Country of the detected location.

        - temperature_c (float):
            Current temperature in Celsius.

        - humidity_percent (float):
            Current relative humidity percentage.

        - wind_speed_kmh (float):
            Current wind speed in km/h.

        - description (str):
            Human-readable weather condition.

        - error (str):
            Error message if request failed.

Notes:
    - Uses Open-Meteo Geocoding API to convert city name
      into latitude and longitude.
    - Uses Open-Meteo Forecast API to fetch current weather.
    - No API key required.
"""

    try:

        # =====================================================
        # STEP 1: GET LAT/LON FROM CITY NAME
        # =====================================================

        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1
            },
            timeout=10
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return {
                "success": False,
                "error": f"City not found: {city}"
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        country = location.get("country", "Unknown")


        # =====================================================
        # STEP 2: GET WEATHER
        # =====================================================

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "wind_speed_10m,"
                    "weather_code"
                )
            },
            timeout=10
        )

        weather_data = weather_response.json()

        current = weather_data["current"]

        weather_code = current["weather_code"]

        result = {
            "success": True,
            "city": city,
            "country": country,
            "temperature_c": current["temperature_2m"],
            "humidity_percent": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "description": WEATHER_CODES.get(
                weather_code,
                "Unknown"
            )
        }

        logger.info(
            f"Weather request: {city}, result: {result}"
        )

        return result

    except Exception as e:

        logger.exception("Weather tool failed")

        return {
            "success": False,
            "error": str(e)
        }


# Start server
if __name__ == "__main__":
    mcp.run(transport="stdio")