import rtde_control
import rtde_receive

TOP_LEFT = { "x": 0.79556, "y": -0.22876, "z": 0.018, "rx": 2.394, "ry": -2.011, "rz": 0.053 }
MVMT_DIFF = 0.06378
HOVER_DIFF = 0.030

RESTING_POS = [0.27206, -0.10977, 0.04678, 2.036, -2.366, 0.012]

rtde_c = rtde_control.RTDEControlInterface("192.168.1.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.102")

# destination is a string ("A1", "A2", "D6", etc.)
def getCoordinates(destination):
    Letter = TOP_LEFT["x"]
    Number = TOP_LEFT["y"]
    Z = TOP_LEFT["z"]
    RadX = TOP_LEFT["rx"]
    RadY = TOP_LEFT["ry"]
    RadZ = TOP_LEFT["rz"]

    if not destination[0] == "A":
        Letter = (ord(destination[0])-ord("A")) * MVMT_DIFF
    if not destination[1] == "1":   
        Number = (ord(destination[1])-ord("1")) * MVMT_DIFF
    
    new_pos = [Letter, Number, Z, RadX, RadY, RadZ]
    
    return new_pos

def checkArrival(target):
    current_pos = rtde_r.getActualTCPPose()
    error = 0.0040

    while not ((target[0]-error <= current_pos[0] <= target[0]+error)
        and (target[1]-error <= current_pos[1] <= target[1]+error)):
        current_pos = rtde_r.getActualTCPPose()
        print(f"Current Actual TCP Pose: {current_pos}")

# destination is a base position list: [x, y, z, rx, ry, rz]
def grabPiece(target):
    hover_pos = target.copy()
    hover_pos[2] += HOVER_DIFF
    
    rtde_c.moveL(hover_pos)
    rtde_c.moveL(target)
    
    checkArrival(target)
    
    # TODO: TURN ON THE MAGNET

def dropPiece(destination):
    current_pos = rtde_r.getActualTCPPose()
    
    hover_pos1 = current_pos.copy()
    hover_pos1[2] += HOVER_DIFF
    
    rtde_c.moveL(hover_pos1)
    
    hover_pos2 = destination.copy()
    hover_pos2[2] += HOVER_DIFF
    
    rtde_c.moveL(hover_pos2)
    rtde_c.moveL(destination)
    
    checkArrival(destination)
    
    # TODO: TURN OFF THE MAGNET
    
    # go to resting position
    rtde_c.moveL(hover_pos2)
    rtde_c.moveL(RESTING_POS)