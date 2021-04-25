import cv2 as cv
import socket
from app import CAMERA_PORT
from protocol import Command


if __name__ == "__main__":
    vc = cv.VideoCapture(0)
    if not vc.isOpened():
        print('Cannot open camera')
        exit()
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', CAMERA_PORT)) 

        try:
            x = 0
            y = 0
            while True:
                ret, frame = vc.read()
                if not ret:
                    print('Cannot read frame')
                    break
                frame = cv.flip(frame, 1)
                out.write(frame)

                x = x + 1
                y = y + 1
                command = Command(Command.MOVE, x, y)
                try:
                    sent = sock.send(command.to_bytes())
                    if sent == 0:
                        break
                except BrokenPipeError:
                    break
        finally:
            out.release()
            vc.release()
