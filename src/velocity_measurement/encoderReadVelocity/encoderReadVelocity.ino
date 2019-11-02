    // Encoder LM393 program
    int D0IN = 2;
    float rpm;
    volatile byte pulses;
    unsigned long timeold;
    unsigned long actual_time;

    // filter variables
    int filter_samples = 1;
    int filter_counter;
    float new_rpm;
    float average;
    float phi;
    
    // How many holes one complete rotation in our encoder has
    unsigned int pulsesPerRound = 20;

    // ISR
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

      // initialization
      filter_counter = 0;
      new_rpm = 0;
      
    }
    void loop()
    {
      // millis() returns the number of milliseconds passed since the Arduino board began running the current program
      while (millis() <= 100000)
          {
    	      if (millis() - timeold >= 40)
    	      {
        		//Desabilita interrupcao durante o calculo
        		detachInterrupt(0);
        		// pulses eh sempre 1, serve como uma flag pra indicar que ta passando pelo buraco
        		rpm = ((60 * 1000 / pulsesPerRound ) / (millis() - timeold)) * pulses;
        		
        		// moving average filter
        		new_rpm = rpm + new_rpm;
        		filter_counter++;
        		if (filter_counter == filter_samples) {
                // get actual time
        		    actual_time = millis();
        		    average = new_rpm/filter_samples;
                // convert to angular velocity to feed the model
                phi = (3.1416*average)/30;
                // Print in the csv format
        		    Serial.print(actual_time);
        		    Serial.print(",");
        		    Serial.println(phi, DEC);
                // Setting the sum to 0
        		    filter_counter = 0;
        		    new_rpm = 0;
        		}        
        		
        		timeold = millis();
        		pulses = 0;
        		
        		//Habilita interrupcao
        		attachInterrupt(0, counter  , FALLING);
    	      }
      }
    }
