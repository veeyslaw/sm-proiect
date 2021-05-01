import threading
import subprocess
import time
from flask import Flask, render_template, request, Response
from image_handle import ImageHandle
import socket
from protocol import Command
from PIL import Image


class CONFIG:
    PORT = 6060
    FPS = 60
    DELAY_SECONDS = 1.0 / FPS
    CAMERA_PORT = 3333
    MESSAGE_LENGTH = 921600
    IMAGE_WIDTH = 1200
    IMAGE_HEIGHT = 500


ih = ImageHandle(CONFIG.IMAGE_WIDTH, CONFIG.IMAGE_HEIGHT)
app = Flask(__name__)
camera_on = False
camera_listener_thread = None
led_listener_thread = None
mutex = threading.Lock()
camera_sock = None


def launch_camera_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', CONFIG.CAMERA_PORT))
        sock.listen(1)
        global camera_sock
        (camera_sock, _) = sock.accept()

        global camera_on
        global ih
        while camera_on:
            message = camera_sock.recv(CONFIG.MESSAGE_LENGTH)
            if message == b'':
                print('Camera stopped')
                camera_on = False
                break
            image = Image.frombytes('RGB', (640, 480), message)
            #### pur teoretic e un PIL.Image corect transmis
            # if you want some spam
            # print(command)
            global mutex
            with mutex:
                ih.set(image)
        
        camera_sock.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    email = request.form.get("email")
    if len(email) < 3:
        msg = f"Bad email"
    else:
        global mutex
        with mutex:
            ih.save()
        subprocess.Popen(['python3', 'email_sender.py', email])
        msg = f"Email sent to {email}"
    return render_template("send_email.html", msg=msg)


### TODO
#@app.route("/capture-background", methods=["POST"])
#def capture_background():
    #global camera_sock
    #if camera_sock is not None:
        #camera_sock.send(b'c')


@app.route("/start-camera", methods=["POST"])
def start_camera():
    global camera_on
    if not camera_on:
        camera_on = True
        global camera_listener_thread
        camera_listener_thread = threading.Thread(target=launch_camera_listener)
        camera_listener_thread.start()
        subprocess.Popen(['python3', 'camera.py'])
    return "Camera is ON"


@app.route("/stop-camera", methods=["POST"])
def stop_camera():
    global camera_on
    global camera_listener_thread
    global led_listener_thread
    if camera_on and isinstance(camera_listener_thread, threading.Thread):
        camera_on = False
        camera_listener_thread.join()
    return "Camera is OFF"


def generate_image_data() -> bytes:
    while True:
        global ih
        global mutex
        with mutex:
            image = ih.image_bytes
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'
        time.sleep(CONFIG.DELAY_SECONDS)


@app.route("/drawing-stream")
def drawing_stream():
    return Response(generate_image_data(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/clear-drawing", methods=["POST"])
def clear_drawing():
    global ih
    ih.clear()
    return render_template("index.html")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT "] = 0
    app.run(host='0.0.0.0', port=CONFIG.PORT)
