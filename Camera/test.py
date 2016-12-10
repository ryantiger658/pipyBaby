from picamera import PiCamera
from time import sleep

camera = PiCamera()

# camera.resolution = (1024, 768)
camera.vflip = True

# camera.start_preview()

# Camera warm-up time
sleep(2)

camera.capture('foo.jpg')
sleep(2)
camera.start_recording('video.h264')
sleep(5)
camera.stop_recording()