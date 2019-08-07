import RPi.GPIO as GPIO
import time


def controlMotor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)

    # PWM to control the speed of the DC motors
    # PWM(channel, frequency)
    pwm = GPIO.PWM(7,207)
    pwm2 = GPIO.PWM(11,50)

    # Setting the initial dc level of the duty cycle as 0
    pwm.start(0)
    pwm2.start(0)


    try:
        while True:
            # -- One direction --
            # Duty cycle increases to speed up the motor
            for i in range(100):
                # ChangeDutyCycle(dc) which dc varies from 0 to 100
                pwm.ChangeDutyCycle(i)
                time.sleep(0.02)
            # Duty cycle increases to slow down the motor
            for i in range(100):
                pwm.ChangeDutyCycle(100-i)
                time.sleep(0.02)

            pwm.ChangeDutyCycle(0)
            
            # -- Another direction --
            for in range(100):
                pwm2.ChangeDutyCycle(i)
                time.sleep(0.02)
            for in range(100):
                pwm2.ChangeDutyCycle(100-i)
                time.sleep(0.02)
            pwm2.ChangeDutyCycle(0)


    except(KeyboardInterrupt):
        pass
    pwm.stop()
    GPIO.cleanup()

controlMotor()