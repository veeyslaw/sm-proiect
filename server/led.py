#import RPi.GPIO as GPIO
import socket
import time
from camera import LED_PORT

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(37,GPIO.OUT)
#GPIO.output(37,1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', LED_PORT))
    while True:
        try:
            sent = sock.send(b'0')
            if sent == 0:
                break
        except BrokenPipeError:
            break
        except ConnectionResetError:
            break

#GPIO.output(37,0)
#GPIO.cleanup()
