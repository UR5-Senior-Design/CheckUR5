import pyrealsense2 as rs
import numpy as np
import cv2
from checkers.board import Board

# class CheckersPiece:
#     isKing = False
    
#     def __init__(self, id):
#         self.id = id

# class CheckersBoard:
#     board_matrix = [[0 for x in range(8)] for y in range(8)] 
    
#     def __init__(self):
#         pass
    
#     def findPiece(self, id):
#         for row in self.board:
#             for col in row:
#                 if id == self.board_matrix[row][col].id:
#                     return [row, col]
#                 else:
#                     print("error: Piece \""+id+"\" not found!")
    
#     def addPiece(self, id, position):
#         self.board_matrix[position[0]][position[1]] = CheckersPiece(id)
    
#     def removePiece(self, id):
#         position = self.findPiece(id)
#         self.board_matrix[position[0]][position[1]] = 0
    
#     def movePiece(self, id, destination):
#         if self.board_matrix[destination[0]][destination[1]] != 0:
#             self.removePiece(id)
#             self.addPiece(id, destination)
        
#     def makeKing(self, id):
#         position = self.findPiece(id)
#         self.board_matrix[position[0]][position[1]].isKing = True


def findAruco(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    arucoParam = cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParam)
    
    marker_corners, ids, _ = arucoDetector.detectMarkers(gray)
    # print(ids[1], marker_corners[1][0][0][0])
    
    all_arucos = {}
    
    if ids is not None:
        for i in range (len(ids)):
            x_center = (marker_corners[i][0][0][0] + marker_corners[i][0][1][0] + marker_corners[i][0][2][0] + marker_corners[i][0][3][0])/4
            y_center = (marker_corners[i][0][0][1] + marker_corners[i][0][1][1] + marker_corners[i][0][2][1] + marker_corners[i][0][3][1])/4
            all_arucos[ids[i][0]] = [int(y_center/125), int(x_center/125)]
    
    cv2.aruco.drawDetectedMarkers(img, marker_corners)
    
    return all_arucos

checkerboard = Board()

checkerboard.get_piece(5, 0).make_king()

pipeline = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

color_path = 'V00P00A00C00_rgb.avi'
# depth_path = 'V00P00A00C00_depth.avi'
colorwriter = cv2.VideoWriter(color_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (1920,1080), 1)
# depthwriter = cv2.VideoWriter(depth_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (640,480), 1)

pipeline.start(config)

# board = np.zeros(shape=(8,8))
# board = [0][1]
# print(board)

try:
    while True:
        frames = pipeline.wait_for_frames()
        # depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not color_frame: # if not depth_frame or not color_frame:
            continue
        
        #convert images to numpy arrays
        # depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        colorwriter.write(color_image)
        # depthwriter.write(depth_colormap)
        
        width, height = 1000, 1000
        point1 = np.float32([[651,97], [545, 706], [1452, 703], [1319, 92]])

        point2 = np.float32([[0, 0], [0, height-1], [width-1, height-1], [width-1, 0]])
        matrix = cv2.getPerspectiveTransform(point1, point2)
        output = cv2.warpPerspective(color_image, matrix, (width, height)) 
        output = cv2.rotate(output, cv2.ROTATE_90_CLOCKWISE)
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        output = cv2.filter2D(src=output, ddepth=-1, kernel=kernel)
        
        all_arucos = findAruco(output)
        
        checkerboard.update_board(all_arucos)
        print(" ")
        checkerboard.print_board()
        
        # for id in all_arucos:
        #     print(all_arucos[id][0])
        
        # print(all_arucos)
        
        # cv2.imshow("Image", color_image)
        cv2.imshow("Output", output)
        
        if cv2.waitKey(1) == ord("q"):
            break
finally:
    colorwriter.release()
    cv2.destroyAllWindows()
    # depthwriter.release()
    pipeline.stop()