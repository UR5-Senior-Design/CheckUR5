import serial
import time
import rtde_control
import rtde_receive

RESTING_POS = [0.23953, -0.09013, 0.02582, 1.819, -1.931, -0.440]

rtde_c = rtde_control.RTDEControlInterface("192.168.1.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.102")

# open communication with Arduino
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=0)
time.sleep(2)

if rtde_c.isConnected():
    print("RTDE is connected.")

    speed = 0.1
    acceleration = 0.1
    
    current_pos = rtde_r.getActualTCPPose()
    print(f"Current Actual TCP Pose: {current_pos}")
    
    # move to the first test position and turn magnet on
    base_pos1 = [0.79257, -0.03927, 0.00673, 2.155, -2.305, 0.066]
    print(f"Moving to base position {base_pos1}")
    rtde_c.moveL(base_pos1, speed, acceleration)

    # TODO: check if robot arm has reached its destination instead of using sleep
    # checking if robot arm has reached its destination yet
    # while current_pos != base_pos1:
    #     current_pos = rtde_r.getActualTCPPose()
    #     print(f"Current Actual TCP Pose: {current_pos}")
    time.sleep(5)

    target_wp = rtde_c.getTargetWaypoint()
    print(f"Target Waypoint: {target_wp}")
    print(f"Finished moving.")
    
    msg = "Magnet ON"
    print(f"Sending message to Arduino: {msg}")
    arduino.write(str.encode(msg))
    
    # TODO: Check for a message from Arduino that the magnet is now ON
    time.sleep(2)
    
    # move to next position and turn magnet off
    base_pos2 = [0.60454, -0.10426, 0.00854, 2.051, -2.374, 0.026]
    print(f"Moving to base position {base_pos2}")
    rtde_c.moveL(base_pos2, speed, acceleration)
    
    # while current_pos != base_pos2:
    #     current_pos = rtde_r.getActualTCPPose()
    #     print(f"Current Actual TCP Pose: {current_pos}")
    time.sleep(5)
    
    print(f"Finished moving.")
        
    msg = "Magnet OFF"
    print(f"Sending message to Arduino: {msg}")
    arduino.write(str.encode(msg))
    
    # TODO: Check for a message from Arduino that the magnet is now OFF
    time.sleep(2)
    
    # go back to resting position to finish turn
    print(f"Moving to resting position {RESTING_POS}")
    rtde_c.moveL(RESTING_POS, speed, acceleration)
    
    # while current_pos != RESTING_POS:
    #     current_pos = rtde_r.getActualTCPPose()
    #     print(f"Current Actual TCP Pose: {current_pos}")
    time.sleep(5)
        
    print(f"Finished moving.")
    print(f"Finished turn.")
else:
    print("RTDE is not connected.")

rtde_c.stopScript()