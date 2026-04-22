from __future__ import annotations

from dataclasses import dataclass

import requests


GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT_SECONDS = 10


class WeatherAppError(Exception):
    """Raised when a recoverable weather app error occurs."""


@dataclass
class LocationResult:
    name: str
    admin1: str | None
    country: str | None
    latitude: float
    longitude: float

    @property
    def display_name(self) -> str:
        parts = [self.name]
        if self.admin1:
            parts.append(self.admin1)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts)


@dataclass
class WeatherResult:
    temperature_c: float
    wind_speed_kph: float
    humidity_percent: int
    weather_code: int
    condition: str
    today_max_c: float
    today_min_c: float


WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_location(query: str) -> LocationResult:
    cleaned_query = query.strip()
    if not cleaned_query:
        raise WeatherAppError("Please enter a location to search.")

    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={
                "name": cleaned_query,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise WeatherAppError(
            "Couldn't reach the location service. Check your connection and try again."
        ) from exc

    data = response.json()
    results = data.get("results") or []
    if not results:
        raise WeatherAppError(f"No results found for '{cleaned_query}'.")

    location = results[0]
    return LocationResult(
        name=location["name"],
        admin1=location.get("admin1"),
        country=location.get("country"),
        latitude=location["latitude"],
        longitude=location["longitude"],
    )


def get_weather(latitude: float, longitude: float) -> WeatherResult:
    try:
        response = requests.get(
            FORECAST_API_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code"
                ),
                "daily": "temperature_2m_max,temperature_2m_min",
                "forecast_days": 1,
                "timezone": "auto",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise WeatherAppError(
            "Couldn't fetch weather data right now. Please try again in a moment."
        ) from exc

    data = response.json()
    current = data.get("current")
    daily = data.get("daily")

    if not current or not daily:
        raise WeatherAppError("Weather data was incomplete. Please try another search.")

    try:
        weather_code = int(current["weather_code"])
        return WeatherResult(
            temperature_c=float(current["temperature_2m"]),
            wind_speed_kph=float(current["wind_speed_10m"]),
            humidity_percent=int(current["relative_humidity_2m"]),
            weather_code=weather_code,
            condition=WEATHER_CODE_MAP.get(weather_code, "Unknown conditions"),
            today_max_c=float(daily["temperature_2m_max"][0]),
            today_min_c=float(daily["temperature_2m_min"][0]),
        )
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise WeatherAppError("Weather data format changed unexpectedly.") from exc
