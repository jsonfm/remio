from threading import Timer
import numpy as np
import cv2


def processing(frame: np.ndarray = None):
    """It applies some processing to the image"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


class RepeatTimer(Timer):
    """A timer with a recurrent task."""
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
