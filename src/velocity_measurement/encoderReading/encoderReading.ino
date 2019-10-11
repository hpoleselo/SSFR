unsigned long start;
const byte encoderPinA = 3;//A pin -> interrupt pin 0
const byte encoderPinB = 4;//B pin -> digital pin 4
volatile long pulse;
volatile bool pinB, pinA, dir;
const byte ppr = 20, upDatesPerSec = 2;
const int fin = 1000 / upDatesPerSec;
const float konstant = 60.0 * upDatesPerSec / (ppr * 2);
int rpm;
double v;


void setup() {
  Serial.begin(9600);
  attachInterrupt(1, readEncoder, CHANGE);
  pinMode(encoderPinA,INPUT_PULLUP);
  pinMode(encoderPinB,INPUT_PULLUP);
}

void loop() {
  if(millis() - start > fin)
  {
    start = millis();
    rpm = pulse * konstant;
    // convert to linear velocity in km/h considering a wheel of diameter 0.0325m
    v= 2*3.1415*(rpm/60.0)*0.0325*3.6;
    
    Serial.println(v,7);
    pulse = 0;
  }
}

void readEncoder()
{
  pinA = bitRead(PIND,encoderPinA);
  pinB = bitRead(PIND,encoderPinB);
  dir = pinA ^ pinB;          // if pinA & pinB are the same
  dir ? --pulse : ++pulse;    // dir is CW, else CCW
}
