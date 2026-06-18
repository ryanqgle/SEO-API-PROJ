import requests, json
import sqlalchemy as db
import pandas as pd

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
response.raise_for_status()
data = response.json() 

df = pd.DataFrame.from_dict(data["hourly"])

engine = db.create_engine('sqlite:///weather.db')

df.to_sql('forecast', con=engine, if_exists='replace', index=False)

with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM forecast;")).fetchall()
   print(pd.DataFrame(query_result))

#print(data)
#print(json.dumps(response.json(), indent=4))
