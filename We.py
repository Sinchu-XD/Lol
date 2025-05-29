import requests

API_KEY = "6955219eb801cdbfcf12b4d9d185eb78"

def get_coordinates(city_name):
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    response = requests.get(geo_url, params=params)
    if response.status_code == 200 and response.json():
        city_data = response.json()[0]
        return city_data["lat"], city_data["lon"]
    else:
        print("[❌] City not found or invalid.")
        return None, None

def get_weather(lat, lon):
    weather_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "exclude": "minutely,hourly,daily,alerts"
    }
    response = requests.get(weather_url, params=params)
    if response.status_code == 200:
        data = response.json()
        current = data["current"]
        print("\n🌤️ Current Weather Report")
        print("🌡️ Temperature:", current["temp"], "°C")
        print("🌡️ Feels Like:", current["feels_like"], "°C")
        print("🌥️ Condition:", current["weather"][0]["description"].title())
        print("💧 Humidity:", current["humidity"], "%")
        print("💨 Wind Speed:", current["wind_speed"], "m/s")
        print("🔴 UV Index:", current["uvi"])
        print("📡 Cloud Cover:", current["clouds"], "%\n")
    elif response.status_code == 401:
        print("[❌] Unauthorized. Check your API key.")
    else:
        print(f"[❌] Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    while True:
        city = input("🔍 Enter city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("👋 Goodbye!")
            break
        lat, lon = get_coordinates(city)
        if lat and lon:
            get_weather(lat, lon)
          
