import httpx
from typing import Dict
from MCP.tools.base import MCPTool

class WeatherTool(MCPTool):
    name = "weather"
    description = "Get current weather by latitude and longitude using Open-Meteo API"

    def __init__(self, timezone: str = "auto"):
        """
        timezone: default "auto" -> API returns times in local timezone
        """
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.timezone = timezone

    def run(self, input: Dict[str, float], context):
        """
        input: {
            "latitude": float,
            "longitude": float
        }
        """
        latitude = input.get("latitude")
        longitude = input.get("longitude")

        if latitude is None or longitude is None:
            return "Error: latitude and longitude required"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "timezone": self.timezone,
        }

        try:
            # Call Open-Meteo API
            resp = httpx.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            # Extract current weather
            current = data.get("current_weather", {})
            if not current:
                return "No current weather found"

            # Build a simple text summary
            temp = current.get("temperature")
            wind = current.get("windspeed")
            weather_info = (
                f"Current weather at ({latitude}, {longitude}): "
                f"Temperature {temp}°C, wind {wind} km/h"
            )
            return weather_info

        except Exception as e:
            return f"Error fetching weather: {str(e)}"
