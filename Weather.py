import requests

API_KEY = "86760c8e26b540b685a92721252905"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city):
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "no"
    }

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        current = data["current"]
        location = data["location"]

        print("\n🌤️ Weather Report for", location["name"], ",", location["country"])
        print("🕒 Local Time:", location["localtime"])
        print("🌡️ Temperature:", current["temp_c"], "°C")
        print("🌡️ Feels Like:", current["feelslike_c"], "°C")
        print("🌥️ Condition:", current["condition"]["text"])
        print("💨 Wind:", current["wind_kph"], "kph")
        print("💧 Humidity:", current["humidity"], "%")
        print("🔴 UV Index:", current["uv"])
        print("📡 Cloud Cover:", current["cloud"], "%\n")

    elif response.status_code == 400:
        print("[❌] City not found or invalid request.")
    elif response.status_code == 401:
        print("[❌] Invalid or missing API key.")
    else:
        print(f"[❌] Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    while True:
        city = input("🔍 Enter city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("👋 Goodbye!")
            break
        get_weather(city)
