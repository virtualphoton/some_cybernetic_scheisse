from time import time


def image_bin(path):
    with open(path, 'rb') as f:
        return f.read()


class Camera:
    def __init__(self):
        path = r'C:\Users\bkmz1\Documents\books\python\some_cybernetic_scheisse\bloggif_frames_gif\frame-{}.gif'
        self.frames = [image_bin(path.format(i)) for i in range(1, 5)]

    def get_frame(self, state):
        return self.frames[state]
