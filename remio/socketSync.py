from socketio import Client


class CustomSocketIO(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def stream(frame: str, *args, **kwargs):
        pass