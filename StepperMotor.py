class StepperMotor:
    'Input the motor pins'
    def __init__(self, motorPins=[0, 0, 0, 0]):
        import RPi.GPIO as GPIO
        import time as time
        from time import sleep as sleep
        import math as math

        # Libs
        self.GPIO = GPIO
        self.time = time
        self.sleep = sleep
        self.math = math

        # Hardware
        self.GPIO.setmode(GPIO.BOARD)
        self.motorPins = motorPins
        for i in motorPins:
            GPIO.setup(i, GPIO.OUT)

        # Vars
        self.direction = True   # True Forward | False Backward
        self.anglePosition = 0
        self.defaultDelay = 0.001
        self.sequences = [
            [1, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 0]
        ]

    def jumpTo(self, destinationAngle, direction=1):
        destinationAngle = destinationAngle%360
        selisih = destinationAngle - self.anglePosition
        if direction==1:
            self.forward(selisih%360)
        elif direction==0:
            self.backward(abs(selisih)%360)
        
    'Rotate motor forward'    
    def forward(self, rotateAngle):
        if(rotateAngle<0):
            self.backward(abs(rotateAngle))
            return
        print('Rotating forward for', rotateAngle)
        stepNum = self.getStepByAngle(rotateAngle)
        for i in range(self.anglePosition, self.anglePosition+stepNum):
            for x in range(len(self.motorPins)):
                self.GPIO.output(self.motorPins[x], self.sequences[i%8][x])
            self.sleep(self.defaultDelay)
        self.anglePosition+=rotateAngle
        self.anglePosition = self.anglePosition%360

    'Rotate motor backward'
    def backward(self, rotateAngle):
        if(rotateAngle<0):
            self.forward(abs(rotateAngle))
            return
        print('Rotating backward for', rotateAngle)
        stepNum = self.getStepByAngle(rotateAngle)
        for i in range(self.anglePosition, self.anglePosition-stepNum, -1):
            for x in range(len(self.motorPins)):
                self.GPIO.output(self.motorPins[x], self.sequences[i%8][x])
            self.sleep(self.defaultDelay)
        self.anglePosition -= rotateAngle
        self.anglePosition = self.anglePosition%360
    
    def motorSleep(self):
        for x in range(len(self.motorPins)):
            self.GPIO.output(self.motorPins[x], 0)

    def getStepByAngle(self, angle):
        return int((angle/360)*400)

    def setSpeed(self, speedAPM):
        if(speedAPM <= 0):
            print("Min speed is", 0, "rotation per minute")
            return
        if(speedAPM > 360*200):
            print("Max speed is", 360*200, "rotation per minute")
            return
        print("Set speed to ", speedAPM/360, "rotation per minute")
        aps = speedAPM/60   # 1/s
        a = (aps/360)*400   # step/s
        t = 1/a             # perioda
        self.defaultDelay = t