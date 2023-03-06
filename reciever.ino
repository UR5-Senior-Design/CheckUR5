const String MAGNET_ON = "Magnet ON"
const String MAGNET_OFF = "Magnet OFF"

void setup(){
    //
    //get from existing Arduino code
    Serial.begin(9600)
}

void loop(){
    
    //check to see if arduino has recieved any messages & respond accordingly
    if(Serial.available() > 0)
    {
        //read in request
        String message = Serial.readString();
        message.trim(); //get rid of any whitespace at end of string

        //turn magnet on or off depending on message
        switch(message)
        {
            case MAGNET_ON:
                digitalWrite(pin,HIGH);
                break;
            case MAGNET_OFF:
                digitialWrite(pin,LOW)
        }

    }
}
