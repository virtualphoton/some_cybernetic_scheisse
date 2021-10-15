import os.path
import sys

from flask import Flask, render_template, Response, request, jsonify
from cameras.ip_webcam.camera import Camera as IP_webcam
from simulation_connection import CommandSender
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__)

Camera_Class = IP_webcam
command_sender_port = 8766
resolution = (1920 // 2, 1080 // 2)


@app.route('/')
def index():
    print(resolution)
    return render_template('index.html', width=resolution[0], height=resolution[1])


def gen_wrapper(camera_generator):
    """
    wraps byte-strings images for flask to stream it
    :param camera_generator: - generator from camera class that yields bytestrings
    :return: byte string for streaming
    """
    while True:
        yield (b''.join((b'--frame\r\n',
                         b'Content-Type: image/jpeg\r\n\r\n', next(camera_generator), b'\r\n')))


@app.route('/video_feed')
def video_feed():
    return Response(gen_wrapper(Camera_Class().gen()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def change_resolution(new_res):
    global resolution
    resolution = new_res


@app.route('/send_command', methods=['POST'])
def send_command():
    flask_commands = {'change_res': change_resolution}
    req_data = request.json
    if req_data['command'] in flask_commands:
        flask_commands[req_data['command']](*req_data.get('args', []), **req_data.get('kwargs', {}))
    jsoned = json.dumps(req_data).encode()
    return jsonify(CommandSender(8766).send_command(jsoned).decode())


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
