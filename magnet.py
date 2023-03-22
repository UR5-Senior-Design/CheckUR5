import serial
import time

# send message to turn magnet on
def turnMagnetOn():
    msg = "Magnet ON"
    print(f"Sending message to Arduino: {msg}")
    arduino.write(str.encode(msg))
    
def turnMagnetOff():
    msg = "Magnet OFF"
    print(f"Sending message to Arduino: {msg}")
    arduino.write(str.encode(msg))


# send message to turn magnet off

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=0)
time.sleep(2)

while(True):
    turnMagnetOn()

    time.sleep(5)

    turnMagnetOff()
    
    time.sleep(5)
