from flask import Flask, render_template, Response
import datetime
from time import sleep
from picamera import PiCamera
import RPi.GPIO. as GPIO
app = Flask(__name__)

#SET CAMERA SETTINGS 
camera = PiCamera()
camera.resolution = (1024, 768)
camera.vflip = True

@app.route("/")
def hello():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {
	'title' : 'HELLO!',
	'time' : timeString
	}
	return render_template('main.html', **templateData)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/camera/")
def index_camera():
	"""Video Streaming Home Page"""
	# camera = PiCamera()
	camera.resolution = (1024, 768)
	camera.vflip = True
	# sleep(2)
	camera.capture('static/foo.jpg')
	return render_template('camera.html')


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80, debug=True)