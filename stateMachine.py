import time
import numpy as np

class stateMachine:
    def __init__(self, exit_event, motorcontroller, ultrasonicDistance):
        self.exit_event = exit_event
        self.motorcontroller = motorcontroller
        self.ultrasonicDistance = ultrasonicDistance
        self.current_state = 0

        #define the list of 
        self.states = [self.findbackwall, self.moveforward, self.stopMachine]

    def testSensor(self):
        while True:
            print(self.ultrasonicDistance.value)
            time.sleep(0.01)

    def averageDistance(self):
        read_values=[]
        standard_deviation = 5
        while True:
            reading = self.ultrasonicDistance.value
            if not (reading in read_values):
                read_values.append(reading)
            if len(read_values)>= 3:
                if np.std(read_values)<standard_deviation:
                    return(np.mean(read_values))
                else:
                    read_values=[]

    def findbackwall(self):
        print('in back wall')
        exitflag = True
        best_distance = 999
        current_distance = 999
        current_position = 0
        best_position = 0
        step_size = 100
        check_steps = 1600
        rotate_steps = 750
        while exitflag:
            self.motorcontroller.rotate(step_size)
            current_position += step_size
            # while self.motorcontroller.moving():
            #     pass
            time.sleep(1.25)
            #check if new position is better 
            current_distance = self.averageDistance()
            print(f'current position: {current_position}, current distance: {current_distance}')
            if current_distance<best_distance:
                best_distance = current_distance
                best_position = current_position
                print(f'new best position is {best_position} and new best distance is {best_distance}')

            #exit condition
            if (current_position >= check_steps):
                exitflag = False
        
        print(f'best position is {best_position} and best distance is {best_distance}')

        #rotate to the best location
        self.motorcontroller.rotate(-(current_position-best_position))
        #blocks for the moving to stop
        time.sleep(5)
        self.motorcontroller.rotate(rotate_steps)
        time.sleep(5)

        #set state to next module
        self.current_state = 1

    def moveforward(self):
        #move back to square bot
        self.motorcontroller.moveRight(400)
        time.sleep(1.5)

        #move forward 
        self.motorcontroller.moveRight(-1600)
        time.sleep(4)

        #square up with corner
        self.motorcontroller.moveForward(800)
        time.sleep(2)

        #set state to end
        self.current_state = -1
    
    def stopMachine(self):
        print("in stop machine")
        self.exit_event.set()

    def statetransition(self):
        try:
            current_state_function = self.states[self.current_state]
            current_state_function()
        except KeyboardInterrupt:
            self.exit_event.set()

    def iteratestates(self):
        while not self.exit_event.is_set():
            try:
                self.statetransition()
            except KeyboardInterrupt:
                self.exit_event.set()
        print('state machine exited gracefully')
        
