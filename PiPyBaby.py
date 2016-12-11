#!/usr/bin/env python
from flask import Flask, render_template, Response
from camera_pi import Camera
from picamera import PiCamera
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Direct URL of the video stream"""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/readPin/<pin>")
def readPin(pin):

    GPIO.setup(int(pin), GPIO.OUT)
    if GPIO.input(int(pin)) == True:
        response = "Pin number " + pin + " is high!"
        GPIO.output(int(pin), GPIO.LOW)
    else:
        response = "Pin number " + pin + " is low!"
        GPIO.output(int(pin), GPIO.HIGH)


    templateData = {
    'title' : 'Status of pin ' + pin,
    'response' : response
    }
    return render_template('pin.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)