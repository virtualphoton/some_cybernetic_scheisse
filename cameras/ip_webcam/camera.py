import cv2


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

    def get_frame(self):
        return self.capture.read()

    def get_gen(self):
        pass

    def livestream(self):
        while True:
            ret, frame = self.get_frame()
            if not ret:
                self.write_on_frame('No connection')
            else:
                self.last_frame = frame
            cv2.imshow('livestream', self.last_frame)
            if cv2.waitKey(1) == ord('q'):
                break
        self.capture.release()
        cv2.destroyAllWindows()

    def write_on_frame(self, msg):
        h, w, _ = self.last_frame.shape
        (text_w, text_h), _ = cv2.getTextSize(msg, self.font, self.font_size, self.thickness)
        text_x, text_y = (w - text_w) // 2, (h - text_h) // 2
        cv2.rectangle(self.last_frame, (text_x - self.margin, text_y - self.margin),
                      (text_x + text_w + self.margin, text_y + text_h + self.margin), self.back_color, -1)
        cv2.putText(self.last_frame, msg, (text_x, text_y + text_h), self.font, self.font_size,
                    self.font_color, self.thickness)


if __name__ == '__main__':
    Camera().livestream()
