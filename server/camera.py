import cv2
import numpy as np
import math
import socket
import time
from app import CAMERA_PORT, IMAGE_WIDTH, IMAGE_HEIGHT
from protocol import Command


# parameters
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 7  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0


def removeBG(bgModel, frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print('Cannot open camera')
        exit()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', CAMERA_PORT)) 

        try:
            time.sleep(1)
            bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
            
            while camera.isOpened():
                ret, frame = camera.read()
                if not ret:
                    print('Cannot read frame')
                    break
                
                frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
                frame = cv2.flip(frame, 1)  # flip the frame horizontally

                img = removeBG(bgModel, frame)
                img = img[0:int(cap_region_y_end * frame.shape[0]),
                            int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI

                # convert the image into binary image
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
                ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

                # get the coutours
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                length = len(contours)

                if length > 0:
                    maxArea = -1
                    for i in range(length):  # find the biggest contour (according to area)
                        temp = contours[i]
                        area = cv2.contourArea(temp)
                        if area > maxArea:
                            maxArea = area
                            ci = i

                    res = contours[ci]
                    hull = cv2.convexHull(res)
                    pts = [(p[0][0], p[0][1]) for p in hull]
                    pmax = min(pts, key=lambda p: p[1])
                    
                    x = int(pmax[0] / img.shape[1] * IMAGE_WIDTH)
                    y = int(pmax[1] / img.shape[0] * IMAGE_HEIGHT)
                    command = Command(Command.MOVE, x, y)
                    try:
                        sent = sock.send(command.to_bytes())
                        if sent == 0:
                            break
                    except BrokenPipeError:
                        break
                
        finally:
            camera.release()
