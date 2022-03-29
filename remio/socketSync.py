from socketio import Client


class CustomSocketIO(Client):
    def __init__(self, address: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = address

    def stop(self):
        self.disconnect()

    def start(self):
        if self.address is not None:
            try:
                self.connect(self.address, wait=False)
            except Exception as e:
                print("socket:: ", e)