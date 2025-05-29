import requests

API_KEY = "81bf870dee15ca954b37a143d38499cd"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "City": data["name"],
            "Country": data["sys"]["country"],
            "Temperature": f"{data['main']['temp']} °C",
            "Feels Like": f"{data['main']['feels_like']} °C",
            "Weather": data["weather"][0]["description"].title(),
            "Humidity": f"{data['main']['humidity']}%",
            "Wind Speed": f"{data['wind']['speed']} m/s",
            "Pressure": f"{data['main']['pressure']} hPa"
        }
        return weather
    elif response.status_code == 404:
        return {"Error": "City not found. Please check the name."}
    else:
        return {"Error": f"Error {response.status_code}: {response.reason}"}

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
      
