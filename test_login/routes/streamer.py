import time

from flask import Blueprint, Response, jsonify
from flask_cors import CORS, cross_origin

streaming = Blueprint('streaming', __name__)
cors = CORS(streaming, resources=r"/video_feed")

class Camera(object):
    def __init__(self, cam_id):
        self.cam_id = cam_id
        self.frames = []
        for i in range(3):
            with open(f'images/{i}.jpg', 'rb') as f:
                self.frames.append(f.read())

    def get_frame(self):
        ret = self.frames[int(time.time() * int(self.cam_id)) % 3]
        time.sleep(1)
        return ret



def gen(camera):
    for _ in range(100):
        
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@streaming.route('/video_feed/<cam_id>', methods=['GET'])
def video_feed(cam_id):
    return Response(gen(Camera(cam_id)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@streaming.route("/t", methods=['GET', "POST"])
@cross_origin(supports_credentials=True)
def login():
  return jsonify({'success': 'ok'})