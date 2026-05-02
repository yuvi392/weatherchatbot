from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_OPENWEATHER_API_KEY"

def extract_city(text):
    words = text.split()
    for word in words:
        if word[0].isupper():
            return word
    return None

@app.route('/weather', methods=['POST'])
def weather():
    data = request.json
    text = data.get("text", "")

    city = extract_city(text)

    if not city:
        return jsonify({
            "response": "Please tell me the city name (e.g., weather in Delhi)."
        })

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()

    if res.get("cod") != "200":
        return jsonify({
            "response": "City not found. Try again."
        })

    forecast_list = res["list"]

    # Take 1 data per day (every 24 hours → every 8th record)
    days = forecast_list[::8][:5]

    result = f"🌤 5-Day Forecast for {city}:\n\n"

    for i, day in enumerate(days):
        temp = day["main"]["temp"]
        desc = day["weather"][0]["description"]

        result += f"📅 Day {i+1}\n🌡 Temp: {temp}°C\n☁ {desc}\n\n"

    return jsonify({
  "generic": [
    {
      "response_type": "text",
      "text": result
    }
  ]
})

if __name__ == "__main__":
    app.run()