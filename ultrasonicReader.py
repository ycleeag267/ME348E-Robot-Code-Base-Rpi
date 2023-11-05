#Libraries
import RPi.GPIO as GPIO
import time
from func_timeout import FunctionTimedOut, func_timeout

class ultrasonicReader:
    def __init__(self, exit_event, GPIO_TRIGGER, GPIO_ECHO, ultrasonicDistance):
        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.GPIO_ECHO = GPIO_ECHO
        self.ultrasonicDistance = ultrasonicDistance
        self.exit_event = exit_event

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
 
    def readSensor(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def iterateSensor(self):
        while not self.exit_event.is_set():
            try:
                self.ultrasonicDistance.value = func_timeout(0.1, self.readSensor)
                # time.sleep(0.01)
            # possibly delay here to allow for reasonable mutex acquisition
            except FunctionTimedOut:
                print("", end="")
                # print('timeout error')
            except Exception as e:
                print(f"Function raised an exception: {e}")
            except KeyboardInterrupt:
                self.exit_event.set()
        
        GPIO.cleanup()
        print('closing ultrasonic reader gracefully')


