#L8 - IOT Active WEB server
# LED rosu -  pin 3
# LED verde - pin 5
# LED blue  - pin 7
#import picamera
import RPi.GPIO as GPIO

#file=open("/var/www/html/imag/imag1.jpg","wb")
#camera=picamera.PiCamera()
#camera.resolution =(320,240)  # 1024,768
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29,GPIO.OUT)
GPIO.output(29,0) #aprind LED


#camera.start_preview()
#time.sleep(2)
#camera.capture(file)
#file.close()

import cv2
filename = '/var/www/html/imag/imag1.jpg'
vc = cv2.VideoCapture(0)
success, image = vc.read()
cv2.imwrite(filename, image)
