#L8 - IOT Active WEB server
# LED rosu -  pin 3
# LED verde - pin 5
# LED blue  - pin 7
import picamera
import RPi.GPIO as GPIO

file=open("/var/www/html/imag/imag1.jpg","wb")
camera=picamera.PiCamera()
camera.resolution =(320,240)  # 1024,768
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,0) #aprind LED
GPIO.setwarnings(False)

#camera.start_preview()
#time.sleep(2)
camera.capture(file)
file.close()




