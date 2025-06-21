import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from datetime import datetime

API_KEY = "e6fbc5f7242887cdf263d42a412f4a06"
CITY = "KOLKATA"
UNITS = "metric"

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)

    data = response.json()
    print("✅ Fetched live weather data.")
    
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def append_to_csv(record, filename = "weather_history.csv"):
    df = pd.DataFrame([record])
    
    if not os.path.exists(filename):
        df.to_csv("weather_history.csv", index = False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)
    print("✅ Weather data appended to CSV.")


def plot_temperature(filename="weather_history.csv"):
    df = pd.read_csv(filename)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    last_7 = df.tail(7)

    plt.figure(figsize=(10, 5))
    plt.plot(last_7["timestamp"], last_7["temp"], marker="o", linestyle="-", color="orange")
    plt.title(f"Temperature Trend - {CITY}")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs("output", exist_ok=True)
    plt.savefig("output/temperature_trend.png")
    print("✅ Temperature trend chart saved in output/")

# ---------- MAIN ----------
if __name__ == "__main__":
    record = fetch_weather(CITY)
    append_to_csv(record)
    plot_temperature()
