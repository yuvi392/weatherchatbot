from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # 🔥 allow requests from your website

API_KEY = os.environ.get("API_KEY")


# 🔹 Current Weather
def get_current_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != 200:
            return "City not found."

        temp = data['main']['temp']
        desc = data['weather'][0]['description']

        return f"Current weather in {city}: {temp}°C, {desc}"

    except Exception:
        return "Error fetching current weather."


# 🔹 5-Day Forecast
def get_forecast(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != "200":
            return "Forecast unavailable."

        forecast_list = data['list']

        result = "5-Day Forecast:\n"

        for i in range(0, 40, 8):
            day = forecast_list[i]
            date = day['dt_txt']
            temp = day['main']['temp']
            desc = day['weather'][0]['description']

            result += f"{date} → {temp}°C, {desc}\n"

        return result

    except Exception:
        return "Error fetching forecast."


# 🔹 Home route
@app.route('/')
def home():
    return "Weather Chatbot API is running!"


# 🔹 Main API
@app.route('/weather', methods=['POST'])
def weather():
    try:
        data = request.get_json()

        if not data or 'city' not in data:
            return jsonify({"response": "Please provide a city name."}), 400

        city = data.get('city').strip()

        if not city:
            return jsonify({"response": "City cannot be empty."}), 400

        current = get_current_weather(city)
        forecast = get_forecast(city)

        return jsonify({
            "response": current + "\n\n" + forecast
        })

    except Exception:
        return jsonify({
            "response": "Server error. Try again later."
        }), 500


if __name__ == '__main__':
    app.run()