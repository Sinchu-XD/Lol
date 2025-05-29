import requests

API_KEY = "6955219eb801cdbfcf12b4d9d185eb78"  # Replace with your valid key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    # Print full URL for debug
    print(f"[DEBUG] Requesting: {BASE_URL}?q={city}&appid={API_KEY}&units=metric")

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "City": data["name"],
            "Country": data["sys"]["country"],
            "Temperature": f"{data['main']['temp']} °C",
            "Weather": data["weather"][0]["description"].title(),
            "Humidity": f"{data['main']['humidity']}%",
            "Wind Speed": f"{data['wind']['speed']} m/s",
        }
    elif response.status_code == 401:
        return {"Error": "401 Unauthorized. Your API key is invalid or inactive."}
    elif response.status_code == 404:
        return {"Error": "404 City not found. Try another city name."}
    else:
        return {"Error": f"Error {response.status_code}: {response.text}"}

def display_weather(info):
    if "Error" in info:
        print(f"\n[❌] {info['Error']}\n")
    else:
        print("\n====== 🌦️ Weather Report ======")
        for key, value in info.items():
            print(f"{key}: {value}")
        print("================================\n")

if __name__ == "__main__":
    while True:
        city = input("🔍 Enter city name (or type 'exit' to quit): ").strip()
        if city.lower() == 'exit':
            print("👋 Exiting Weather Terminal. Stay safe!")
            break
        result = get_weather(city)
        display_weather(result)
        
