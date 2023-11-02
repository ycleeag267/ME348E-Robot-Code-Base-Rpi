import multiprocessing
import time
from arduinoComms import arduinoComms
from motorControl import motorControl
from ultrasonicReader import ultrasonicReader

def inputSimulator(motorController, ultrasonicSensor):
    initialTime = time.time()

    while True: 
        if (time.time()-initialTime>3):
            #motorController.writeTargetSteps([1000, 1000, 1000, 1000])
            motorController.moveRight (1000)
            initialTime = time.time()

        readings = motorController.readCurrentSteps()
        print(f'current steps: {readings[0]}, {readings[1]}, {readings[2]}, {readings[3]}')
        # print(f'ultrasonic distance reading: {ultrasonicSensor.value}')
        time.sleep(1)

if __name__ == "__main__":
    #declaring serial variables
    # port = 'COM4'   #For PC
    port = '/dev/ttyACM3'   #For Rpi
    baud_rate = 115200

    #declaring sensor variables
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24

    #declaring multiprocessing variables
    sendTarget = multiprocessing.Value('i', False)
    targetStep1 = multiprocessing.Value('i', 0)
    targetStep2 = multiprocessing.Value('i', 0)
    targetStep3 = multiprocessing.Value('i', 0)
    targetStep4 = multiprocessing.Value('i', 0)
    currentStep1 = multiprocessing.Value('i', 0)
    currentStep2 = multiprocessing.Value('i', 0)
    currentStep3 = multiprocessing.Value('i', 0)
    currentStep4 = multiprocessing.Value('i', 0)
    ultrasonicDistance = multiprocessing.Value('d', 9999)

    #declare class objects
    arduinoCommunication = arduinoComms(port, baud_rate, sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, currentStep1, currentStep2, currentStep3, currentStep4)
    motorController = motorControl(sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, currentStep1, currentStep2, currentStep3, currentStep4)
    # ultrasonicSensor = ultrasonicReader(GPIO_TRIGGER, GPIO_ECHO, ultrasonicDistance)

    process1 = multiprocessing.Process(target=arduinoCommunication.maintainCommunications)
    process2 = multiprocessing.Process(target=inputSimulator, args= (motorController, ultrasonicDistance))
    # process3 = multiprocessing.Process(target=ultrasonicSensor.iterateSensor)
    
    process1.start()
    process2.start()
    # process3.start()

    process1.join()
    process2.join()
    # process3.join()