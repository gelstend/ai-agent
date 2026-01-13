import httpx


def get_current_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather from Open-Meteo API.

    :param latitude: 纬度
    :param longitude: 经度
    :return: dict with weather info
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto"
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather")
        if not current:
            raise ValueError("No current_weather data found")

        return {
            "latitude": latitude,
            "longitude": longitude,
            "temperature_c": current.get("temperature"),
            "wind_speed_kmh": current.get("windspeed"),
            "weather_time": current.get("time")
        }

    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    # 北京大概坐标
    lat = 39.9042
    lon = 116.4074

    result = get_current_weather(lat, lon)
    print(result)
