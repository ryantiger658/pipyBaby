#!/usr/bin/python
import time
import Adafruit_DHT

envPin = 4

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, envPin)

    temperature = 9.0/5.0 * temperature + 32

    print 'Temp: {0:0.1f} F  Humidity: {1:0.1f} %'.format(temperature, humidity)
    time.sleep(5)