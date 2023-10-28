import multiprocessing
import time
from arduinoComms import arduinoComms
from motorControl import motorControl

def inputSimulator(motorController):
    initialTime = time.time()

    while True: 
        if (time.time()-initialTime>3):
            motorController.writeTargetSteps([5000, 5000, 5000, 5000])
            initialTime = time.time()

        readings = motorController.readCurrentSteps()
        print(f'current steps: {readings[0]}, {readings[1]}, {readings[2]}, {readings[3]}')
        time.sleep(0.5)

if __name__ == "__main__":
    #declaring serial variables
    port = 'COM4'
    baud_rate = 115200
    
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

    #declare class objects
    arduinoCommunication = arduinoComms(port, baud_rate, sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, currentStep1, currentStep2, currentStep3, currentStep4)
    motorController = motorControl(sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, currentStep1, currentStep2, currentStep3, currentStep4)

    process1 = multiprocessing.Process(target=arduinoCommunication.maintainCommunications)
    process2 = multiprocessing.Process(target=inputSimulator, args= (motorController,))
    
    process1.start()
    process2.start()

    process1.join()
    process2.join()