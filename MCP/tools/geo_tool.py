import httpx
from typing import Dict
from MCP.tools.base import MCPTool


class GeoTool(MCPTool):
    name = "geocode"
    description = "Convert a location name (city, district, region) into latitude and longitude"

    def __init__(self, language: str = "zh", count: int = 1):
        self.base_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.language = language
        self.count = count

    def run(self, input: Dict[str, str], context):
        """
        input: {
            "location": str
        }
        """
        location = input.get("location")

        if not location:
            return "Error: location name is required"

        params = {
            "name": location,
            "count": self.count,
            "language": self.language,
            "format": "json"
        }

        try:
            resp = httpx.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            results = data.get("results")
            if not results:
                return f"No location found for '{location}'"

            loc = results[0]

            latitude = loc.get("latitude")
            longitude = loc.get("longitude")

            if latitude is None or longitude is None:
                return f"Invalid location data for '{location}'"

            display_name = " ".join(
                str(x) for x in [
                    loc.get("country"),
                    loc.get("admin1"),
                    loc.get("admin2"),
                    loc.get("name"),
                ] if x
            )

            return {
                "latitude": latitude,
                "longitude": longitude,
                "display_name": display_name
            }

        except Exception as e:
            return f"Error fetching geocoding data: {str(e)}"
