import os.path
import sys

from flask import Flask, render_template, Response, request, jsonify
from cameras.ip_webcam.camera import Camera as IP_webcam
from simulation_connection import CommandSender
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__)

cam = IP_webcam()
command_sender_port = 8766

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
    ids = set(map(int, cam.get_ids())) | connected_ids
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
    return Response(gen_wrapper(cam.gen()),
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
    app.run(host='localhost', debug=True)
