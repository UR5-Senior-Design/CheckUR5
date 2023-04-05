# Note: moveL pose vector based on from "base" XYZ, RX, RY, RZ values on pendant IN METERS

# Team CheckUR5
# CSE 4316-007 Senior Design I
# Sprint 4 - December 5, 2022

import rtde_control
import rtde_receive

rtde_c = rtde_control.RTDEControlInterface("192.168.1.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.102")

if rtde_c.isConnected():
    print("RTDE is connected.")

    speed = 0.1
    acceleration = 0.1
    # base_pos1 = [519.10, 52.02, 257.72, 1.910, -2.4, -0.236]
    # base_pos2 = [600.95, 86.19, 82.49, 2.107, -2.429, -0.031]
    base_pos1 = [0.56857, 0.14334, 0.17938, 2.777, -1.485, 0.099]
    base_pos2 = [0.61225, 0.12859, 0.05207, 2.733, -1.509, 0.022]
    base_pos3 = [-0.143, -0.435, 0.20, -0.001, 3.12, 0.04]
    # joint_pos1 = [-176.57, -68.28, 103.59, -128.61, -90.98, -29.86]
    # joint_pos2 = [-178.21, -52.48, 100.35, -135.94, -90.98, -29.86]
    
    print(f"Moving to base position {base_pos1}")
    rtde_c.moveL(base_pos1, speed, acceleration)
    print(f"Moving to base position {base_pos2}")
    rtde_c.moveL(base_pos2, speed, acceleration)

    # rtde_c.moveJ(joint_pos1, speed, acceleration)

    actual_pos = rtde_r.getActualTCPPose()
    print(f"Actual TCP Pose: {actual_pos}")

    target_wp = rtde_c.getTargetWaypoint()
    print(f"Target Waypoint: {target_wp}")

    print(f"Finished moving.")
else:
    print("RTDE is not connected.")

rtde_c.stopScript()