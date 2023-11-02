class motorControl:
    def __init__(self, sendTarget, targetStep1, targetStep2, targetStep3, targetStep4, currentStep1, currentStep2, currentStep3, currentStep4):
        self.sendTarget = sendTarget
        self.targetStep1 = targetStep1
        self.targetStep2 = targetStep2
        self.targetStep3 = targetStep3
        self.targetStep4 = targetStep4
        self.currentStep1 = currentStep1
        self.currentStep2 = currentStep2
        self.currentStep3 = currentStep3
        self.currentStep4 = currentStep4

    def readCurrentSteps(self):
        reading = [0, 0, 0, 0]
        reading[0] = self.currentStep1.value
        reading[1] = self.currentStep2.value
        reading[2] = self.currentStep3.value
        reading[3] = self.currentStep4.value
        return reading

    def writeTargetSteps(self, targetList):
        self.sendTarget.value = True
        self.targetStep1.value = targetList[0]
        self.targetStep2.value = targetList[1]
        self.targetStep3.value = targetList[2]
        self.targetStep4.value = targetList[3]

    def moveForward(self, targetDistance):
        self.targetStep1.value = targetDistance
        self.targetStep2.value = -targetDistance
        self.targetStep3.value = -targetDistance
        self.targetStep4.value = targetDistance

    def moveRight(self, targetDistance):
        self.targetStep1.value = -targetDistance
        self.targetStep2.value = targetDistance
        self.targetStep3.value = -targetDistance
        self.targetStep4.value = targetDistance

    def rotate(self, targetDistance):
        self.targetStep1.value = targetDistance
        self.targetStep2.value = targetDistance
        self.targetStep3.value = targetDistance
        self.targetStep4.value = targetDistance