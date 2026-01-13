from coordinate_test import geocode_location
from weather_test import get_current_weather


def get_weather_by_location(location_name: str) -> dict:
    geo = geocode_location(location_name)
    if "error" in geo:
        return geo

    weather = get_current_weather(
        latitude=geo["latitude"],
        longitude=geo["longitude"]
    )

    if "error" in weather:
        return weather

    return {
        "location": f'{geo["country"]} {geo["admin"]} {geo["name"]}',
        **weather
    }


if __name__ == "__main__":
    print(get_weather_by_location("上海"))
