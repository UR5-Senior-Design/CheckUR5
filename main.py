from checkers.game import Game
from checkers.minimax.algorithm import minimax
import time
import cv2
import pyrealsense2 as rs
import numpy as np

def findAruco(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    arucoParam = cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParam)
    
    marker_corners, ids, _ = arucoDetector.detectMarkers(gray)
    
    all_arucos = {}
    
    if ids is not None:
        for i in range (len(ids)):
            x_center = (marker_corners[i][0][0][0] + marker_corners[i][0][1][0] + marker_corners[i][0][2][0] + marker_corners[i][0][3][0])/4
            y_center = (marker_corners[i][0][0][1] + marker_corners[i][0][1][1] + marker_corners[i][0][2][1] + marker_corners[i][0][3][1])/4
            all_arucos[ids[i][0]] = [int(y_center/125), int(x_center/125)] # dictionary in the format id: [row, col] for every aruco marker ID
    
    cv2.aruco.drawDetectedMarkers(img, marker_corners)
    
    return all_arucos

MINIMAX_DEPTH = 4

# start running the checkers game from here
def main():
    
    # initialize camera
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

    color_path = 'V00P00A00C00_rgb.avi'
    colorwriter = cv2.VideoWriter(color_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (1920,1080), 1)
    pipeline.start(config)
    
    
    run = True # set state of the game
    game = Game()

    print(f"Welcome to CheckUR5!\n\nHere are the commands you can type and send:\n")
    print(f"\tStart - start the game\n\tReset - reset the game\n\tQuit - quit the game")

    # TODO: add interaction to start the gamea
    try:
        while run:
            winner = game.get_winner()
            if winner != None:
                if winner == "orange":
                    print(f"The UR5 Robot won the game!")
                else:
                    print(f"The Player won the game!")
                
                # TODO: maybe give option to reset and start the game again here???
                run = False
            # robot's turn
            elif game.turn == "orange":
                value, new_board = minimax(game.get_board(), MINIMAX_DEPTH, "orange", game)

                print("UR5 Robot's turn actions: \n")
                game.ai_move(new_board) # set robot's move decision and move robot
            # human player's turn
            elif game.turn == "blue":
                # TODO: add turn timeout after 20 seconds
                # timeout = 20 # 20 seconds to make a turn
                player_input = input("Player's turn, press A to end turn")

                if player_input == "A":
                    
                    # get next frame
                    frames = pipeline.wait_for_frames()
                    color_frame = frames.get_color_frame()
                    if not color_frame:
                        continue
                    
                    #convert images to numpy arrays
                    color_image = np.asanyarray(color_frame.get_data())
                    
                    colorwriter.write(color_image)
                    
                    # warp & crop board image
                    width, height = 1000, 1000
                    point1 = np.float32([[561,110], [399, 917], [1485, 928], [1355, 105]])
                    point2 = np.float32([[0, 0], [0, height-1], [width-1, height-1], [width-1, 0]])
                    matrix = cv2.getPerspectiveTransform(point1, point2)
                    output = cv2.warpPerspective(color_image, matrix, (width, height)) 
                    output = cv2.rotate(output, cv2.ROTATE_180)
                    
                    # sharpen image
                    kernel = np.array([[0, -1, 0],
                                    [-1, 5,-1],
                                    [0, -1, 0]])
                    output = cv2.filter2D(src=output, ddepth=-1, kernel=kernel)
                    
                    # find arucos and returns dictionary of aruco IDs and their positions on the board
                    all_arucos = findAruco(output)
                    
                    game.update_board(all_arucos)
                    
                    # for id in all_arucos:
                    #     print(all_arucos[id][0])
                    
                    # print(all_arucos)
                    
                    # cv2.imshow("Image", color_image)
                    # cv2.imshow("Output", output)
                    
                    # if cv2.waitKey(1) == ord("q"):
                    #     break
                    
                    
                    # TODO: some computer vision logic here maybe?
                    # maybe i could get rid of the checking for player_input from keyboard and we could just check if board in a changed and steady state?

                # indicate the moves/removes human has made
                print(f"Player's turn actions: \n")
            
            # TODO: add interaction to reset the game
            # TODO: add interaction to quit the game
    finally:
        colorwriter.release()
        cv2.destroyAllWindows()
        pipeline.stop()
main()
