import cv2
import cv2.aruco as aruco
from types import SimpleNamespace


class Camera:

    def __init__(self):
        self.url = 'http://192.168.0.2:8080'
        self.capture = cv2.VideoCapture(f'{self.url}/video')
        self.last_frame = None

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 5
        self.font_color = (0, 0, 230, 255)  # BGR order!
        self.back_color = (0, 0, 0, 255)
        self.thickness = 3
        self.margin = 20  # px

        self.aruco_data = None

    def get_frame(self):
        return self.capture.read()

    def get_gen(self):
        pass

    def detect_aruco(self, size=4, total_markers=250):
        """
        detect
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
        if self.aruco_data is None:
            self.aruco_data = SimpleNamespace(**{'ind': 0, 'boxes': None, 'ids': []})
        data = self.aruco_data
        if data.ind == 0:
            data.boxes, data.ids = self.detect_aruco()
        data.ind = (data.ind + 1) % freq
        if draw_bound and data.boxes is not None:
            self.last_frame = aruco.drawDetectedMarkers(self.last_frame, data.boxes)
        return [l[0] for l in data.ids] if data.ids is not None else []

    def add_ids(self, trail=3):
        """
        :param trail: last unique sets of ids to take into account
        """
        if self.aruco_data.ind == 0:  # update with same frequency as aruko
            pass

    def livestream(self):
        while True:
            ret, frame = self.get_frame()
            if not ret:
                self.write_on_frame('No connection')
            else:
                self.last_frame = frame
            self.aruco_with_freq(freq=5, draw_bound=True)
            self.add_ids()
            cv2.imshow('livestream', self.last_frame)
            if cv2.waitKey(1) == ord('q'):
                break
        self.capture.release()
        cv2.destroyAllWindows()

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
    Camera().livestream()
