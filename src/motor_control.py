import RPi.GPIO as GPIO          
from time import sleep

# Motor A forward direction control
in1 = 24
# Motor A backwards direction control
in2 = 23
# PWM Port
en = 25
temp1=1

# Escolhemos duas GPIOs proximas da do Motor A, aleatorio
# Motor B forward direction control
inB1 = 22
# Motor B backwards direction control
inB2 = 27

GPIO.setmode(GPIO.BCM)
# Set the ports to control the motor's direction as output
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)

# PWM is output
GPIO.setup(en,GPIO.OUT)

# By default the motor should not run
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

# Setting MotorB's ports
GPIO.setup(inB1,GPIO.OUT)
GPIO.setup(inB2,GPIO.OUT)

# By default the motor should not run
GPIO.output(inB1,GPIO.LOW)
GPIO.output(inB2,GPIO.LOW)

# PWM on port 25 wich 1000Hz of frequency
pwm = GPIO.PWM(en,1000)

# Starts PWM with 25%
pwm.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

# Infinite loop
while(1):
    x = raw_input()
    
    if x=='r':
        print("Running motor A")
        if (temp1==1):
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
        print("Running MotorB")
        if (temp1==1):
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
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        # teste
        GPIO.output(inB1,GPIO.HIGH)
        GPIO.output(inB2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        # teste
        GPIO.output(inB1,GPIO.LOW)
        GPIO.output(inB2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        pwm.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        pwm.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        pwm.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
