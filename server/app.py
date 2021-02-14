from flask import Flask, render_template, Response
from server.camera import Camera
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    state = 0
    while True:
        frame = camera.get_frame(state)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        state = (state + 1) % 4
        time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
