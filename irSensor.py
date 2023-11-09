import time
import numpy as np
import RPi.GPIO as GPIO

class irSensor:
    def __init__(self, sensorPin):
        self.sensorPin = sensorPin
        #sensor1 = 14
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensorPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def readSensor(self):
        ir_value = not GPIO.input(self.sensorPin)
        #returns true if detected, false if ir beacon is not detected
        return ir_value

    def timeRead(self):
        initial_time = time.time()
        while (time.time()-initial_time<1):
            if self.readSensor():
                return True
        return False



			






