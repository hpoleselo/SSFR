// Pins for connecting Arduino w/ Motor
int IN1 = 4 ;
int IN2 = 5 ;
int motorSpeed = 3;

//Inicializa Pinos
void setup(){
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(motorSpeed,OUTPUT);
}

void loop(){

  // PWM goes from 0 to 255, 255 is the full Duty Cycle
  
  // Goes forward
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  delay(1000);
  analogWrite(motorSpeed,70);
  delay(6000);
  
  // Stop motors
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
}
