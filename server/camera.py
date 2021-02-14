from time import time


def image_bin(path):
    with open(path, 'rb') as f:
        return f.read()


class Camera:
    PATH = r'C:\Users\bkmz1\Documents\books\python\some_cybernetic_scheisse\out.jpg'

    def get_frame(self):
        return image_bin(Camera.PATH)
