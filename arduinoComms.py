import serial
import time
import numpy as np

class arduinoComms:
    def __init__(self, port, baud, motorSpeed1, motorSpeed2, motorSpeed3, motorSpeed4, encoderValue1, encoderValue2, encoderValue3, encoderValue4):
        self.port = port
        self.baud = baud
        self.motorSpeed1 = motorSpeed1
        self.motorSpeed2 = motorSpeed2
        self.motorSpeed3 = motorSpeed3
        self.motorSpeed4 = motorSpeed4
        self.encoderValue1 = encoderValue1
        self.encoderValue2 = encoderValue2
        self.encoderValue3 = encoderValue3
        self.encoderValue4 = encoderValue4

        #declared constants
        self.serial_delay = 0.001
    
    def sendString(self, ser, input):
        try:
            comma_separated_string = ",".join(map(str, input)) + "\n"
            ser.write(comma_separated_string.encode())
        except:
            print('error with sending string')

    def readString(self, ser):
        try:
            response = ser.readline().decode().strip()
            responseList = response.strip().split(',')
            integer_list = [int(element) for element in responseList]
            return integer_list
        except:
            print('error reading string from arduino')
            return [0, 0, 0, 0]

    def updateMotors(self):
        #send motor values
        motorSpeedString = [0, 0, 0, 0]
        motorSpeedString[0]= self.motorSpeed1.value
        motorSpeedString[1]= self.motorSpeed2.value
        motorSpeedString[2]= self.motorSpeed3.value
        motorSpeedString[3]= self.motorSpeed4.value

        for element in motorSpeedString:
            if (element < 0):
                element = 0
            if (element > 255):
                element = 255
        self.sendString(motorSpeedString)

        #read encoder values
        receivedValues = self.readString()
        self.encoderValue1.value = receivedValues[0]
        self.encoderValue2.value = receivedValues[1]
        self.encoderValue3.value = receivedValues[2]
        self.encoderValue4.value = receivedValues[3]

    def maintainCommunications(self):
        ser=serial.Serial(self.port, self.baud, timeout=1)
        print('serial connected')
        
        while True:
            #send motor values
            motorSpeedString = [0, 0, 0, 0]
            motorSpeedString[0]= self.motorSpeed1.value
            motorSpeedString[1]= self.motorSpeed2.value
            motorSpeedString[2]= self.motorSpeed3.value
            motorSpeedString[3]= self.motorSpeed4.value

            for element in motorSpeedString:
                if (element < -255):
                    element = 0
                if (element > 255):
                    element = 255
            self.sendString(ser, motorSpeedString)

            #read encoder values
            receivedValues = self.readString(ser)
            self.encoderValue1.value = receivedValues[0]
            self.encoderValue2.value = receivedValues[1]
            self.encoderValue3.value = receivedValues[2]
            self.encoderValue4.value = receivedValues[3]



        