from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        try:
            point_resp = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
            point_resp.raise_for_status()
            forecast_url = point_resp.json()["properties"]["forecast"]

            forecast_resp = requests.get(forecast_url)
            forecast_resp.raise_for_status()
            periods = forecast_resp.json()["properties"]["periods"]

            weather = periods[0]  # Get today's forecast
        except Exception as e:
            error = str(e)

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

