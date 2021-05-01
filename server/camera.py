import cv2
import numpy as np
import socket
import time
from protocol import Command
from app import CONFIG
import threading
import subprocess
import time
from PIL import Image


LED_PORT = 9999
# parameters
cap_region_x_begin = 0  # start point/total width
cap_region_y_end = 1  # start point/total width
threshold = 20  # BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0
camera_on = False
capture_background = True


def launch_led_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', LED_PORT))
        sock.listen(1)
        (led_sock, _) = sock.accept()
    
        global camera_on
        while camera_on:
            time.sleep(1)
            message = led_sock.recv(8)

        led_sock.close()


def launch_app_listener(app_sock):
    global camera_on
    global capture_background
    while camera_on:
        time.sleep(0.1)
        message = led_sock.recv(8)
        if message == b'':
            camera_on = False
            break
        elif message == b'c':
            capture_background = True


def remove_bg(bg_model, img_frame):
    fgmask = bg_model.apply(img_frame, learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    result = cv2.bitwise_and(img_frame, img_frame, mask=fgmask)
    return result


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print('Cannot open camera')
        exit()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', CONFIG.CAMERA_PORT))
        try:
            camera_on = True
            app_listener_thread = threading.Thread(target=launch_app_listener)
            app_listener_thread.start()
            led_listener_thread = threading.Thread(target=launch_led_listener)
            led_listener_thread.start()
            subprocess.Popen(['python3', 'led.py'])
            
            capture_frames = 0
            while camera.isOpened():
                ret, frame = camera.read()
                if not ret:
                    print('Cannot read frame')
                    break
                if capture_frames > 0:
                    capture_frames -= 1
                else:
                    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
                    frame = cv2.flip(frame, 1)  # flip the frame horizontally

                    img = remove_bg(bgModel, frame)
                    stop_x = int(cap_region_y_end * frame.shape[0])
                    start_y = int(cap_region_x_begin * frame.shape[1])
                    img = img[:stop_x, start_y:frame.shape[1]]  # clip the ROI

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

                        cv2.circle(img, pmax, 8, (200, 0, 255), -1)
                        cv2.drawContours(img, [res], 0, (0, 255, 0), 2)
                        cv2.drawContours(img, [hull], 0, (0, 0, 255), 3)
                        try:
                            message = Image.fromarray(img, 'RGB').tobytes()
                            sent = sock.send(message)
                            if sent == 0:
                                break
                        except BrokenPipeError:
                            break
                        except ConnectionResetError:
                            break
                    
                if capture_background:
                    capture_background = False
                    capture_frames = 100
                    bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
                    
                time.sleep(0.01)

        finally:
            camera_on = False
            led_listener_thread.join()
            app_listener_thread.join()
            camera.release()
