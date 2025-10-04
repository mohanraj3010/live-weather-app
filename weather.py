import os
import requests
from flask import Flask, render_template_string, request
from cachetools import TTLCache, cached
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY must be set in .env file")

# Flask app
app = Flask(__name__)

# Cache: store up to 100 results for 5 minutes
cache = TTLCache(maxsize=100, ttl=300)

# Weather API function with caching
@cached(cache)
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            return {"error": data.get("message", "Invalid city name")}

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "condition": data["weather"][0]["description"].title(),
        }
    except requests.exceptions.RequestException:
        return {"error": "Network error. Please try again later."}

# HTML template
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #f4f4f9; padding: 20px; }
        .container { max-width: 400px; margin: auto; background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        input { width: 70%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }
        button { padding: 10px 20px; border: none; background: #007BFF; color: white; border-radius: 8px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; margin-top: 10px; }
        .weather { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🌤 Live Weather App</h2>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter city name" required>
            <button type="submit">Search</button>
        </form>

        {% if weather %}
            {% if weather.error %}
                <p class="error">{{ weather.error }}</p>
            {% else %}
                <div class="weather">
                    <h3>{{ weather.city }}, {{ weather.country }}</h3>
                    <p><b>Temperature:</b> {{ weather.temperature }}°C</p>
                    <p><b>Humidity:</b> {{ weather.humidity }}%</p>
                    <p><b>Wind:</b> {{ weather.wind }} m/s</p>
                    <p><b>Condition:</b> {{ weather.condition }}</p>
                </div>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        weather = get_weather(city)
    return render_template_string(template, weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
