import serial
import time
import numpy as np

com_port = 'COM4'
baud_rate = 115200
serial_delay = 0.001

def setup(port, baud):
    global ser
    while True:
        try:
            ser=serial.Serial(port,baud, timeout=1)
            return
        except:
            pass

def sendString(input,waitTime):
    try:
        for x in input:
            ser.write(bytes(x,'utf-8'))
            # ser.write("%s"%(x).encode())
            time.sleep(waitTime)
    except:
        print('error with sending string')

def readString():
    line = ""
    while True:
        char = ser.read().decode('utf-8')
        if char == '\n':
            return line
        line += char

def updateMotors(motorVelocities):
    data_to_send = ','.join(map(str, motorVelocities)) + '\n'
    sendString(com_port, baud_rate, data_to_send, serial_delay)
    encoder_values = readString()
    



def main():
    pass

if __name__ == '__main__':
    setup()
    main()
