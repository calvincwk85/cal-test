from flask import Flask, request, render_template_string
import requests
from datetime import datetime
import pytz  # Import pytz for time zone handling

app = Flask(__name__)

# Replace with your Weatherstack API key
WEATHERSTACK_API_KEY = "d9ab17d81cc2ff3a926ad905ffdaaff6"

# Map locations to their respective time zones
LOCATION_TIMEZONES = {
    "Singapore": "Asia/Singapore",
    "Tokyo": "Asia/Tokyo",
    "New York": "America/New_York",
    "London": "Europe/London",
    "Sydney": "Australia/Sydney",
    "New Delhi": "Asia/Kolkata",
    "Bangkok": "Asia/Bangkok",
    "Los Angeles": "America/Los_Angeles",
    "Moscow": "Europe/Moscow",
    "Berlin": "Europe/Berlin",
    "Nairobi": "Africa/Nairobi",
    "Johannesburg": "Africa/Johannesburg",
    "Shanghai": "Asia/Shanghai",
    "Paris": "Europe/Paris",
}

@app.route("/", methods=["GET", "POST"])
def weather():
    # List of locations for the dropdown
    locations = list(LOCATION_TIMEZONES.keys())
    selected_location = None
    weather_result = ""
    weather_icon_url = ""

    if request.method == "POST":
        selected_location = request.form.get("location")

        if selected_location:
            # Get current time in the location's time zone
            timezone = pytz.timezone(LOCATION_TIMEZONES[selected_location])
            current_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

            # Call Weatherstack API for the selected location
            url = f"http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={selected_location}"
            response = requests.get(url)
            data = response.json()
            
            # Process API response
            if response.status_code == 200 and "current" in data:
                temperature = data["current"]["temperature"]
                weather_descriptions = ", ".join(data["current"]["weather_descriptions"])
                weather_icon_url = data["current"]["weather_icons"][0] # Extract weather icon URL

                weather_result = (
                    f"The weather in {selected_location} is {weather_descriptions} with a temperature of {temperature}°C. "
                    f"Current time: {current_time}."
                )
            else:
                error_message = data.get("error", {}).get("info", "Unable to fetch weather data.")
                weather_result = f"Error fetching weather for {selected_location}: {error_message}"

    # Render HTML with the dropdown menu
    html_template = """
    <!doctype html>
    <html>
    <head>
        <title>Calvin's Weather Project</title>
    </head>
    <body>
        <h1>Hello Everyone, Welcome to Weather Information</h1>
        <form method="POST">
            <label for="location">Choose a location:</label>
            <select name="location" id="location">
                {% for location in locations %}
                <option value="{{ location }}" {% if location == selected_location %}selected{% endif %}>{{ location }}</option>
                {% endfor %}
            </select>
            <button type="submit">Get Weather</button>
        </form>
        <p>{{ weather_result }}</p>
        {% if weather_icon_url %}
        <img src="{{ weather_icon_url }}" alt="Weather Icon">
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(
        html_template,
        locations=locations,
        selected_location=selected_location,
        weather_result=weather_result,
        weather_icon_url=weather_icon_url
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)