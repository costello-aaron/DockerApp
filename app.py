from flask import Flask, request, render_template
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)
num_days = 7
#region TEMPERATURE CONVERSION
@app.template_filter('to_celsius')
def to_celsius(f):
    try:
        return round((f - 32) * 5/9)
    except TypeError:
        return 'N/A'
#endregion

def get_coordinates_from_city(city_name):
    """
    Gets latitude and longitude  from a city name using Nominatim geocoding service
    """
    try:
        # Nominatim geocoding service
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': city_name,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'WeatherApp/1.0'  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None
            
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None



@app.route("/", methods=["GET", "POST"])
def index():
    """
    Converts city name into coordinates.
    Processes the weather data for the given city.
    Returns the weather data to the index.html template.
    """
    weather = None
    weekly_weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            # Get coordinates from city name
            lat, lon = get_coordinates_from_city(city)
            
            if lat is not None and lon is not None:
                try:
                    point_resp = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
                    point_resp.raise_for_status()
                    forecast_url = point_resp.json()["properties"]["forecast"]

                    forecast_resp = requests.get(forecast_url)
                    forecast_resp.raise_for_status()
                    forecast_data = forecast_resp.json()
                    periods = forecast_data["properties"]["periods"]

                    weather = periods[0]  # Get today's forecast
                    weekly_weather = generate_weekly_weather_report(forecast_data)
                except Exception as e:
                    error = str(e)
            else:
                error = f"Could not locate coordinates for {city}"
        else:
            error = "Please enter a city name"

    return render_template("index.html", weather=weather, weekly_weather=weekly_weather, error=error, city=city if request.method == "POST" else None)

def generate_weekly_weather_report(forecast_data):
    """
   Gernerate weekly weather report from the forecast data
   Returns a list of daily forecasts for the next 7 days.
    """
    weekly_report = []
    
    if not forecast_data or "properties" not in forecast_data or "periods" not in forecast_data["properties"]:
        return weekly_report
    
    periods = forecast_data["properties"]["periods"]
    
    # Group periods by day and create daily summaries
    daily_forecasts = {}
    
    for period in periods:
        # Extract date from the startTime
        start_time = datetime.fromisoformat(period["startTime"].replace("Z", "+00:00"))
        date_key = start_time.date()
        
        if date_key not in daily_forecasts:
            daily_forecasts[date_key] = {
                "date": date_key,
                "day_name": start_time.strftime("%A"),
                "day_periods": []
            }
        
        daily_forecasts[date_key]["day_periods"].append(period)
    
    # Convert to list and sort by date
    sorted_days = sorted(daily_forecasts.keys())
    
    # Get next number of days
    for i, date_key in enumerate(sorted_days[:num_days]):
        day_data = daily_forecasts[date_key]
        
        # Creates summary for the day
        day_summary = {
            "date": day_data["date"],
            "day_name": day_data["day_name"],
            "periods": day_data["day_periods"],
            "high_temp": None,
            "low_temp": None
        }
        
        # Extract temperature from periods
        for period in day_data["day_periods"]:
            if "temperature" in period:
                temp = period["temperature"]
                if period.get("isDaytime", True):  # Daytime 
                    if day_summary["high_temp"] is None or temp > day_summary["high_temp"]:
                        day_summary["high_temp"] = temp
                else:  # Nighttime 
                    if day_summary["low_temp"] is None or temp < day_summary["low_temp"]:
                        day_summary["low_temp"] = temp
        
        weekly_report.append(day_summary)
    
    return weekly_report
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

