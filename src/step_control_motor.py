import RPi.GPIO as GPIO          
from time import sleep

# ---- SETTING UP RASPBERRY PI GPIO PORTS! ----- 
en = 25     # PWM port
enb = 17    # PWM2 port

in1 = 24    # Motor A forward direction control
in2 = 23    # Motor A backwards direction control

# Escolhemos duas GPIOs proximas da do Motor A, aleatorio
inB1 = 22   # Motor B forward direction control
inB2 = 27   # Motor B backwards direction control

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
print("Commands: ah-CCW, s-stop, f-CCW, ho-CW, e-exit")
print("\n")    

# Infinite loop
while(1):
    userInput = raw_input()
    
    if userInput =='ah':
        print("CCW")
        # Motor A 
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        # Motor B
        GPIO.output(inB1,GPIO.HIGH)
        GPIO.output(inB2,GPIO.LOW)
        print("forward")
        userInput ='z'

    elif userInput =='ho':
        print("Robot rotating CW")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        # Motor B
        GPIO.output(inB1,GPIO.LOW)
        GPIO.output(inB2,GPIO.HIGH)
        flag=0
        userInput ='z'        

    elif userInput =='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(inB1,GPIO.LOW)
        GPIO.output(inB2,GPIO.LOW)
        userInput ='z'
    
    elif userInput =='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
