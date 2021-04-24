import cv2 as cv
import mediapipe as mp

vc = cv.VideoCapture(0)

if not vc.isOpened():
    print('Cannot open camera')
    exit()

fiourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)


try:
    while True:
        ret, frame = vc.read()
        if not ret:
            print('Cannot read frame')
            break
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(frame)
        out.write(frame)
finally:
    out.release()
    vc.release()
