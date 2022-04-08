import time
import json
from typing import Union
from threading import Thread, Event
from serial import Serial
from serial.tools import list_ports
from .sevent import Emitter


class SerialEmitter(Emitter):
    """A custom serial class threaded and event emit based.

    Args:
        name: device name
        reconnectDelay: wait time between reconnection attempts.
        maxAttempts: max read attempts.
        portsRefreshTime: time for check serial devices changes.
        emitterIsEnabled: disable on/emit events (callbacks execution)

    Events:
        data: incoming(data: str).
        connection: update(status: bool).
        ports: list:ports

    """

    def __init__(
        self,
        name: str = "default",
        reconnectDelay: Union[int, float] = 1,
        maxAttempts: int = 10,
        portsRefreshTime: int = 1,
        emitterIsEnabled: bool = True,
        emitAsDict: bool = True,
        *args,
        **kwargs
    ):
        super().__init__(emitterIsEnabled=emitterIsEnabled, *args, **kwargs)
        self.name = name
        self.port = kwargs.pop("port", None)
        self.reconnectDelay = reconnectDelay
        self.maxAttempts = maxAttempts
        self.portsRefreshTime = portsRefreshTime
        self.emitAsDict = emitAsDict
        self.lastConnectionState = False
        self.attempts = 0
        self.time = 0
        self.lastDevicesList = []
        self.serial = Serial(*args, **kwargs)

        self.thread = Thread(target=self.run, name="serial-thread", daemon=True)
        self.running = Event()
        self.pauseEvent = Event()
        self.resume()

    def __setitem__(self, key, value):
        if self.serial.isOpen():
            self.serial.close()
        setattr(self.serial, key, value)

    def isConnected(self):
        """It checks if the serial port is open."""
        return self.serial.isOpen()

    def getPort(self):
        """It returns the current port device."""
        return self.serial.port

    def setPort(self, port: str = None):
        """It updates the port device value."""
        if port is not None:
            self.serial.close()
            self.serial.port = port
            self.connect()
        
    def restorePort(self):
        """Restores the default serial port."""
        self.setPort(self.port)
    
    def resume(self):
        """It resumes the read loop."""
        self.pauseEvent.set()

    def pause(self):
        """It pauses the read loop."""
        self.pauseEvent.clear()

    def setPause(self, value: bool = True):
        """Updates the pause/resume state."""
        if value:
            self.pause()
        else:
            self.resume()

    def needAPause(self):
        """It pauses or resume the read loop."""
        self.pauseEvent.wait()

    def hasDevice(self):
        """It checks if a serial device is setted."""
        return self.port is not None

    def isOpen(self):
        """It checks if serial port device is open."""
        return self.serial.isOpen()

    def attemptsLimitReached(self):
        """Check if read attempts have reached their limit."""
        return self.attempts >= self.maxAttempts

    def start(self):
        """It starts read loop."""
        self.running.set()
        self.thread.start()

    def getListOfPorts(self):
        """It returns a list with the availables serial port devices."""
        return [port.device for port in list_ports.comports()]

    def connect(self):
        """It will try to connect with the specified serial device."""
        try:
            self.lastConnectionState = self.serial.isOpen()

            if self.serial.isOpen():
                self.serial.close()

            if self.serial.port is None and self.port is not None:
                self.serial.port = self.port

            self.serial.open()

        except Exception as e:
            print("connection error: ", e)
    
    def dictToJson(self, message: dict = {}) -> str:
        """It converts a dictionary to a json str."""
        try:
            return json.dumps(message)
        except Exception as e:
            print('Serial:: ', e)
        return message

    def write(self, message: Union[str, dict] = "", end: str = "\n", asJson: bool = False):
        """It writes a message to the serial device.

        Args:
            message: string to be sent.
            end: newline character to be concated with the message.
        """
        if self.serial.isOpen():
            try:
                if len(message) > 0:
                    if asJson:
                        message = self.dictToJson(message)                  
                    message += end
                    message = message.encode()
                    self.serial.write(message)
            except Exception as e:
                print("Write error: ", e)

    def readData(self):
        """It will try to read incoming data."""
        try:
            data = self.serial.readline().decode().rstrip()
            if len(data) > 0:
                if self.emitAsDict: data = {self.name: data}
                self.emit("data", data)
                return data
        except Exception as e:
            print("Read data error: ", e)
            if not self.attemptsLimitReached():
                self.attempts += 1
            else:
                self.attempts = 0
                try:
                    self.serial.close()
                except Exception as e:
                    print(e)
            return None

    def checkSerialPorts(self, dt: Union[int, float]):
        """It Monitors if there are changes in the serial devices."""
        if self.portsRefreshTime > 0:
            self.time += dt
            if self.time >= self.portsRefreshTime:
                actualDevicesList = self.getListOfPorts()
                if actualDevicesList != self.lastDevicesList:
                    self.lastDevicesList = actualDevicesList
                    self.emit("ports", actualDevicesList)
                self.time = 0

    def run(self):
        """Here the run loop is executed."""
        while self.running.is_set():
            t0 = time.time()

            if self.lastConnectionState != self.serial.isOpen():
                status = self.serial.isOpen()
                if self.emitAsDict: status = {self.name: status}
                self.emit("connection", status)
                self.lastConnectionState = self.serial.isOpen()

            if self.serial.isOpen():
                self.readData()
            else:
                if self.hasDevice():
                    self.connect()
                    time.sleep(self.reconnectDelay)

            t1 = time.time()
            dt = t1 - t0

            self.checkSerialPorts(dt)
            self.needAPause()

    def disconnect(self):
        """It clears the current serial port device."""
        if self.serial.port is not None:
            self.serial.close()
            self.serial.port = None

    def stop(self):
        """It stops the read loop an closed the connection with the serial device."""
        self.resume()
        self.disconnect()
        if self.running.is_set():
            self.running.clear()
            self.thread.join()


class Serials:
    """A class for manage multiple serial devices at the same time.

    Args:
        devices: a list of serial devices to be controled.
    """

    def __init__(self, devices: dict = {}, *args, **kwargs):
        self.devices = {}
        if len(devices) > 0:
            for name, settings in devices.items():
                if isinstance(settings, dict):
                    self.devices[name] = SerialEmitter(name=name, **settings)

    def __len__(self):
        return len(self.devices)
    
    def __getitem__(self, key):
        if key in self.devices:
            return self.devices[key]

    def hasDevices(self):
        """It checks if there is some serial device on list."""
        return len(self.devices) > 0

    def setDevices(self, devices: list = [], *args, **kwargs):
        """It updates the current serial devices list.

        Args:
            devices: serial devices list.
        """
        if self.hasDevices():
            self.stopAll()
        devices = list(set(devices))
        self.devices = [SerialEmitter(port=name, *args, **kwargs) for name in devices]

    def startAll(self):
        """It starts all serial devices"""
        for device in self.devices.values():
            device.start()

    def startOnly(self, name: str = "default"):
        """It starts only one specific serial device.

        Args:
            name: device name.
        """
        if name in self.devices:
            self.devices[name].start()

    def stopAll(self):
        """It stops all serial devices running."""
        for device in self.devices.values():
            device.stop()

    def stopOnly(self, name="default"):
        """It stops only one specific serial device.

        Args:
            name: device name.
        """
        if name in self.devices:
            self.device[name].stop()

    def pauseOnly(self, deviceName="default"):
        """It pauses a specific camera device.
        Args:
            deviceName: camera device name.
        """
        if deviceName in self.devices:
            device = self.devices[deviceName]
            device.pause()

    def pauseAll(self):
        """It pauses all camera devices."""
        for device in self.devices.values():
            device.pause()

    def resumeAll(self):
        """It resumes all camera devices."""
        for device in self.devices.values():
            device.resume()

    def resumeOnly(self, deviceName="default"):
        """It resumes a specific camera device.

        Args:
            deviceName: camera device name.
        """
        if deviceName in self.devices:
            device = self.devices[deviceName]
            device.resume()

    def getListOfPorts(self):
        """It returns a list with the availables serial port devices."""
        return [port.device for port in list_ports.comports()]

    def toJson(self, data: str = ""):
        """Converts a string to a json."""
        try: 
            return json.loads(data)
        except Exception as e:
            # print("Serials:: ", e)
            return data

    def writeTo(self, deviceName: str = "default", message: str = "", end: str = "\n", 
            asJson: bool = False
        ):
        """It writes a message to a specific serial device.

        Args:
            deviceName: name of the serial device.
            message: message to be written.
            end: newline character to be concated with the message.
            asJson: transform message to a json?
        """
        if deviceName in self.devices:
            self.device[deviceName].write(message=message, end=end, asJson=asJson)

    def write(self, message: dict = {}, end: str = "\n", asJson: bool = False):
        """It writes a message given a dict with the device name and the message.

        Args:
            message: message to be written.
            end: newline character to be concated with the message.
            asJson: transform message to a json?
        """
        for deviceName, data in message.items():
            if deviceName in self.devices:
                self.device[deviceName].write(message=data, end=end, asJson=asJson)

    def on(self, eventName: str = "", callback=None, *args, **kwargs):
        """A wrapper function for use on/emit functions. It defines a specific event
        to every serial devices listed on current instance.

        Args:
            eventName: name of the event to be signaled.
            callback: callback function
        """
        index = 0
        for device in self.devices.values():
            f = None
            # if eventName =='data':
            #     f = lambda data: callback(device.getPort(), data)
            # elif eventName == 'connection':
            #     f = lambda status: callback(device.getPort(), status)
            # elif eventName == 'ports' and index == 0:
            #     f = lambda ports: callback(device.getListOfPorts())
            #     device.on(eventName, f, *args, **kwargs)
            # if  eventName == 'ports':
            #     device.on(eventName, callback, *args, **kwargs)
            device.on(eventName, callback, *args, **kwargs)
            index += 1
