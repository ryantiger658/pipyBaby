import RPi.GPIO as GPIO, Adafruit_DHT as envSensor, time

# Set to "F" to display all temperatures in fahrenheit
temp = "F"

# Set to the pin that the DHT sensor is attatched to
tempAndHumidityPin = 4

# Set to the approprate DHT sensor model number 11 or 22
AdafruitDHTSensor = 22

GPIO.setmode(GPIO.BCM)

def getEnv():
    # Read from the sensor
    humidity, temperature = envSensor.read(AdafruitDHTSensor, tempAndHumidityPin)
    if humidity is None or temp is None:
        humidity = 1000

    while humidity > 100:
        humidity, temperature = envSensor.read(AdafruitDHTSensor, tempAndHumidityPin)
        if humidity is None or temp is None:
            humidity = 1000
        time.sleep(3)

    # If the global temp is set to fahrenheit convert the temp
    if temp == "F":
        temperature = 9.0/5.0 * temperature + 32

    # Put the temp and humdity into an object
    results = {
    'temperature' : round(temperature, 2),
    'humidity' : round(humidity, 2)
    }

    #Access the global env temp
    global initialEnv

    #Update the global temp
    initialEnv = results

    return results