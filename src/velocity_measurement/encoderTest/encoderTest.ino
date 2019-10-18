    // This program just tests the encoder, in our case the disk has 20 holes, so when
    // our counter has counted 20 it has be 1 turn. That's why we marked the disk with
    // something to be our reference when knowing when the disk has a complete turn.
    
    int D0IN = 3;
    int encoderReading;
    int counter = 0 ;
    int old_state = 0;
 
    void setup()
    {
      Serial.begin(9600);
      // retrieving the readings from the sensor
      pinMode(D0IN, INPUT);
    }
    
    void loop()
    {   
        encoderReading = digitalRead(D0IN);
        if (encoderReading != old_state) {
          counter = counter + 1;
          Serial.println(counter);
          // Since we want to check the TRANSITION we have to hold the state and count only when...
          // Meaning we're actually getting double the readings in order to get one full turn, so we should divide that by two
          old_state = encoderReading;
          if (counter == 20) {
            Serial.println("One turn");
            counter = 0;
          }
        }


        delay(5);
    }
