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
  while (millis() <= 100000) {
        // Sample time
        if (millis() - timeold >= 50) {
          // Disables Interrupt while doing calculation
          detachInterrupt(0);
          
          // pulses eh sempre 1, serve como uma flag pra indicar que ta passando pelo buraco
          rpm = ((60 * 1000 / pulsesPerRound ) / (millis() - timeold)) * pulses;
          actual_time = millis();
          // convert to angular velocity to feed the model
          phi = (3.1416*rpm)/30;
          
          // Print in the csv format
          Serial.print(actual_time);
          Serial.print(",");
          Serial.println(phi, DEC);      
          
          timeold = millis();
          pulses = 0;
          
          attachInterrupt(0, counter  , FALLING);

          // Start spinning the wheels
          analogWrite(motorSpeed,70);
        }
  }
}
