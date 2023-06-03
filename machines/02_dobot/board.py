import cv2.aruco as aruco

dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.CharucoBoard(8, 8, .4, .2, dictionary)

board.draw((100, 100))