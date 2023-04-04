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
        try:
            self.rtde_c = rtde_control.RTDEControlInterface(robot_ip)
            self.rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
        
            if self.rtde_c.isConnected() and self.rtde_r.isConnected():
                print(f"Robot is connected.")
        except:
            print(f"Robot is not connected")
    
    # clean up when we're done with robot
    def __del__(self):
        print("Destructor for Robot called. Closing Arduino port, disconnecting robot and deleting object.")
        self.arduino.close()
        self.rtde_c.disconnect()
        self.rtde_r.disconnect()
    
    # magnet functions
    # send a message to the arduino
    def sendMsg(self, msg):
        print(f"Sending message to Arduino: {msg}")
        self.arduino.write(str.encode(msg))

    # send message to turn magnet on
    def turnMagnetOn(self):
        msg = "Magnet ON"
        self.sendMsg(msg)
        
        # wait until magnet is on before leaving the function, timeout after 10 seconds
        start = time()
        while True:
            received_msg = self.arduino.readline()
            received_msg.rstrip("\n")
            
            end = time()
            time_elapsed = end-start
            time_elapsed.round(0)
            if received_msg == "Magnet is currently ON" or time_elapsed == 10:
                print(f"Received Arduino message: {received_msg}")
                break;
        
        return
            
    
    # send message to turn magnet off
    def turnMagnetOff(self):
        msg = "Magnet OFF"
        self.sendMsg(msg)
        
        # wait until magnet is on before leaving the function, timeout after 10 seconds
        start = time()
        while True:
            received_msg = self.arduino.readline()
            received_msg.rstrip("\n")
            
            end = time()
            time_elapsed = end-start
            time_elapsed.round(0)
            if received_msg == "Magnet is currently OFF" or time_elapsed == 10:
                print(f"Received Arduino message: {received_msg}")
                break;
        
        return
        
    # movement functions
    # target is a tuple (row, col) designating the square position on the board to move to
    # the position is calculated based on the origin position (0,0)/TOP_LEFT
    # return the base position list [x, y, z, rx, ry, rz] of the target 
    def get_position(self, target):
        X = TOP_LEFT["x"]
        Y = TOP_LEFT["y"]
        Z = TOP_LEFT["z"]
        RadX = TOP_LEFT["rx"]
        RadY = TOP_LEFT["ry"]
        RadZ = TOP_LEFT["rz"]

        if target[0] != 0:
            diff = (target[0]) * MVMT_DIFF
            val = ord("A")
            print(f"X difference: {target[0]}-{val} = {diff}")
            Y += diff
        if target[1] != 0:   
            diff = (target[1]) * MVMT_DIFF
            val = ord("1")
            print(f"Y difference: {target[1]}-{val} = {diff}")
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

    # target is a tuple (row, col) designating the square position on the board to grab the piece
    # go to the target position where robot arm will pick up piece and pick up the piece
    def grab_piece(self, target):
        pos = self.get_position(target)
        
        hover_pos = pos.copy()
        hover_pos[2] += HOVER_DIFF
        
        self.rtde_c.moveL(hover_pos, SPEED, ACCELERATION)
        self.rtde_c.moveL(pos, SPEED, ACCELERATION)
        
        self.check_arrival(pos)
        
        # TURN ON THE MAGNET
        self.turnMagnetOn()
        # TODO: check for whether magnet is actually on instead of doing a delay
        time.sleep(1) # give magnet time to turn on

    # target is a tuple (row, col) designating the square position on the board to drop the piece
    # this function assumes that the robot arm has already picked up a piece/at the grabbed piece position
    # go to the target position where robot arm will drop piece and drop it
    def drop_piece(self, target):
        pos = self.get_position(target)
        
        # assuming robot arm has already grabbed piece
        current_pos = self.rtde_r.getActualTCPPose()
        
        # raise arm up
        hover_pos1 = current_pos.copy()
        hover_pos1[2] += HOVER_DIFF
        
        self.rtde_c.moveL(hover_pos1, SPEED, ACCELERATION)
        
        # hover over target position
        hover_pos2 = pos.copy()
        hover_pos2[2] += HOVER_DIFF
        
        self.rtde_c.moveL(hover_pos2, SPEED, ACCELERATION)
        self.rtde_c.moveL(pos, SPEED, ACCELERATION) # move down to drop piece
        
        self.check_arrival(pos)
        
        # TURN OFF THE MAGNET
        self.turnMagnetOff()
        # TODO: check for whether magnet is actually on instead of doing a delay
        time.sleep(1) # give magnet time to turn off
        
        # go to resting position
        self.rtde_c.moveL(hover_pos2, SPEED, ACCELERATION)
        self.rtde_c.moveL(HOME_POS, SPEED, ACCELERATION)
    
    