/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/

//define pins and pin values
int MAGNET_PIN = 2;
int magnet_val;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(MAGNET_PIN, OUTPUT);

  // start the serial monitor
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  // read magnet pin input
  magnet_val = digitalRead(MAGNET_PIN);

  //turn on the magnet if it's off
  if(magnet_val == LOW)
  {
    digitalWrite(MAGNET_PIN, HIGH);   // turn the electromagnet on (HIGH is the voltage level)
    Serial.println("Magnet is ON");
  }
  else
  {
    digitalWrite(MAGNET_PIN, LOW); // turn the electromagnet off by making the voltage LOW
    Serial.println("Magnet is OFF");
  }

  delay(5000);                       // wait for 5 seconds
}
