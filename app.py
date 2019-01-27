from flask import Flask, render_template, redirect, url_for, request, Response
from flask import make_response
import os.path
import requests as r
import cv2
from queries import get_satellite_image, get_area
from classification import image_segmentation
from solarpanel import solarPanel
import base64

def image_to_string(image):
	_, buffer = cv2.imencode('.png', image)
	str_buffer = str(base64.b64encode(buffer))[2:-1]
	return str_buffer

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title = 'Beam')

@app.route("/index")
def index():
    return render_template("index.html", title = 'Beam')

@app.route('/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        address = request.form['address']

        satellite = get_satellite_image(address)
        satellite_buffer = image_to_string(satellite)

        roof_image, area_percent = image_segmentation(satellite)
        total_area, latitude, longitude = get_area(address)
        area_in_square_meters = total_area*area_percent
        roof_buffer = image_to_string(roof_image)

        solar_panel = solarPanel(address, latitude, longitude, 0.25*area_in_square_meters)
        mean_light_intensity = solar_panel.meanLightIntensity
        monthly_savings = solar_panel.monthlySaving

        response = make_response('{"address" : "' + address + '", "satellite" : "' + satellite_buffer + '", "roof" : "' + roof_buffer + \
            '", "area" : "' + "%.2f" % area_in_square_meters + '", "mean_light_intensity" : "' +  "%.2f" % mean_light_intensity + \
            '", "monthly_savings" : "' + "%.2f" % monthly_savings + '"}')
        
        response.headers['Content-Type'] = "application/json"
        return response

if __name__ == "__main__":
    app.run(debug = True)