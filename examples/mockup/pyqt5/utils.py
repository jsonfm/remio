from threading import Timer
import cv2


def process_image(frame=None, width=2):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


class Processing(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
