import math
from datetime import datetime, timedelta, timezone
import locale
from fmiopendata.wfs import download_stored_query
import requests
from xml.etree import ElementTree as ET
import dash
from dash import html, dcc
import plotly.graph_objs as go
import fmi_weather_client as fmi  # Import for forecast data

# Set locale to Finnish for day names
locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')

# === Constants ===
DEFAULT_CITY = "Helsinki"
PLACE_OPTIONS = ["Helsinki", "Turku", "Tampere", "Oulu", "Rovaniemi"]  # Add more cities as needed

# Extended weather condition map
WEATHER_CONDITION_MAP = {
    0.0: "Selkeä",  # Clear
    1.0: "Osittain pilvinen",  # Partly cloudy
    2.0: "Pilvinen",  # Cloudy
    3.0: "Kevyt sade",  # Light rain
    4.0: "Kohtalainen sade",  # Moderate rain
    5.0: "Väkevä sade",  # Heavy rain
    6.0: "Lumi",  # Snow
    7.0: "Sumu",  # Fog
    8.0: "Ukoskiviv",  # Thunderstorm
    9.0: "Räntä",  # Sleet
    10.0: "Huurre",  # Frost
    11.0: "Kevyt sade ja ukkonen",  # Light rain with thunder
    12.0: "Kohtalainen sade ja ukkonen",  # Moderate rain with thunder
    13.0: "Väkevä sade ja ukkonen",  # Heavy rain with thunder
    14.0: "Sateen ja ukkosen murtuminen",  # Break in rain and thunder
    15.0: "Räntä ja ukkonen",  # Sleet with thunder
    16.0: "Lumi ja ukkonen",  # Snow with thunder
    17.0: "Räntä ja lumi",  # Sleet and snow
    18.0: "Väkevä sumu",  # Dense fog
    19.0: "Kevyt sade ja sumu",  # Light rain and fog
    20.0: "Kohtalainen sade ja sumu",  # Moderate rain and fog
    21.0: "Väkevä sade ja sumu",  # Heavy rain and fog
    22.0: "Sumu ja tuulisuus",  # Fog with wind
    23.0: "Pilvinen ja tuulinen",  # Cloudy with wind
    24.0: "Selkeä ja tuulinen",  # Clear with wind
    25.0: "Lumi ja tuulinen",  # Snow with wind
    26.0: "Sateinen ja tuulinen",  # Rainy with wind
    27.0: "Ukkoja ja tuulinen",  # Thunderstorms with wind
    28.0: "Kevyt sade ja ukkonen ja tuulinen",  # Light rain with thunder and wind
    29.0: "Kohtalainen sade ja ukkonen ja tuulinen",  # Moderate rain with thunder and wind
    30.0: "Ukkosmyrsky",  # Thunderstorm (stronger)
    31.0: "Erittäin voimakas ukkonen",  # Very strong thunderstorm
    32.0: "Pilvinen ja jäätyvä sade",  # Cloudy with freezing rain
    33.0: "Väkevä jäätyvä sade",  # Heavy freezing rain
    34.0: "Pilvinen ja lumisateen alkaminen",  # Cloudy with snow beginning
    35.0: "Kevyt räntä",  # Light sleet
    36.0: "Kohtalainen räntä",  # Moderate sleet
    37.0: "Väkevä räntä",  # Heavy sleet
    38.0: "Paksu sumu",  # Thick fog
    39.0: "Kevyt sade ja sumu",  # Light rain and fog
    40.0: "Pilvinen ja sateen murtuminen",  # Cloudy with a break in rain
    41.0: "Jatkuva sade",  # Continuous rain
    42.0: "Lumipyry",  # Snowstorm
    43.0: "Väkevä lumipyry",  # Heavy snowstorm
    44.0: "Häivähdys",  # Traces of something (uncertain)
}

# Icons for the weather conditions
WEATHER_ICONS = {
    "Selkeä": "☀️",
    "Osittain pilvinen": "🌤️",
    "Pilvinen": "☁️",
    "Kevyt sade": "🌧️",
    "Kohtalainen sade": "🌧️",
    "Väkevä sade": "🌧️🌧️",
    "Lumi": "❄️",
    "Sumu": "🌫️",
    "Ukoskiviv": "🌩️",  # Thunderstorm
    "Räntä": "🌧️❄️",  # Sleet
    "Huurre": "🌨️",  # Frost
    "Tuntematon": "❓",  # Unknown or undefined condition
    "Kevyt sade ja ukkonen": "🌧️🌩️",  # Light rain with thunder
    "Kohtalainen sade ja ukkonen": "🌧️🌩️",  # Moderate rain with thunder
    "Väkevä sade ja ukkonen": "🌧️🌩️",  # Heavy rain with thunder
    "Sateen ja ukkosen murtuminen": "🌧️🌩️",  # Break in rain and thunder
    "Räntä ja ukkonen": "🌧️❄️🌩️",  # Sleet with thunder
    "Lumi ja ukkonen": "❄️🌩️",  # Snow with thunder
    "Räntä ja lumi": "🌧️❄️❄️",  # Sleet and snow
    "Väkevä sumu": "🌫️🌫️",  # Dense fog
    "Kevyt sade ja sumu": "🌧️🌫️",  # Light rain and fog
    "Kohtalainen sade ja sumu": "🌧️🌫️",  # Moderate rain and fog
    "Väkevä sade ja sumu": "🌧️🌫️🌧️",  # Heavy rain and fog
    "Sumu ja tuulisuus": "🌫️💨",  # Fog with wind
    "Pilvinen ja tuulinen": "☁️💨",  # Cloudy with wind
    "Selkeä ja tuulinen": "☀️💨",  # Clear with wind
    "Lumi ja tuulinen": "❄️💨",  # Snow with wind
    "Sateinen ja tuulinen": "🌧️💨",  # Rainy with wind
    "Ukkoja ja tuulinen": "🌩️💨",  # Thunderstorms with wind
    "Kevyt sade ja ukkonen ja tuulinen": "🌧️🌩️💨",  # Light rain with thunder and wind
    "Kohtalainen sade ja ukkonen ja tuulinen": "🌧️🌩️💨",  # Moderate rain with thunder and wind
    "Ukkosmyrsky": "🌩️🌩️",  # Thunderstorm (stronger)
    "Erittäin voimakas ukkonen": "⚡🌩️",  # Very strong thunderstorm
    "Pilvinen ja jäätyvä sade": "☁️🌨️",  # Cloudy with freezing rain
    "Väkevä jäätyvä sade": "🌨️❄️",  # Heavy freezing rain
    "Pilvinen ja lumisateen alkaminen": "☁️❄️",  # Cloudy with snow beginning
    "Kevyt räntä": "🌧️❄️",  # Light sleet
    "Kohtalainen räntä": "🌧️❄️",  # Moderate sleet
    "Väkevä räntä": "🌧️❄️❄️",  # Heavy sleet
    "Paksu sumu": "🌫️🌫️",  # Thick fog
    "Kevyt sade ja sumu": "🌧️🌫️",  # Light rain and fog
    "Pilvinen ja sateen murtuminen": "☁️🌧️",  # Cloudy with a break in rain
    "Jatkuva sade": "🌧️🌧️",  # Continuous rain
    "Lumipyry": "❄️❄️❄️",  # Snowstorm
}   

# === Observation data (last 24h) ===
def fetch_observed_data(place):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    start_str = start_time.isoformat(timespec="seconds") + "Z"
    end_str = end_time.isoformat(timespec="seconds") + "Z"

    obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                                args=[f"place={place}", f"starttime={start_str}", f"endtime={end_str}"])

    temperature_times = []
    temperature_values = []
    observed_condition = None

    for tstep in sorted(obs.data.keys()):
        for station_name in obs.data[tstep]:
            data = obs.data[tstep][station_name]
            temp = data.get("Air temperature")
            condition = data.get("Weather symbol3")
            
            if temp:
                temperature_times.append(tstep)
                temperature_values.append(temp["value"])

            if condition and not observed_condition:
                symbol_value = condition.get("value")
                if symbol_value is not None:
                    observed_condition = {
                        'icon': WEATHER_ICONS.get(WEATHER_CONDITION_MAP.get(symbol_value, "Tuntematon"), "❓"),
                        'text': WEATHER_CONDITION_MAP.get(symbol_value, f"Tuntematon ({symbol_value})"),
                        'temperature': temp["value"],
                        'wind_speed': data.get("Wind speed", {}).get("value", 0),
                        'snow_depth': data.get("Snow depth", {}).get("value", 0),
                        'date': end_time.strftime("%d.%m.%Y"),
                        'day_name': end_time.strftime("%A")  # Day name in Finnish
                    }

    # Default to clear sky condition if no condition is found
    if observed_condition is None:
        observed_condition = {
            'icon': "☀️",
            'text': "Selkeä",
            'temperature': 0,
            'wind_speed': 0,
            'snow_depth': 0,
            'date': end_time.strftime("%d.%m.%Y"),
            'day_name': end_time.strftime("%A")  # Day name in Finnish
        }

    return temperature_times, temperature_values, observed_condition


# === Forecast data (next 4 days) using fmi_weather_client ===
def get_weather(city):
    forecast = fmi.forecast_by_place_name(city)

    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    end_time = now + timedelta(days=4)

    weather_data = []
    for weather in forecast.forecasts:
        if now < weather.time <= end_time:
            condition_value = getattr(weather.symbol, "value", "Unknown")

            # Log the condition value for debugging purposes
            print(f"Debug: {weather.time.strftime('%d.%m.%Y')} - Condition: {condition_value}")

            # Map condition number to text
            condition_text = WEATHER_CONDITION_MAP.get(condition_value, "Tuntematon")

            snow_depth = getattr(weather, "snow_depth", 0)
            if snow_depth is None or not isinstance(snow_depth, (int, float)) or math.isnan(snow_depth):
                snow_depth = 0

            weather_data.append({
                "time": weather.time.isoformat(),
                "date": weather.time.strftime("%d.%m.%Y"),
                "day_name": weather.time.strftime("%A"),  # Day name in Finnish
                "temperature": weather.temperature.value,
                "low_temp": weather.temperature.value - 2,
                "wind_speed": weather.wind_speed.value,
                "snow_depth": snow_depth,
                "condition": condition_text  # Use the text description of the condition
            })

    return weather_data


# === Create Dash App ===
app = dash.Dash(__name__)
app.title = f"Säänäkymä"

# Fetch data once on startup (default to Helsinki)
obs_times, obs_temps, current_condition = fetch_observed_data(DEFAULT_CITY)
forecast_data = get_weather(DEFAULT_CITY)

# Extract forecast times, temperatures, and conditions
forecast_times = [entry['time'] for entry in forecast_data]
forecast_temps = [entry['temperature'] for entry in forecast_data]
forecast_condition = [entry['condition'] for entry in forecast_data]
forecast_dates = [entry['date'] for entry in forecast_data]
forecast_day_names = [entry['day_name'] for entry in forecast_data]

# === Layout ===
app.layout = html.Div([
    html.H1(f"Sää", style={'textAlign': 'center'}),

    # Dropdown for selecting city
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in PLACE_OPTIONS],
        value=DEFAULT_CITY,  # Default city
        style={'width': '50%', 'margin': '0 auto'}
    ),

    html.Div([  # Current condition frame
        html.Div([
            html.H4(f"{current_condition['date']} ({current_condition['day_name']})"),
            html.P(f"{current_condition['icon']} {current_condition['text']}"),
            html.P(f"Lämpötila: {current_condition['temperature']}°C"),
            html.P(f"Tuulen nopeus: {current_condition['wind_speed']} m/s"),
            html.P(f"Lumensyvyys: {current_condition['snow_depth']} cm"),
        ], style={
            'border': '1px solid #ccc',
            'padding': '10px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.1)',
            'textAlign': 'center',
            'backgroundColor': '#f9f9f9',
            'flex': '0',
            'margin': '5px',
            'minWidth': '220px',
        }),

        # Forecast frames (one for each day)
        html.Div([
            html.Div([
                html.H4(f"{forecast_dates[i]} ({forecast_day_names[i]})"),
                html.P(f"{WEATHER_ICONS.get(forecast_condition[i], '❓')} {forecast_condition[i]}"),
                html.P(f"Lämpötila: {forecast_temps[i]}°C"),
                html.P(f"Tuulen nopeus: {forecast_data[i]['wind_speed']} m/s"),
                html.P(f"Lumensyvyys: {forecast_data[i]['snow_depth']} cm"),
            ], style={
                'border': '1px solid #ccc',
                'padding': '10px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.1)',
                'textAlign': 'center',
                'backgroundColor': '#f9f9f9',
                'flex': '1',
                'margin': '5px',
                'minWidth': '220px',
            }) for i in range(len(forecast_dates))
        ], style={
            'display': 'flex',
            'flexWrap': 'nowrap',
            'justifyContent': 'space-between',
            'overflow': 'auto',
            'flexDirection': 'row',
            'alignItems': 'flex-start',
        }),

    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),

    dcc.Graph(
        id="temperature-chart",
        figure={
            "data": [
                go.Scatter(x=obs_times, y=obs_temps, mode="lines+markers", name="Havaittu lämpötila"),
                go.Scatter(x=forecast_times, y=forecast_temps, mode="lines+markers", name="Ennustettu lämpötila")
            ],
            "layout": go.Layout(
                title="Lämpötila",
                xaxis_title="Aika",
                yaxis_title="Lämpötila (°C)",
                hovermode="x unified"
            )
        }
    )
])


# === Update city data on dropdown change ===
@app.callback(
    dash.dependencies.Output('temperature-chart', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value')]
)
def update_city_data(selected_city):
    # Fetch new data for selected city
    obs_times, obs_temps, current_condition = fetch_observed_data(selected_city)
    forecast_data = get_weather(selected_city)

    forecast_times = [entry['time'] for entry in forecast_data]
    forecast_temps = [entry['temperature'] for entry in forecast_data]
    forecast_condition = [entry['condition'] for entry in forecast_data]

    # Update the temperature chart
    figure = {
        "data": [
            go.Scatter(x=obs_times, y=obs_temps, mode="lines+markers", name="Havaittu lämpötila"),
            go.Scatter(x=forecast_times, y=forecast_temps, mode="lines+markers", name="Ennustettu lämpötila")
        ],
        "layout": go.Layout(
            title="Lämpötila",
            xaxis_title="Aika",
            yaxis_title="Lämpötila (°C)",
            hovermode="x unified"
        )
    }

    return figure


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
