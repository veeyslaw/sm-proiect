import sys
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    email = request.form.get("email")
    # send email with smtp
    return render_template("send_email.html", email=email)


@app.route("/start-camera", methods=["POST"])
def start_camera():
    return "Camera is ON"


@app.route("/stop-camera", methods=["POST"])
def stop_camera():
    return "Camera is OFF"


if __name__ == "__main__":
    port = 6969
    try:
        port = int(sys.argv[1])
    except Exception as e:
        print(e)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT "] = 0
    app.run(port=port)
