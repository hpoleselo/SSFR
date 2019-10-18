    // Encoder LM393 program
    int D0IN = 3;
    float rpm;
    volatile byte pulses;
    unsigned long timeold;
    unsigned long actual_time;

    // filter variables
    int filter_samples = 5;
    int filter_counter;
    float new_rpm;
    float average;
    
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
      if (millis() - timeold >= 1000)
      {
        //Desabilita interrupcao durante o calculo
        detachInterrupt(0);
        // pulses eh sempre 1, serve como uma flag pra indicar que ta passando pelo buraco
        rpm = ((60 * 1000 / pulsesPerRound ) / (millis() - timeold)) * pulses;
        // filtro media movel
        new_rpm = rpm + new_rpm;
        filter_counter++;
        if (filter_counter == filter_samples) {
            Serial.print("Dentro do if New RPM:");
            Serial.println(new_rpm);
            average = new_rpm/5.0;
            // adicionar atraso de 5 amostras, pegar tempo aqui
            Serial.print("RPM Filtrado:");
            Serial.println(new_rpm, DEC);
            filter_counter = 0;
            new_rpm = 0;
        }        
        timeold = millis();
        // pode tirar e deixar so com o timeold, usamos pra plotar o grafico
        actual_time = millis();
        pulses = 0;
        
        // Shows the angular velocity in the serial monitor
        Serial.print("New RPM dps dos milli:");
        Serial.println(new_rpm);
        
        //Serial.print("RPM = ");
        //Serial.println(rpm, DEC);
        //Habilita interrupcao
        attachInterrupt(0, counter  , FALLING);
      }
    }
