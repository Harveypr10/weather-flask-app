from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Securely fetch API key
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_weather(city):
    """Fetch weather data from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses
        data = response.json()

        if "main" in data and "coord" in data:
            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "city": city,
                "lat": data["coord"]["lat"],
                "lon": data["coord"]["lon"]
            }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")

    return None  # Return None if data can't be retrieved

@app.route("/", methods=["GET", "POST"])
def index():
    """Render the web app and update location dynamically."""
    location = {"lat": 51.5074, "lon": -0.1278}  # Default: London
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:  # Only fetch if the user inputs a city
            weather_data = get_weather(city)
            if weather_data:
                location = {"lat": weather_data["lat"], "lon": weather_data["lon"]}  # Update location

    print("DEBUG: Sending location:", location)  # Debugging step
    return render_template("index.html", weather=weather_data, location=location)

# Ensure Gunicorn can properly reference the Flask app
if __name__ == "__main__":
    app.run(debug=True)