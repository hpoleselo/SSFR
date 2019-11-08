import RPi.GPIO as GPIO
import sys
import rospy
import pidcontroller
import threading
import csv
#import pi_aruco_interface
from time import sleep, time
from geometry_msgs.msg import Point

class FollowerRobot(object):
    def __init__(self, use_ros=True):
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
        pwm.start(80)
        pwm2.start(80)
        print("[INFO]: --- Initialized motors from the Robot ---")

        self.pid = pidcontroller.PID(200,300,0)

        # Setting the class variables to be 0 at start and then they will be updated as long the subscriber retrieves them
        self.x = 0
        self.z = 0

        if use_ros:
        # Retrieve the messages over ROS from the position
            rospy.init_node("aruco_receiver")
            self.positionSubscriber = rospy.Subscriber("marker_position", Point, self.positionCallback)
            print("[INFO]: --- Retrieving position from ArUco Marker! ---")

        # [Caso fosse usar Thread] Initializing the Thread
        if use_ros != True:
            self.ArucoInstance = pi_aruco_interface.ArucoInterface()
            # The problem with the thread is because the opening of the camera is concurrent
            self.t = threading.Thread(target=self.ArucoInstance.track_aruco,args=("Thread sendo executada",))

        #self.runTest()
        self.modelIdentification()

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

    def goForward(self):
        print("[INFO]: Robot going forward")
        # Motor A
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        # Motor B
        GPIO.output(self.inB1,GPIO.HIGH)
        GPIO.output(self.inB2,GPIO.LOW)

    def goBackwards(self):
        print("[INFO]: Robot going backwards")
        # Motor A
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        # Motor B
        GPIO.output(self.inB1,GPIO.LOW)
        GPIO.output(self.inB2,GPIO.HIGH)
    
    def rotateLeftWheelBackwards(self):
        print("[INFO]: Rotating only the left wheel backwards")
        # Motor A 
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        # Motor B
        GPIO.output(self.inB1,GPIO.LOW)
        GPIO.output(self.inB2,GPIO.LOW)

    def rotateLeftWheelForward(self):
        print("[INFO]: Rotating only the left wheel forward")
        # Motor A 
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        # Motor B
        GPIO.output(self.inB1,GPIO.LOW)
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

    def testMotors(self):
        self.rotateClockwise()
        sleep(5)
        self.rotateCounterClockWise()
        sleep(5)
        self.stopMotors()
        sleep(1)
        self.cleanPorts()

    def pegarPosXCThread(self):
        """ [HALTED] Inicia a thread , i.e a obtencao da posicao"""
        self.t.daemon = True
        self.t.start()
        print(self.ArucoInstance.x)

    def positionCallback(self, position):
        """ Retrieves the ArUco position over ROS """
        self.x = position.x
        self.z = position.z

    def saveMeasurement(self, n, t, x, z):
        n = str(n)
        file = "measurement" + n + ".csv"
        with open(file, mode='w') as measurement:
            measurement = csv.writer(measurement, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            measurement.writerow(['t', 'x', 'z'])
            for i in range(len(t)):
                measurement.writerow([t[i],x[i],z[i]])

    def followMarker(self):
        """ Pre test function to check if the PID will work. """
        #TODO: Testar pra stop os motores e clean no ctrl+c, ver exemplo do pi aruco interface pois este funciona
        try:
            while True:
                if self.x < -0.05:
                    self.rotateClockwise()
                elif self.x > 0.05:
                    self.rotateCounterClockWise()
                """
                erro = abs(self.x)
                if erro > 0.01:
                    if self.x < -0.05:
                        self.rotateCounterClockWise()
                        while erro > 0.01:
                            new_position = self.x
                            erro = abs(new_position)
                        self.stopMotors
                    if self.x > 0.08:
                        self.rotateClockwise()
                        while erro > 0.01:
                            new_position = self.x
                            erro = abs(new_position)
                        self.stopMotors
                    """
        except(KeyboardInterrupt):
            self.stopMotors
            self.cleanPorts()

    def positionControl(self, x):
        targetPosition = 0
        try:
            while True:
                currentPosition = self.readMarkerX()
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
        
    def modelIdentification(self):
        t = []
        x = []
        z = []
        print("[INFO]: Moving the robot in 3s...")
        sleep(3)
        t_end = time() + 2.5
        self.goForward()
        while time() < t_end:
            # a camera tem 30 fps, estimou-se que no max pegaremos 30 amostras de posicao por segundo
            # entao o delay no sleep eh baseado nisso, 0.025 em um intervalo de 1.5s gera 60 amostras
            t.append(time())
            x.append(self.x)
            z.append(self.z)
            sleep(0.025)
        print("Points retrieved:"), len(t)
        # Measurement number
        n = 1
        self.saveMeasurement(n,t,x,z)
        self.stopMotors()
        self.cleanPorts()
        
    def runTest(self):
        #self.rotateLeftWheelBackwards()
        #self.rotateLeftWheelForward()
        self.goForward()
        sleep(1)
        self.stopMotors()
        self.cleanPorts()

def run():
    robot = FollowerRobot()

if __name__ == "__main__":
    run()


