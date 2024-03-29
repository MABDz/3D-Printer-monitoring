import cv2
import numpy as np


chessboard_img = cv2.imread('image2.jpg', cv2.IMREAD_GRAYSCALE)
replacement_img = cv2.imread('2d.png')

ret, corners = cv2.findChessboardCorners(chessboard_img, (7,7), None)

if ret == True:

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    cv2.cornerSubPix(chessboard_img, corners, (11,11), (-1,-1), criteria)

    src_pts = np.float32([[0,0], [replacement_img.shape[1], 0], [replacement_img.shape[1], replacement_img.shape[0]], [0, replacement_img.shape[0]]])
    dst_pts = np.float32([corners[0,0], corners[6,0], corners[-1,0], corners[-7,0]])

    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    warped_img = cv2.warpPerspective(replacement_img, M, (chessboard_img.shape[1], chessboard_img.shape[0]))

    cv2.imwrite('result.jpg', warped_img)

else:
    print("Could not find chessboard corners.")
