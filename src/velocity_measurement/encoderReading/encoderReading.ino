    // Encoder LM393 program
    int D0IN = 2;
    int rpm;
    volatile byte pulses;
    unsigned long timeold;
    // How many holes one complete rotation in our encoder has
    unsigned int pulsesPerRound = 20;
    void counter()
    {
      // Everytime we detect a hole it counts as one pulse, pulses = pulses + 1
      pulses++;
    }
    void setup()
    {
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
    void loop()
    {
      // ACHO QUE DEVEMOS DIIMINUIR PRA SER A CADA MILISEGUNDO MESMO E IR SALVANDO (DIMINUIR PRA 10 OU 1)
      // Updates the counter each second
      // millis() returns the number of milliseconds passed since the Arduino board began running the current program
      if (millis() - timeold >= 1000)
      {
        //Desabilita interrupcao durante o calculo
        detachInterrupt(0);
        // TALVEZ MUDAR A FORMULA
        rpm = (60 * 1000 / pulsesPerRound ) / (millis() - timeold) * pulses;
        timeold = millis();
        pulses = 0;
        // Shows the angular velocity in the serial monitor
        Serial.print("RPM = ");
        Serial.println(rpm, DEC);
        //Habilita interrupcao
        attachInterrupt(0, counter  , FALLING);
      }
    }
