import multiprocessing
import time
from arduinoComms import arduinoComms
from motorControl import motorControl
from ultrasonicReader import ultrasonicReader
from stateMachine import stateMachine
#import LoadShoot class
from LoadShoot import LoadShoot

def inputSimulator(motorController, ultrasonicDistance, exit_event):
    # initialTime = time.time()
    initialTime = 0

    while not exit_event.is_set(): 
        try:
            if (time.time()-initialTime>1):
                # motorController.writeTargetSteps([10, 10, 10, 10])
                # chosenSpeed = input("enter desired turn distance: ")
                motorController.rotate(10)
                initialTime = time.time()

            readings = motorController.readCurrentSteps()
            # print(f'current steps: {readings[0]}, {readings[1]}, {readings[2]}, {readings[3]} at {time.time()-initialTime}')
            # print(f'ultrasonic distance reading: {ultrasonicDistance.value}')
            time.sleep(1)
        except KeyboardInterrupt:
            exit_event.set()

    print("closing input simulator gracefully")

if __name__ == "__main__":
    #declaring serial variables
    # port = 'COM4'   #For PC
    port = '/dev/ttyACM0'   #For Rpi
    baud_rate = 115200

    #declaring sensor variables
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24

    #declaring multiprocessing variables
    exit_event = multiprocessing.Event()
    sendTarget = multiprocessing.Value('i', False)
    targetStep1 = multiprocessing.Value('i', 0)
    targetStep2 = multiprocessing.Value('i', 0)
    targetStep3 = multiprocessing.Value('i', 0)
    targetStep4 = multiprocessing.Value('i', 0)
    #shooting command variable. sent as 1 when shooting one puck. 
    #will shoot and load next puck, ensuring next puck ready to fire
    ShootCommand = multiprocessing.Value('i', 0)
    currentStep1 = multiprocessing.Value('i', 0)
    currentStep2 = multiprocessing.Value('i', 0)
    currentStep3 = multiprocessing.Value('i', 0)
    currentStep4 = multiprocessing.Value('i', 0)
    ultrasonicDistance = multiprocessing.Value('d', 9999)

    #declare class objects
    arduinoCommunication = arduinoComms(port, baud_rate, exit_event, sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, ShootCommand, currentStep1, currentStep2, currentStep3, currentStep4)
    motorController = motorControl(sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, currentStep1, currentStep2, currentStep3, currentStep4)
    #declare loading and shooting object
    LoadShooter = LoadShoot(ShootCommand)
    ultrasonicSensor = ultrasonicReader(exit_event, GPIO_TRIGGER, GPIO_ECHO, ultrasonicDistance)
    decisionMaking = stateMachine(exit_event, motorController, ultrasonicDistance, LoadShooter)

    process1 = multiprocessing.Process(target=arduinoCommunication.maintainCommunications)
    process2 = multiprocessing.Process(target=ultrasonicSensor.iterateSensor)
    process3 = multiprocessing.Process(target=decisionMaking.iteratestates)
    # process3 = multiprocessing.Process(target=inputSimulator, args=[motorController, ultrasonicDistance, exit_event])

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()