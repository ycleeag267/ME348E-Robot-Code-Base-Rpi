import multiprocessing
import time
from arduinoComms import arduinoComms

def inputSimulator(motorSpeed1, motorSpeed2, motorSpeed3, motorSpeed4, encoderValue1, encoderValue2, encoderValue3, encoderValue4):
    while True: 
        motorSpeed1.value = - motorSpeed1.value
        motorSpeed2.value = - motorSpeed2.value
        motorSpeed3.value = - motorSpeed3.value
        motorSpeed4.value = - motorSpeed4.value

        print(f'motor speeds: {motorSpeed1.value}, {motorSpeed2.value}, {motorSpeed3.value}, {motorSpeed4.value}')

        print(f'encoder readings: {encoderValue1.value}, {encoderValue2.value}, {encoderValue3.value}, {encoderValue4.value}')
        time.sleep(1)

if __name__ == "__main__":
    #declaring serial variables
    port = 'COM4'
    baud_rate = 115200
    
    #declaring multiprocessing variables
    motorSpeed1 = multiprocessing.Value('i', 150)
    motorSpeed2 = multiprocessing.Value('i', 150)
    motorSpeed3 = multiprocessing.Value('i', 150)
    motorSpeed4 = multiprocessing.Value('i', 150)
    encoderValue1 = multiprocessing.Value('l', 0)
    encoderValue2 = multiprocessing.Value('l', 0)
    encoderValue3 = multiprocessing.Value('l', 0)
    encoderValue4 = multiprocessing.Value('l', 0)

    #declare class objects
    arduinoCommunication = arduinoComms(port, baud_rate, motorSpeed1, motorSpeed2, motorSpeed3, motorSpeed4, encoderValue1, encoderValue2, encoderValue3, encoderValue4)

    process1 = multiprocessing.Process(target=arduinoCommunication.maintainCommunications)
    process2 = multiprocessing.Process(target=inputSimulator, args= (motorSpeed1, motorSpeed2, motorSpeed3, motorSpeed4, encoderValue1, encoderValue2, encoderValue3, encoderValue4))
    
    process1.start()
    process2.start()

    process1.join()
    process2.join()