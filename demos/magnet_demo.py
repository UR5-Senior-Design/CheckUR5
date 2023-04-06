# Note: moveL pose vector based on from "base" XYZ, RX, RY, RZ values on pendant IN METERS

import serial
import time
import rtde_control
import rtde_receive
from magnet import *


RESTING_POS = [0.27206, -0.10977, 0.04678, 2.036, -2.366, 0.012]

rtde_c = rtde_control.RTDEControlInterface("192.168.1.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.102")

# open communication with Arduino
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0)
time.sleep(2)

if rtde_c.isConnected():
    print("RTDE is connected.")

    speed = 0.1
    acceleration = 0.1
    
    current_pos = rtde_r.getActualTCPPose()
    print(f"Current Actual TCP Pose: {current_pos}")
    
    # move to the first test position and turn magnet on
    base_pos1 = [0.66451, -0.03888, 0.01947, 2.156, -2.260, 0.023]
    print(f"Moving to base position {base_pos1}")
    rtde_c.moveL(base_pos1, speed, acceleration)

    # TODO: check if robot arm has reached its destination instead of using sleep
    # checking if robot arm has reached its destination yet
    target = base_pos1
    error = 0.0040
    
    while not ((target[0]-error <= current_pos[0] <= target[0]+error)
            and (target[1]-error <= current_pos[1] <= target[1]+error)):
            current_pos = rtde_r.getActualTCPPose()
            print(f"Current Actual TCP Pose: {current_pos}")
    #time.sleep(5)

    target_wp = rtde_c.getTargetWaypoint()
    print(f"Target Waypoint: {target_wp}")
    print(f"Finished moving.")
    
    turnMagnetOn(arduino)
    
    # TODO: Check for a message from Arduino that the magnet is now ON
    time.sleep(2)
    
    # lift up
    base_pos1[2] += 0.030
    rtde_c.moveL(base_pos1, speed, acceleration)
    
    # move to next position and turn magnet off
    base_pos2 = [0.79251, -0.1617, 0.02093, 1.951, -2.439, 0.027]
    print(f"Moving to base position {base_pos2}")
    rtde_c.moveL(base_pos2, speed, acceleration)
    
    target = base_pos2
    
    while not ((target[0]-error <= current_pos[0] <= target[0]+error)
        and (target[1]-error <= current_pos[1] <= target[1]+error)):
        current_pos = rtde_r.getActualTCPPose()
        print(f"Current Actual TCP Pose: {current_pos}")
    #time.sleep(5)
    
    current_pos = rtde_r.getActualTCPPose()
    print(f"Current Actual TCP Pose: {current_pos}")
    
    print(f"Finished moving.")
        
    turnMagnetOff(arduino)
    
    # TODO: Check for a message from Arduino that the magnet is now OFF
    time.sleep(2)
    
    # go back to resting position to finish turn
    print(f"Moving to resting position {RESTING_POS}")
    rtde_c.moveL(RESTING_POS, speed, acceleration)
    
    
    current_pos = rtde_r.getActualTCPPose()
    print(f"Current Actual TCP Pose: {current_pos}")
        
    print(f"Finished moving.")
    print(f"Finished turn.")
else:
    print("RTDE is not connected.")

rtde_c.stopScript()