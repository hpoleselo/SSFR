// Code from PID: https://gist.github.com/ivanseidel/b1693a3be7bb38ff3b63
// Creating the PID as an object to be instantiated on our main code
class PID{
public:
  
  double error;
  double sample;
  double lastSample;
  double kP, kI, kD;      
  double P, I, D;
  double pid;
  
  double setPoint;
  long lastProcess;
  
  PID(double _kP, double _kI, double _kD){
    kP = _kP;
    kI = _kI;
    kD = _kD;
  }

  // Add new sample is basically reading from the sensor the variable, in our case the velocity
  void addNewSample(double _sample){
    sample = _sample;
  }

  // Gets new variable
  void setSetPoint(double _setPoint){
    setPoint = _setPoint;
  }
  
  double process(){
    // Implementação P ID
    error = setPoint - sample;
    float deltaTime = (millis() - lastProcess) / 1000.0;
    lastProcess = millis();
    
    //P
    P = error * kP;
    
    //I
    I = I + (error * kI) * deltaTime;
    
    //D
    D = (lastSample - sample) * kD / deltaTime;
    lastSample = sample;
    
    // Soma tudo
    pid = P + I + D;
    
    return pid;
  }
};

// This is the value of the PWM we used to retrieve the experimental curve, is the point where we want to operate
const float steadyStatePWM = 120.0;

// Variable used to send the signal from the PID to our actuator, in this case, the motor.
float controlPWM = 0;

// Pins for connecting Arduino w/ Motor
int IN1 = 4 ;
int IN2 = 5 ;
int motorSpeed = 3;
int D0IN = 2; // Encoder pin

// Variables to calculate the velocity
int rpm;
volatile byte pulses;
unsigned long timeold;
unsigned long actual_time;
float phi;
unsigned int pulsesPerRound = 20;   // How many holes one complete rotation in our encoder has
int sampleTime = 50;                // In miliseconds

// Gains of the PID Controller
double Kp = 10.0, Ki = 1.0, Kd = 1.0;

// Instantiating our PID controller
PID SpeedPidControl(Kp,Ki,Kd);

// ISR
void counter()
{
  // Everytime we detect a hole it counts as one pulse, pulses = pulses + 1
  pulses++;
  
}

void setup(){
    pinMode(IN1,OUTPUT);
    pinMode(IN2,OUTPUT);
    pinMode(motorSpeed,OUTPUT);

    // Sets up the motor to go forward by default
    digitalWrite(IN1,HIGH);
    digitalWrite(IN2,LOW);
  
    Serial.begin(9600);
    // The pin has be our input since we're reading the pulses from the sensor
    pinMode(D0IN, INPUT);
    //Interrupcao 0 - pino digital 2
    // Everytime the interrupt is triggered (borda de descida) we call the counter
    attachInterrupt(0, counter, FALLING);
    pulses = 0;
    rpm = 0;
    timeold = 0;
}

void loop(){

  // PWM goes from 0 to 255, 255 is the full Duty Cycle

  // millis() returns the number of milliseconds passed since the Arduino board began running the current program
  while (millis() <= 15000) {
        // Sample time is set to
        if (millis() - timeold >= sampleTime) {
          // Disables Interrupt while doing calculation
          detachInterrupt(0);

          // Pulses is always 1 because we set it to 0 in the end of the code, it is like a flag that we're detecting something
          // otherwise it will not calculate the speed of the wheel
          rpm = ((60 * 1000 / pulsesPerRound ) / (millis() - timeold)) * pulses;
          actual_time = millis();
          // convert to angular velocity to feed the model
          phi = (3.1416*rpm)/30;
          
          // Pass the read variable to the PID controller
          SpeedPidControl.addNewSample(phi);

          // PID signal control to our actuator, calculates the error and so on
          controlPWM = (SpeedPidControl.process() + steadyStatePWM);

          // If our PID controller tries to subceed the minimum to rotate the motor...
          if (controlPWM < 60) {
            //Serial.println("Tentou colocar menos no motor");
            controlPWM = 60;
          }
          
          // If our PID controller tries to surpass the limit
          else if (controlPWM > 255) {
            //Serial.println("Tentou colocar mais no motor");
            controlPWM = 255;
          }
          
          
          // Print in the csv format
          Serial.print(actual_time);
          Serial.print(",");
          Serial.println(phi, DEC);      
          
          timeold = millis();
          pulses = 0;
          
          attachInterrupt(0, counter  , FALLING);

          // Actuate on motor based on the output from the PID
          analogWrite(motorSpeed,controlPWM);
        }
  }
}
