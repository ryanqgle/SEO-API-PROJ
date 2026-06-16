import requests, json

url = "https://api.open-meteo.com/v1/forecast"

coordsString = input("Enter a set of coordinates: ")

coords = coordsString.split(',')
print(coords)
params = {
    "latitude": float(coords[0]),
    "longitude": float(coords[1]),
    "current_weather": True,
    "hourly": "temperature_2m",
    "forecast_days": 1,
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "mph"
}

response = requests.get(url, params=params)
data = response.json() 
#print(data)
print(json.dumps(response.json(), indent=4))