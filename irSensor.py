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

    def averageRead(self):
        truth_state = 0
        samples = 50
        for i in range(samples):
            time.sleep(0.01)
            truth_state += self.readSensor()

        # truth_state = round(truth_state/samples)
        truth_state = truth_state/samples
        return truth_state



			






