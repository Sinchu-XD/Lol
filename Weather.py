import requests

def get_weather(city):
    url = f"http://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        data = response.json()

        current = data['current_condition'][0]
        weather = {
            "City": city.title(),
            "Temperature": f"{current['temp_C']} °C",
            "Feels Like": f"{current['FeelsLikeC']} °C",
            "Weather": current['weatherDesc'][0]['value'],
            "Humidity": f"{current['humidity']}%",
            "Wind Speed": f"{current['windspeedKmph']} km/h",
            "Pressure": f"{current['pressure']} hPa"
        }

        return weather
    except Exception as e:
        return {"Error": f"Failed to fetch weather: {str(e)}"}

def display_weather(weather):
    if "Error" in weather:
        print(f"\n[❌] {weather['Error']}\n")
    else:
        print("\n====== 🌤️ Weather Report ======\n")
        for key, value in weather.items():
            print(f"{key}: {value}")
        print("\n===============================\n")

if __name__ == "__main__":
    while True:
        city = input("🔍 Enter city name (or type 'exit' to quit): ").strip()
        if city.lower() == 'exit':
            print("👋 Exiting Weather Terminal. Stay safe!")
            break
        weather_data = get_weather(city)
        display_weather(weather_data)
