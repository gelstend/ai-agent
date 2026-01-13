import requests


def geocode_location(location_name: str) -> dict:
    """
    Convert location name to latitude and longitude using Open-Meteo Geocoding API.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": location_name,
        "count": 1,
        "language": "zh",
        "format": "json"
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results")
        if not results:
            return {"error": f"No location found for '{location_name}'"}

        loc = results[0]
        return {
            "name": loc.get("name"),
            "latitude": loc.get("latitude"),
            "longitude": loc.get("longitude"),
            "country": loc.get("country"),
            "admin": loc.get("admin1"),
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print(geocode_location("北京市"))
