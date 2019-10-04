import RPi.GPIO as GPIO          
from time import sleep

flag=1

# ---- SETTING UP RASPBERRY PI GPIO PORTS! ----- 
en = 25     # PWM port
enb = 17    # PWM2 port

in1 = 24    # Motor A forward direction control
in2 = 23    # Motor A backwards direction control

# Escolhemos duas GPIOs proximas da do Motor A
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

# PWM on port 25 with 1000Hz of frequency
pwm = GPIO.PWM(en,1000)
pwm2 = GPIO.PWM(enb,1000)

# Starts PWM with 25%
pwm.start(25)
pwm2.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

# Infinite loop
while(1):
    x = raw_input()
    
    if x=='r':
        print("Running Motor A")
        if (flag==1):
            # Motor goes forward
            GPIO.output(in1,GPIO.HIGH)
            # We must set then the other direction to low
            GPIO.output(in2,GPIO.LOW)
            print("forward")
            x='z'
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("backward")
            x='z'

    # Adicionei isso pro segundo motor
    elif x=='r2':
        print("Running Motor B")
        if (flag==1):
            # Motor goes forward
            GPIO.output(inB1,GPIO.HIGH)
            # We must set then the other direction to low
            GPIO.output(inB2,GPIO.LOW)
            print("forward motorB")
            x='z'
        else:
            GPIO.output(inB1,GPIO.LOW)
            GPIO.output(inB2,GPIO.HIGH)
            print("backward motor B")
            x='z'

    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(inB1,GPIO.LOW)
        GPIO.output(inB2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        # teste
        GPIO.output(inB1,GPIO.HIGH)
        GPIO.output(inB2,GPIO.LOW)
        flag=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        # teste
        GPIO.output(inB1,GPIO.LOW)
        GPIO.output(inB2,GPIO.HIGH)
        flag=0
        x='z'

    elif x=='m':
        print("medium")
        pwm.ChangeDutyCycle(50)
        pwm2.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        pwm.ChangeDutyCycle(75)
        pwm2.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
