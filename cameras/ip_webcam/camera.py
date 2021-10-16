import cv2
import cv2.aruco as aruco
from types import SimpleNamespace
from time import sleep
import threading


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Camera(metaclass=Singleton):
    camera_instance = None

    def __init__(self):

        self.url = 'http://192.168.0.2:8080'
        self.capture = cv2.VideoCapture(f'{self.url}/video')
        self.last_frame = None
        self.last_frame_id = 0
        self.dt = 0.01

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 5
        self.font_color = (0, 0, 230, 255)  # BGR order!
        self.back_color = (0, 0, 0, 255)
        self.thickness = 3
        self.margin = 20  # px

        self.aruco_data = SimpleNamespace(**{'ind': 0, 'boxes': None, 'ids': [], 'saved_ids': [], 'saved_ids_ind': 0})
        self.frame_getter_thread()

    def get_frame(self):
        """
        :return: numpy.ndarray representing image(because it's opencv)
        """
        return self.capture.read()

    def frame_getter_thread(self):
        """
        method that starts a thread that gets images
        :return:
        """

        def thread_func(self: Camera):

            while True:
                ret, frame = self.get_frame()
                if not ret:
                    self.write_on_frame('No connection')
                    self.last_frame_id = -1
                    break
                else:
                    self.last_frame = frame
                    self.last_frame_id += 1
                self.aruco_with_freq(draw_bound=True)
                self._add_ids()

        thread = threading.Thread(target=thread_func, args=(self,))
        thread.start()

    def gen(self):
        """
        generator for streaming
        :return: image as a string of bytes
        """
        sent_id = 0
        stop_flag = None
        while stop_flag is None:
            while sent_id == self.last_frame_id:
                sleep(self.dt)
                if self.last_frame_id == -1:
                    break
            sent_id = self.last_frame_id
            _, buf_arr = cv2.imencode('.jpg', self.last_frame)
            stop_flag = yield buf_arr.tobytes()

    def detect_aruco(self, size=4, total_markers=250):
        """
        detect aruco on image
        :param size: size of nxn marker(default and minimum are 4)
        :param total_markers: maximum id of marker(not included). Default 250, i.e. 0 <= id <= 249
        :return: found boxes and ids of markers
        """
        key = getattr(aruco, f'DICT_{size}X{size}_{total_markers}')
        aruco_dict = aruco.Dictionary_get(key)
        aruco_param = aruco.DetectorParameters_create()
        gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
        boxes, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_param)
        return boxes, ids

    def aruco_with_freq(self, freq=5, draw_bound=True):
        """
        calls detect_aruco() once per n frames
        :param freq: number of frames between looking for aruco
        :param draw_bound: whether to draw bound around aruco codes on self.last_frame. Default True
        :return: list of ids of markers
        """
        data = self.aruco_data
        if not data.ind:
            data.boxes, ids = self.detect_aruco()
            data.ids = [id_[0] for id_ in ids] if ids is not None else []
        data.ind = (data.ind + 1) % freq
        if draw_bound and data.boxes is not None:
            self.last_frame = aruco.drawDetectedMarkers(self.last_frame, data.boxes)
        return data.ids

    def _add_ids(self, trail=10):
        """
        :param trail: last unique sets of ids to take into account
        """
        data = self.aruco_data
        if data.ind == 0:  # update with same frequency as aruco
            if not len(data.saved_ids):
                data.saved_ids = [set()] * trail
            data.saved_ids[data.saved_ids_ind % trail] = set(data.ids)
            data.saved_ids_ind += 1

    def get_ids(self):
        """
        :return: set of markers' ids on frame
        """
        ids = set()
        for id_ in self.aruco_data.saved_ids:
            ids |= id_
        return ids

    def write_on_frame(self, msg):
        """
        write text in the middle of the screen
        :param msg:
        """
        h, w, _ = self.last_frame.shape
        (text_w, text_h), _ = cv2.getTextSize(msg, self.font, self.font_size, self.thickness)
        text_x, text_y = (w - text_w) // 2, (h - text_h) // 2
        cv2.rectangle(self.last_frame, (text_x - self.margin, text_y - self.margin),
                      (text_x + text_w + self.margin, text_y + text_h + self.margin), self.back_color, -1)
        cv2.putText(self.last_frame, msg, (text_x, text_y + text_h), self.font, self.font_size,
                    self.font_color, self.thickness)


if __name__ == '__main__':
    cam = Camera()
    cam.frame_getter_thread()
    id_ = 0
    while True:
        if id_ != cam.last_frame_id:
            cv2.imshow('livestream', cam.last_frame)
            if cv2.waitKey(1) == ord('q'):
                break
            id_ += 1
    cam.capture.release()
    cv2.destroyAllWindows()
