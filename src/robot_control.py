import RPi.GPIO as GPIO
import sys
import rospy
import pidcontroller
import pi_aruco_interface
import threading
from time import sleep
from geometry_msgs.msg import Point

class SSFR(object):
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
        GPIO.setup(self.in1,GPIO.OUT)    # Forward
        GPIO.setup(self.in2,GPIO.OUT)    # Backwards

        # Motor B, setting the ports to control the direction of the motor
        GPIO.setup(self.inB1,GPIO.OUT)   # Forward
        GPIO.setup(self.inB2,GPIO.OUT)   # Backwards

        # PWM is output
        GPIO.setup(en,GPIO.OUT)
        GPIO.setup(enb,GPIO.OUT)

        # By default none of the motors should run
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.inB1,GPIO.LOW)
        GPIO.output(self.inB2,GPIO.LOW)

        # PWM on port 25 and 17 with 1000Hz of frequency
        pwm = GPIO.PWM(en,1000)
        pwm2 = GPIO.PWM(enb,1000)

        # On our experiment we will be working around 60% of the PWM, i.e 4.5V applied to the motors
        pwm.start(30)
        pwm2.start(30)

        # Retrieve the messages over ROS from the position
        #rospy.init_node("aruco_receiver")

        self.pid = pidcontroller.PID(200,300,0)
        self.ArucoInstance = pi_aruco_interface.ArucoInterface()
        self.t = threading.Thread(target=self.ArucoInstance.track_aruco(),args=("Thread sendo executada",))

        self.main()

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
        print("[INFO]: GPIO Clean up")
        sys.exit()

    def positionCallback(self, position):
        """ Retrieves the ArUco position over ROS """
        return position.x, position.z

    def testMotors(self):
        self.rotateClockwise()
        sleep(5)
        self.rotateCounterClockWise()
        sleep(5)
        self.stopMotors()
        sleep(1)
        self.cleanPorts()

    def pegarPosX(self):
        """ Inicia a thread , i.e a obtencao da posicao"""
        self.t.start()
        self.ArucoInstance.x

    def followMarker(self):
        """ Pre test function to check if the PID will work. """
        self.pegarPosX()
        while True:
            actual_position = 0
            new_position = self.ArucoInstance.x
            erro = abs(new_position)
            if erro > 0.01:
                if new_position < 0:
                    self.rotateCounterClockWise()
                    while erro > 0.01:
                        new_position = x
                        erro = abs(new_position)
                    self.stopMotors
                if new_position > 0:
                    self.rotateClockwise()
                    while erro > 0.01:
                        new_position = x
                        erro = abs(new_position)
                    self.stopMotors

    def positionControl(self, x):
        targetPosition = 0
        try:
            while True:
                currentPosition = self.readMarkerX()tele
                error = targetPosition - currentPosition
                correction = self.pid.Update(error)
                if error > 0:
                    self.rotateCounterClockWise()
                    pwm(correction)
                elif error < 0:
                    self.rotateClockwise()
        except(KeyboardInterrupt):
            self.stopMotors()
            self.cleanPorts()
            sys.exit()
        
    def main(self):
        """ Runs the wished method. """
        self.followMarker()
        
SSFR()


