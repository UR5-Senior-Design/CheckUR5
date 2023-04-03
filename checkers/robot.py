import rtde_control
import rtde_receive
import serial
import time

TOP_LEFT = { "x": 0.79556, "y": -0.22876, "z": 0.015, "rx": 2.394, "ry": -2.011, "rz": 0.053 } # position of A1 square
    
MVMT_DIFF = 0.06378 # the distance between the center points of each square
HOVER_DIFF = 0.030 # the difference in z axis to hover over a piece

HOME_POS = (0.20425, -0.13615, 0.03746, 1.848, -2.428, 0.086) # robot arm resting/home position
BOX_POS = (0.23268, 0.20282, 0.09428, 2.930, -0.969, 0.018) # collection box position for robot arm to drop pieces to

# robot arm speed and acceleration
SPEED = 0.1
ACCELERATION = 0.1

# a robot class that you can create to handle all movements of the robot for the checkers game and also the magnet/arduino communications
# robot arm positions for this class is based off of the Base position
class Robot:    
    def __init__(self, arduino_port='/dev/ttyUSB0', robot_ip="192.168.1.102"):
        # arduino to control the magnet
        self.arduino = serial.Serial(port=arduino_port, baudrate=9600, timeout=0)
        
        # UR5 robot arm interface for controlling and receiving robot arm information
        self.rtde_c = rtde_control.RTDEControlInterface(robot_ip)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
    
    # magnet functions
    # send a message to the arduino
    def sendMsg(self, msg):
        print(f"Sending message to Arduino: {msg}")
        self.arduino.write(str.encode(msg))

    # send message to turn magnet on
    def turnMagnetOn(self):
        msg = "Magnet ON"
        self.sendMsg(msg)
    
    # send message to turn magnet off
    def turnMagnetOff(self):
        msg = "Magnet OFF"
        self.sendMsg(msg)
        
    # movement functions
    # destination is a string ("A1", "A2", "D6", etc.)
    # return the base position list of the coordinate square
    def get_position(self, destination):
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
    def check_arrival(self, target):
        current_pos = self.rtde_r.getActualTCPPose()
        error = 0.0040

        while not ((target[0]-error <= current_pos[0] <= target[0]+error)
            and (target[1]-error <= current_pos[1] <= target[1]+error)):
            current_pos = self.rtde_r.getActualTCPPose()
            print(f"Current Actual TCP Pose: {current_pos}")

        return

    # destination/target is a base position list: [x, y, z, rx, ry, rz]
    # go to the target position where robot arm will pick up piece
    def grab_piece(self, target):
        hover_pos = target.copy()
        hover_pos[2] += HOVER_DIFF
        
        self.rtde_c.moveL(hover_pos, SPEED, ACCELERATION)
        self.rtde_c.moveL(target, SPEED, ACCELERATION)
        
        self.check_arrival(self, target)
        
        # TURN ON THE MAGNET
        self.turnMagnetOn()
        # TODO: check for whether magnet is actually on instead of doing a delay
        time.sleep(1) # give magnet time to turn on

    # go to the target position where robot arm will drop piece
    def drop_piece(self, target):
        current_pos = self.rtde_r.getActualTCPPose()
        
        hover_pos1 = current_pos.copy()
        hover_pos1[2] += HOVER_DIFF
        
        self.rtde_c.moveL(hover_pos1, SPEED, ACCELERATION)
        
        hover_pos2 = target.copy()
        hover_pos2[2] += HOVER_DIFF
        
        self.rtde_c.moveL(hover_pos2, SPEED, ACCELERATION)
        self.rtde_c.moveL(target, SPEED, ACCELERATION)
        
        self.check_arrival(target)
        
        # TURN OFF THE MAGNET
        self.turnMagnetOff()
        # TODO: check for whether magnet is actually on instead of doing a delay
        time.sleep(1) # give magnet time to turn off
        
        # go to resting position
        self.rtde_c.moveL(hover_pos2, SPEED, ACCELERATION)
        self.rtde_c.moveL(HOME_POS, SPEED, ACCELERATION)
    
    