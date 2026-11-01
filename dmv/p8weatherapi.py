# 8. OpenWeatherMap API -> DataFrame -> Clean -> Analyze -> Plot

# Get a free API key from https://openweathermap.org/api
# Paste your API key below.
# If no key is provided, the script uses data/weather_sample.json

import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# -----------------------------
# 1 & 2. Get Weather Data
# -----------------------------
API_KEY = ""
CITY = "Pune"

if API_KEY:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
else:
    data = json.load(open("data/weather_sample.json"))

# -----------------------------
# 3. Extract Weather Attributes
# -----------------------------
df = pd.DataFrame([
    {
        "time": x["dt_txt"],
        "temp": x["main"]["temp"],
        "humidity": x["main"]["humidity"],
        "wind": x["wind"]["speed"],
        "rain": x.get("rain", {}).get("3h", 0)
    }
    for x in data["list"]
])

# -----------------------------
# 4. Clean & Preprocess
# -----------------------------
df["time"] = pd.to_datetime(df["time"])
df = df.dropna()
df = df.set_index("time")

# -----------------------------
# 5. Data Modeling
# -----------------------------
print("\nOverall Statistics:")
print(df.describe().round(2))

daily = df.resample("D").agg({
    "temp": ["mean", "max", "min"],
    "rain": "sum",
    "wind": "mean"
})

print("\nDaily Weather Summary:")
print(daily.head())

# -----------------------------
# 6. Visualization
# -----------------------------
fig, ax = plt.subplots(1, 3, figsize=(15, 4))

df["temp"].plot(ax=ax[0], title="Temperature (°C)")

daily["rain"].plot.bar(
    ax=ax[1],
    title="Daily Rainfall (mm)",
    xticks=[]
)

ax[2].scatter(df["temp"], df["humidity"])
ax[2].set_title("Temperature vs Humidity")
ax[2].set_xlabel("Temperature")
ax[2].set_ylabel("Humidity")

plt.tight_layout()
plt.show()

# -----------------------------
# 7. Data Aggregation
# -----------------------------
monthly = df.resample("M").agg({
    "temp": "mean",
    "humidity": "mean",
    "wind": "mean",
    "rain": "sum"
})

print("\nMonthly Summary:")
print(monthly)

# -----------------------------
# 8. Geographical Visualization
# -----------------------------
lat = data["city"]["coord"]["lat"]
lon = data["city"]["coord"]["lon"]

print("\nLocation Coordinates")
print("Latitude :", lat)
print("Longitude:", lon)

weather_map = folium.Map(
    location=[lat, lon],
    zoom_start=10
)

folium.Marker(
    [lat, lon],
    popup=CITY,
    tooltip="Weather Location"
).add_to(weather_map)

weather_map.save("weather_map.html")

print("Map saved successfully as 'weather_map.html'")

# -----------------------------
# 9. Correlation Analysis
# -----------------------------
plt.figure(figsize=(6, 4))
sns.heatmap(
    df.corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.show()