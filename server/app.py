from flask import Flask, render_template, Response, request, abort, session, jsonify
from server.simulation_connection import Camera, CommandSender
import time
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/send_command', methods=['POST'])
def send_command():
    req_data = request.json
    jsoned = json.dumps(req_data).encode()
    return jsonify(CommandSender().send_command(jsoned).decode())


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
