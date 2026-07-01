import requests
import pandas as pd
import sqlalchemy as db
from flask import Flask, render_template, request

app = Flask(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
engine = db.create_engine("sqlite:///weather.db")


def fetch_weather(latitude, longitude):
    """Fetch current + hourly forecast from Open-Meteo and cache it in SQLite."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
    }

    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Persist the hourly forecast to the database (same idea as main.py).
    df = pd.DataFrame.from_dict(data["hourly"])
    df.to_sql("forecast", con=engine, if_exists="replace", index=False)

    # Pair up each hour with its temperature for display.
    hourly = [
        {"time": t.replace("T", " "), "temp": temp}
        for t, temp in zip(df["time"], df["temperature_2m"])
    ]

    return {
        "current": data["current_weather"],
        "hourly": hourly,
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    coords = ""

    if request.method == "POST":
        coords = request.form.get("coords", "").strip()
        try:
            latitude, longitude = (float(part) for part in coords.split(","))
            weather = fetch_weather(latitude, longitude)
        except ValueError:
            error = "Enter coordinates as \"latitude, longitude\" — e.g. 40.71, -74.01"
        except requests.RequestException:
            error = "Could not reach the weather service. Please try again."

    return render_template("home.html", weather=weather, error=error, coords=coords)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
