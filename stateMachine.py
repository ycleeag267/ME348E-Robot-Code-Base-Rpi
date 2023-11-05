class stateMachine:
    def __init__(self, exit_event, motorcontroller, ultrasonicsensor):
        self.exit_event = exit_event
        self.motorcontroller = motorcontroller
        self.ultrasonicsensor = ultrasonicsensor
        self.current_state = 0

        #define the list of 
        self.states = [self.findbackwall, self.stopMachine]

    def findbackwall(self):
        exitflag = True
        best_distance = 999
        current_distance = 999
        current_position = 0
        best_position = 0
        step_size = 10
        check_steps = 5000
        while exitflag:
            self.motorcontroller.rotate(step_size)
            current_position += step_size
            while self.motorcontroller.moving():
                pass

            #check if new position is better 
            current_distance = self.ultrasonicsensor.value
            if current_position<best_distance:
                best_distance = current_distance
                best_position = current_position

            #exit condition
            if (current_position >= check_steps):
                exitflag = False
        
        #rotate to the best location
        self.motorcontroller.rotate(-(current_position-best_position))
        #blocks for the moving to stop
        while self.motorcontroller.moving():
            pass

        #set state to end
        self.current_state = -1
    
    def stopMachine(self):
        self.exit_event.set()

    def statetransition(self):
        current_state_function = self.states[self.current_state]
        current_state_function()

    def iteratestates(self):
        while not self.exit_event.is_set():
            try:
                self.statetransition()
            except KeyboardInterrupt:
                self.exit_event.set()
        print('state machine exited gracefully')
        
