import serial
import time

def sendMagnetMsg(msg, arduino):
    print(f"Sending message to Arduino: {msg}")
    arduino.write(str.encode(msg))

# send message to turn magnet on
def turnMagnetOn(arduino):
    msg = "Magnet ON"
    sendMagnetMsg(msg, arduino)
    
def turnMagnetOff(arduino):
    msg = "Magnet OFF"
    sendMagnetMsg(msg, arduino)


# send message to turn magnet off

# arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0)
# time.sleep(2)

# while(True):
#     turnMagnetOn(arduino)

#     time.sleep(5)

#     turnMagnetOff(arduino)
    
#     time.sleep(5)
