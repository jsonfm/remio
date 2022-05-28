"""Some utils."""
from threading import Thread, Event
import numpy as np
import cv2
import json
import time


def processing(frame: np.ndarray = None):
    """It applies some processing to the image"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


class PausableTimer:
    """A timer with a recurrent task."""
    def __init__(self, interval = None, callback = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.timeout = interval
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.running = Event()
        self.pauseEvent = Event()
        self.thread = Thread(target=self.run, daemon=True)
        self.start()
        self.pause()
        self.quit = False

    def start(self):
        self.thread.start()

    def run(self):
        while True:
            self.pauseEvent.wait()
            self.running.wait(self.timeout)
            self.callback(*self.args, **self.kwargs)
            if self.quit:
                break

    def resume(self, now: bool = True):
        self.pauseEvent.set()
        if now:
            self.running.set()

    def pause(self, reset=False):
        self.pauseEvent.clear()
        if reset:
            self.running.clear()

    def stop(self):
        self.resume(now=True)
        self.quit = True


class CountTimer:
    """A timer tha executes a task periodically.
    Args:
        cb: a callback function
        interval: time in seconds.
    """
    def __init__(self, cb, interval: int = 1):
        self.lastTime = 0
        self.enabled = False
        self.cb = cb
        self.interval = interval
    
    def start(self):
        """Starts the timer."""
        self.lastTime = time.time()
        self.enabled = True
    
    def stop(self):
        """Stops the timer."""
        self.lastTime = 0
        self.time = 0
        self.enabled = False

    def update(self):
        """Checks if the callback must be executed."""
        if self.enabled:
            if time.time() - self.lastTime <= self.interval:
                self.cb()
                self.lastTime = time.time()


class Variables:
    """A variables dictionary with some extra functionalities, like state backup.
    
    Args:
        variables: a dictionary with variables.

    Example:
        variables = Variable({
            'var1': 1, # type: int
            'var2': 3.14 # type: float
            'var3': 'active' # type: str
            'var4': False, # type: bool
        })
    """
    def __init__(self, variables: dict = {}):
        self.variables = variables
        self.backup = variables.copy()
        self.updatedStatus = False

    def __len__(self):
        return len(self.variables)

    def __str__(self):
        return str(self.variables)
    
    def __getitem__(self, key):
        return self.variables[key]
    
    def __setitem__(self, key: str, value):
        self.variables[key] = value

    def restore(self):
        """Restores the variables backup."""
        self.variables = self.backup.copy()

    def set(self, key: str, value, backup=True):
        """Updates a variable value"""
        if backup:
            self.backup = self.variables.copy()
        self.variables[key] = value
    
    def get(self, key):
        """Returns a specific variable value."""
        return self.variables[key]

    def values(self):
        """Get the variables values on dict format."""
        return self.variables

    def json(self):
        """Returns the variables dict as JSON string."""
        return json.dumps(self.variables)

    def update(self, data: str):
        """Updates the variables values."""
        if isinstance(data, str):
            data = json.loads(data)
        self.variables = data
        self.backup = dict(self.variables)
        self.setUpdated(True)

    def setUpdated(self, value: bool):
        """Updates the updated status."""
        self.updatedStatus = value
    
    def updated(self):
        """Returns the updated status."""
        return self.updatedStatus
