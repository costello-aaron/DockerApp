from flask import Flask, request, render_template
import python_weather
import requests

import asyncio

app = Flask(__name__)

@app.template_filter('to_celsius')
def to_celsius(f):
    try:
        return round((f - 32) * 5/9)
    except TypeError:
        return 'N/A'

async def get_weather(city):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        return weather
    
def get_weather_sync(city):
    return asyncio.run(get_weather(city))

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city = None

    if request.method == "POST":
        city = request.form.get("city")

        try:
            weather = get_weather_sync(city)

        except Exception as e:
            error = str(e)

    return render_template("index.html", weather=weather, city=city, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

