from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")




def extract_city(text):
    text = text.lower()

    # Remove common words
    stopwords = [
        "weather", "temperature", "forecast", "in", "for",
        "what", "is", "the", "today", "now", "tell", "me",
        "show", "please"
    ]

    words = re.split(r'\s+', text)

    # Remove stopwords
    filtered = [word for word in words if word not in stopwords]

    # Join remaining words (handles multi-word cities like New York)
    city = " ".join(filtered).strip()

    return city.title()


# 🔹 Current Weather
def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        return "City not found."

    temp = data['main']['temp']
    desc = data['weather'][0]['description']

    return f"Current weather in {city}: {temp}°C, {desc}"


# 🔹 5-Day Forecast
def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

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


# 🔹 Home route
@app.route('/')
def home():
    return "Weather Chatbot API is running!"


# 🔹 Main route (UPDATED)
@app.route('/weather', methods=['POST'])
def weather():
    user_input = request.json.get('input', '')

    city = extract_city(user_input)

    current = get_current_weather(city)
    forecast = get_forecast(city)

    return jsonify({
        "response": current + "\n\n" + forecast
    })


if __name__ == '__main__':
    app.run(debug=True)