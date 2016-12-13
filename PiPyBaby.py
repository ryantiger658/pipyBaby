#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify
from camera_pi import Camera
from picamera import PiCamera
import RPi.GPIO as GPIO
import Adafruit_DHT as envSensor
import json
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Set to "F" to display all temperatures in fahrenheit
temp = "F"

# Set to the pin that the DHT sensor is attatched to
tempAndHumidityPin = 4

# Set to the approprate DHT sensor model number
AdafruitDHTSensor = 11


# Video streaming generator function.
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Get the current ambient enviroment 
def getEnv():
    # Read from the sensor
    humidity, temperature = envSensor.read_retry(AdafruitDHTSensor, tempAndHumidityPin)

    # If the global temp is set to fahrenheit convert the temp
    if temp == "F":
        temperature = 9.0/5.0 * temperature + 32

    # Put the temp and humdity into an object
    results = {
    'temperature' : temperature,
    'humidity' : humidity
    }
    return(results)

initialEnv = getEnv()

"""BEGIN FLASK PAGE DEFINITIONS"""

@app.route('/')
def index():
    """Video streaming home page."""
    templateData = initialEnv
    return render_template('index.html', **initialEnv)

@app.route('/video_feed')
def video_feed():
    """Direct URL of the video stream"""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/env')
def readTempAndHumidity():
    #  Read the temp and humidity from the sensor
    env = getEnv()

    # Convert the data to JSON
    env = json.dumps(env)

    # Output the JSON data to the page
    resp = Response(response=env,
    status=200, \
    mimetype="application/json")
    return(resp)

# @app.route("/readPin/<pin>")
# def readPin(pin):

#     GPIO.setup(int(pin), GPIO.OUT)
#     if GPIO.input(int(pin)) == True:
#         response = "Pin number " + pin + " is high!"
#         GPIO.output(int(pin), GPIO.LOW)
#     else:
#         response = "Pin number " + pin + " is low!"
#         GPIO.output(int(pin), GPIO.HIGH)


#     templateData = {
#     'title' : 'Status of pin ' + pin,
#     'response' : response
#     }
#     return render_template('pin.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)