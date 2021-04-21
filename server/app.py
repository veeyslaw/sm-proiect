import io
import threading
import time
from flask import Flask, render_template, request, Response
from tests.test_painting import ImageDrawer

idrw = ImageDrawer(1200, 500)
app = Flask(__name__)


CONFIG = {
    "PORT": 6969,
    "FPS": 60
}
DELAY_SECONDS = 1.0 / CONFIG["FPS"]


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
    return "Camera is ON"


@app.route("/stop-camera", methods=["POST"])
def stop_camera():
    return "Camera is OFF"


def generate_image_data() -> bytes:
    while idrw.is_running:
        img_byte_arr = io.BytesIO()
        idrw.image.save(img_byte_arr, format='PNG')
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img_byte_arr.getvalue() + b'\r\n'
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
    idrw.run()
    t.join()
