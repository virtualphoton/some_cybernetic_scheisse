import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, Response, request, jsonify
from cameras.webcam.camera import Camera as Webcam
from .simulation_connection import CommandSender
from .constants import SECRET_KEY
from .authorization import authorization
import json
from datetime import timedelta

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.register_blueprint(authorization)

connected_ids = set()
machines = {
    1: {
        'aruco_id': 1,
        'name': 'I identify myself as a 6R robot',
        'js_path': '/static/js/01_commands.js',
        'port': 8786,
        'connected': 0
    }
}


def get_machines_fields(ids, fields):
    return [{field: machines[id_][field] for field in fields} for id_ in ids if id_ in machines]


@app.route('/')
def index():
    return render_template('index.html', width=1920 // 2, height=1080 // 2)


def gen_wrapper(camera_generator):
    """
    wraps byte-strings images for flask to stream it
    :param camera_generator: - generator from camera class that yields bytestrings
    :return: byte string for streaming
    """
    while True:
        yield (b''.join((b'--frame\r\n',
                         b'Content-Type: image/jpeg\r\n\r\n', next(camera_generator), b'\r\n')))


@app.route('/get_machines', methods=['GET'])
def get_machines():
    ids = set(map(int, Webcam('url', url=camera_url).get_ids())) | connected_ids
    data = get_machines_fields(ids, ('aruco_id', 'name', 'connected'))
    return jsonify(data)


@app.route('/toggle_state', methods=['POST'])
def toggle_state():
    data = request.json['button_id']
    _, new_state, id_ = data.split('_')
    id_ = int(id_)
    port = machines[id_]['port']
    if new_state == 'on':
        CommandSender(port).send_command({'command': 'connect'})
        connected_ids.add(id_)
        machines[id_]['connected'] = 1
        return jsonify({'type': 'has_connected', 'commands_url': machines[id_]['js_path']})
    elif new_state == 'off':
        CommandSender(port).send_command({'command': 'disconnect'})
        connected_ids.remove(id_)
        machines[id_]['connected'] = 0
        return jsonify({'type': 'has_disconnected'})


@app.route('/video_feed')
def video_feed():
    return Response(gen_wrapper(Webcam('url', url=camera_url).gen()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/send_command', methods=['POST'])
def send_command():
    flask_commands = {}
    req_data = request.json
    if req_data['command'] in flask_commands:
        ret_json = flask_commands[req_data['command']](*req_data.get('args', []), **req_data.get('kwargs', {}))
    else:
        jsoned = json.dumps(req_data)
        port = machines[req_data['id']]['port']
        ret_json = json.loads(CommandSender(port).send_command(jsoned))
    return jsonify(ret_json)


if __name__ == '__main__':
    # camera_url = input('Type ip and port of ip webcam (e.g. 192.168.0.3:8080): ')
    app.run(host='localhost', debug=True)
