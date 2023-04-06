import pyrealsense2 as rs
import numpy as np
import cv2
from checkers.board import Board

class ComputerVision:
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
        
        self.color