import RPi.GPIO as GPIO
import sys
import pi_aruco_interface          
from time import sleep

class SSFRController(object):
    def __init__(self):
        """ This init function sets the Raspberry ports to control the H-Bridge and initializes the ArUco interface """
        en = 25     # PWM port
        enb = 17    # PWM2 port

        self.in1 = 24    # Motor A forward direction control
        self.in2 = 23    # Motor A backwards direction control

        # Escolhemos duas GPIOs proximas da do Motor A, aleatorio
        self.inB1 = 22   # Motor B forward direction control
        self.inB2 = 27   # Motor B backwards direction control

        # Mode of refering to the ports from Raspberry
        GPIO.setmode(GPIO.BCM)

        # Motor A, setting the ports to control the direction of the motor
        GPIO.setup(in1,GPIO.OUT)    # Forward
        GPIO.setup(in2,GPIO.OUT)    # Backwards

        # Motor B, setting the ports to control the direction of the motor
        GPIO.setup(inB1,GPIO.OUT)   # Forward
        GPIO.setup(inB2,GPIO.OUT)   # Backwards

        # PWM is output
        GPIO.setup(en,GPIO.OUT)
        GPIO.setup(enb,GPIO.OUT)

        # By default none of the motors should run
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(inB1,GPIO.LOW)
        GPIO.output(inB2,GPIO.LOW)

        # PWM on port 25 and 17 with 1000Hz of frequency
        pwm = GPIO.PWM(en,1000)
        pwm2 = GPIO.PWM(enb,1000)

        # On our experiment we will be working around 60% of the PWM, i.e 4.5V applied to the motors
        pwm.start(60)
        pwm2.start(60)

        self.aruco_interface = pi_aruco_interface.ArucoInterface()

        self.firstRun()

    def rotateClockwise(self):
        print("[INFO]: Rotating CW")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        # Motor B
        GPIO.output(self.inB1,GPIO.LOW)
        GPIO.output(self.inB2,GPIO.HIGH)

    def rotateCounterClockWise(self):
        print("[INFO]: Rotating CCW")
        # Motor A 
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        # Motor B
        GPIO.output(self.inB1,GPIO.HIGH)
        GPIO.output(self.inB2,GPIO.LOW)

    def stopMotors(self):
        print("[INFO]: Stopping both motors")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.inB1,GPIO.LOW)
        GPIO.output(self.inB2,GPIO.LOW)

    def cleanPorts(self):
        GPIO.cleanup()
        print("GPIO Clean up")
        sys.exit()

    def testMotors(self):
        self.rotateClockwise()
        sleep(5)
        self.rotateCounterClockWise()
        sleep(5)
        self.stopMotors()
        sleep(1)
        self.cleanPorts()

    def readMarkerX(self):
        self.aruco_interface.track_aruco()
        # x_value = self.aruco_interface.track_aruco()
        #return x

    def positionControl(self):
        while True:
            x = self.readMarkerX()
            if x < 0:
                self.rotateCounterClockWise()
            elif x > 0:
                self.rotateClockwise()

        



    def firstRun(self):
        self.testMotors()
    
        



