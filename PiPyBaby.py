#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify
from camera_pi import Camera
from env import getEnv 
import json

app = Flask(__name__)

# Get the current ambient enviroment 
initialEnv = getEnv()

# Video streaming generator function.
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



"""BEGIN FLASK PAGE DEFINITIONS"""

"""Index Page"""
@app.route('/')
def index():
    templateData = initialEnv
    return render_template('index.html', **initialEnv)

"""Full Screen Video"""
@app.route('/fullScreen')
def fullScreenVideo():
    return render_template('fullScreenVideo.html')

"""Direct URL of the video stream"""
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

"""DHT Envriomental Sensor Page"""
@app.route('/env')
def readTempAndHumidity():
    # Convert the data to JSON
    getEnv()
    env = json.dumps(initialEnv)

    # Output the JSON data to the page
    resp = Response(response=env,
    status=200, \
    mimetype="application/json")
    return(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)