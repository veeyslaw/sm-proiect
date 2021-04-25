import RPi.GPIO as GPIO
import socket
from app import CONFIG

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.output(37,1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', CONFIG.LED_PORT))
    sock.recv(1)

GPIO.output(37,0)
GPIO.cleanup()
