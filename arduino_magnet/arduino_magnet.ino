//define pins, pin values & serial monitor strings

String MAGNET_ON = "Magnet ON";
String MAGNET_OFF = "Magnet OFF";

int MAGNET_PIN = 2;
int magnet_val;

//the setup function runs once when you press rest or power to board
void setup(){
    //initialize MAGNET_PIN as an output
    pinMode(MAGNET_PIN, OUTPUT);

    //start the serial monitor
    Serial.begin(9600);
}

//the loop functions runs over and over again forever
void loop(){
    //read magnet pin input
    magnet_val = digitalRead(MAGNET_PIN);

    //check to see if arduino has recieved any messages & respond accordingly
    if(Serial.available() > 0)
    {
        //read in request
        String message = Serial.readString();
        message.trim(); //get rid of any whitespace at end of string

        //turn magnet on or off depending on message

        if(message == MAGNET_ON)
        {
            digitalWrite(MAGNET_PIN,HIGH); //turn the electromagnet on (HIGH Is the voltage level)   
        }
        else if(message == MAGNET_OFF)
        {
            digitalWrite(MAGNET_PIN,LOW); //turn the electromagent off by making the voltage LOQ
        }
    }

    
    // send messages to the PC indicating status of the magnet
    if(magnet_val == HIGH)
    {
        Serial.println(MAGNET_ON);
    }
    else
    {
        Serial.println(MAGNET_OFF);
    }
    delay(1000); //delay for 1 second
}
