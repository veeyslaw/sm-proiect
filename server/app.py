import io
import threading
import time
import cv2
import numpy as np
from flask import Flask, render_template, request, Response
from tests.test_painting import ImageDrawer

idrw = ImageDrawer(1200, 500)
app = Flask(__name__)

PORT = 6969
HOST = "127.0.0.1"


@app.route("/")
def index():
    return render_template("index.html", address=f"{HOST}:{PORT}")


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
    return "Camera is ON"


@app.route("/stop-camera", methods=["POST"])
def stop_camera():
    return "Camera is OFF"


def generate_image_data() -> bytes:
    while idrw.is_running:
        img_byte_arr = io.BytesIO()
        idrw.image.save(img_byte_arr, format='PNG')
        nparr = np.fromstring(img_byte_arr.getvalue(), np.uint8)
        img = cv2.imdecode(nparr, flags=1)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        time.sleep(0.1)


@app.route('/drawing-stream')
def drawing_stream():
    return Response(generate_image_data(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT "] = 0
    t = threading.Thread(target=lambda: app.run(port=PORT))
    t.start()
    idrw.run()
    t.join()
