import rtde_control
import rtde_receive
from magnet import *

TOP_LEFT = { "x": 0.79556, "y": -0.22876, "z": 0.015, "rx": 2.394, "ry": -2.011, "rz": 0.053 }
MVMT_DIFF = 0.06378
HOVER_DIFF = 0.030

speed = 0.1
acceleration = 0.1

RESTING_POS = [0.27206, -0.10977, 0.04678, 2.036, -2.366, 0.012]

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0)
rtde_c = rtde_control.RTDEControlInterface("192.168.1.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.102")

# destination is a string ("A1", "A2", "D6", etc.)
# return the base position list of the coordinate square
def get_position(destination):
    X = TOP_LEFT["x"]
    Y = TOP_LEFT["y"]
    Z = TOP_LEFT["z"]
    RadX = TOP_LEFT["rx"]
    RadY = TOP_LEFT["ry"]
    RadZ = TOP_LEFT["rz"]

    if not destination[0] == "A":
        diff = (ord(destination[0])-ord("A")) * MVMT_DIFF
        val = ord("A")
        print(f"X difference: {ord(destination[0])}-{val} = {diff}")
        Y += diff
    if not destination[1] == "1":   
        diff = (ord(destination[1])-ord("1")) * MVMT_DIFF
        val = ord("1")
        print(f"Y difference: {ord(destination[1])}-{val} = {diff}")
        X -= diff
    
    new_pos = [X, Y, Z, RadX, RadY, RadZ]
    
    return new_pos

# check if the robot arm has arrived to the target position before doing any other actions
def check_arrival(target):
    current_pos = rtde_r.getActualTCPPose()
    error = 0.0040

    while not ((target[0]-error <= current_pos[0] <= target[0]+error)
        and (target[1]-error <= current_pos[1] <= target[1]+error)):
        current_pos = rtde_r.getActualTCPPose()
        print(f"Current Actual TCP Pose: {current_pos}")

# destination/target is a base position list: [x, y, z, rx, ry, rz]
# go to the target position where robot arm will pick up piece
def grab_piece(target):
    hover_pos = target.copy()
    hover_pos[2] += HOVER_DIFF
    
    rtde_c.moveL(hover_pos, speed, acceleration)
    rtde_c.moveL(target, speed, acceleration)
    
    check_arrival(target)
    
    # TURN ON THE MAGNET
    turnMagnetOn(arduino)
    time.sleep(1) # give magnet time to turn on

# go to the target position where robot arm will drop piece
def drop_piece(target):
    current_pos = rtde_r.getActualTCPPose()
    
    hover_pos1 = current_pos.copy()
    hover_pos1[2] += HOVER_DIFF
    
    rtde_c.moveL(hover_pos1, speed, acceleration)
    
    hover_pos2 = target.copy()
    hover_pos2[2] += HOVER_DIFF
    
    rtde_c.moveL(hover_pos2, speed, acceleration)
    rtde_c.moveL(target, speed, acceleration)
    
    check_arrival(target)
    
    # TURN OFF THE MAGNET
    turnMagnetOff(arduino)
    time.sleep(1) # give magnet time to turn off
    
    # go to resting position
    rtde_c.moveL(hover_pos2, speed, acceleration)
    rtde_c.moveL(RESTING_POS, speed, acceleration)
    
def main():
    position1 = get_position("B1")
    position2 = get_position("F7")
    
    grab_piece(position1)
    drop_piece(position2)

main()