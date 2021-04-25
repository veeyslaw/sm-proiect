import io
import threading
import subprocess
import time
from flask import Flask, render_template, request, Response
from image_handle import ImageHandle
import socket
from protocol import Command


CONFIG = {
    "PORT": 6969,
    "FPS": 144
}
DELAY_SECONDS = 1.0 / CONFIG["FPS"]
CAMERA_PORT = 3333
MESSAGE_LENGTH = 1024
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 500


ih = ImageHandle(IMAGE_WIDTH, IMAGE_HEIGHT)
app = Flask(__name__)
camera_on = False
camera_listener_thread = None


def launch_camera_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', CAMERA_PORT))
        sock.listen(1)
        (camera_sock, _) = sock.accept()
    
    global camera_on
    global ih
    while camera_on:
        message = camera_sock.recv(MESSAGE_LENGTH)
        if message == b'':
            print('Camera stopped')
            camera_on = False
            break
        command = Command.from_bytes(message)
        print(str(command))
        ih.paint(command.x, command.y)
    
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
        msg = f"Email sent to {email}"
        # send email with smtp
    return render_template("send_email.html", msg=msg)


@app.route("/start-camera", methods=["POST"])
def start_camera():
    global camera_on
    if not camera_on:
        camera_on = True
        global camera_listener_thread
        camera_listener_thread = threading.Thread(target=launch_camera_listener)
        camera_listener_thread.start()
        subprocess.Popen(['python', 'camera.py'])
    return "Camera is ON"


@app.route("/stop-camera", methods=["POST"])
def stop_camera():
    global camera_on
    if camera_on:
        camera_on = False
        global camera_listener_thread
        camera_listener_thread.join()
    return "Camera is OFF"


def generate_image_data() -> bytes:
    while True:
        global ih
        image = ih.image_bytes
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'
        time.sleep(DELAY_SECONDS)


@app.route('/drawing-stream')
def drawing_stream():
    return Response(generate_image_data(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT "] = 0
    t = threading.Thread(target=lambda: app.run(port=CONFIG["PORT"]))

    t.start()
    t.join()
