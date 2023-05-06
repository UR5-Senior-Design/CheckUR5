# CheckUR5
## About
A Senior Design project that allows the UR5 collaborative robot arm to play a game of checkers with a human player.

Team CheckUR5:
Nimita Uprety
Patricia Rojas
Hoang Ho
Joanna Huynh
Kevin Vu

## Requirements
### Physical Items
- UR5 collaborative robot arm
- Intel RealSense Depth Camera D435i
- 21 in x 21 in checkerboard
  - 0.5 in border on each side
  - 2.5 in x 2.5 in squares
- 24 (MEASUREMENT HERE) checker pieces
- Electromagnet gripper
  - Electromagnet circuit with Arduino Nano and MOSFET module
  - See ()[./arduino_magnet/arduino_magnet.ino] for the Arduino code
- Checker piece collection box

### Dependencies
- Linux distribution Ubuntu 22.04 LTS
- Python 3.x, we used 3.10.6
- OpenCV
- [RealSense SDK 2.0](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide)
- [ur_rtde](https://pypi.org/project/ur-rtde/)
- pyserial

## Setup
Movement logic of robot depends on its placement relative to the checkerboard and collection box. Each square's position is calculated based on the square designated as the top-left square and the distance difference between each square.

To change where the top left square is, change `TOP_LEFT` in ()[./checkers/robot.py]
To change where the collection box is, change `BOX_POS` in ()[./checkers/robot.py]

**The position values we used are based on the "Base" feature.**
![Project setup for playing checkers with the UR5 image 1](./images/setup-1.jpg)
![Project setup for playing checkers with the UR5 image 2](./images/setup-2.jpg)
![The electromagnet circuit using the Arduino Nano and MOSFET module](./images/microcontroller.jpg)
