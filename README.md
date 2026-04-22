# Simple Weather App

A desktop weather application built with Python and Tkinter. The app lets users search for a city or place name, converts that location into latitude and longitude with the Open-Meteo Geocoding API, and then fetches current conditions plus a same-day temperature forecast from the Open-Meteo Forecast API.

This project is lightweight, beginner-friendly, does not require an API key, and now separates the GUI from the API service logic for easier maintenance.

## Features

- Search weather by city or location name
- Fetch geographic coordinates automatically using Open-Meteo Geocoding
- Show the matched location name with region and country details
- Display current temperature, wind speed, humidity, and weather condition
- Show today's high and low temperature forecast
- Show a weather icon based on the current temperature range
- Classify wind speed into simple text labels such as `Gentle breeze`, `Fresh breeze`, and `Strong gale`
- Simple desktop GUI built with Tkinter
- Provide clearer error messages for empty searches, missing locations, and API failures
- Separate UI and API logic with a dedicated `weather_service.py` module

## Built With

- Python 3.13+
- Tkinter
- Requests
- Open-Meteo Geocoding API
- Open-Meteo Forecast API

## Project Structure

```text
weather-app-python/
|-- logo/
|   |-- cold.png
|   |-- cool.png
|   |-- hot.png
|   |-- magnifier.png
|   `-- weather.png
|-- main.py
|-- weather_service.py
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

## How It Works

1. The user enters a location in the search box.
2. The app sends that text to the Open-Meteo geocoding endpoint.
3. The first matching result is used to get latitude and longitude.
4. Those coordinates are passed to the weather forecast endpoint.
5. The service layer validates the API responses and formats the result into simple Python data objects.
6. The GUI updates the location details, current weather metrics, today's forecast, and the temperature-based icon.

## Installation

### Option 1: Using `uv`

```bash
uv sync
uv run python main.py
```

### Option 2: Using `pip`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install requests
python main.py
```

## Requirements

- Python 3.13 or newer
- Internet connection

## Usage

1. Run the application.
2. Type a city or place name into the search field.
3. Press `Enter` or click the `Search` button.
4. View the location details, current conditions, and today's forecast for the selected location.

## Example Queries

- `Manila`
- `Tokyo`
- `New York`
- `London`

## Current Output

The app currently shows:

- Temperature in `deg C`
- Wind speed in kilometers per hour
- Relative humidity percentage
- Current weather condition text
- Today's high and low temperature
- The matched city, region, and country when available
- A weather icon selected from hot, cool, or cold temperature ranges
- A short wind description based on speed
- A status message for successful searches and user-friendly error feedback

## Known Limitations

- Only the first geocoding search result is used
- The interface still focuses on current conditions and a same-day forecast rather than a multi-day outlook
- The app depends on a live internet connection and the availability of Open-Meteo services
- The desktop UI is still a single-window Tkinter app without search history or saved locations

## Author

Created as a Python weather app project using Tkinter and Open-Meteo APIs.
