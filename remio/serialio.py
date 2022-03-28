from serial import Serial
from serial.tools import list_ports
from threading import Thread, Event
from typing import Union
import time
from .sevent import Emitter


class SerialEmitter(Emitter):
    """A custom serial class threaded and event emit based.
    
    Args:
        reconnectDelay: wait time between reconnection attempts.
        maxAttempts: max read attempts.
        portsRefreshTime: time for check serial devices changes.
        emitterIsEnabled: disable on/emit events (callbacks execution)
    
    Events: 
        data-incoming: incoming(data: str).
        connection-status: update(status: bool).

    """
    def __init__(self, 
            reconnectDelay: Union[int, float] = 1, 
            maxAttempts: int = 10, 
            portsRefreshTime: int = 1,
            emitterIsEnabled: bool = True,
            *args, 
            **kwargs):
        super().__init__(*args, **kwargs)
        self.port = kwargs.pop('port', None)
        self.reconnectDelay = reconnectDelay
        self.maxAttempts = maxAttempts
        self.portsRefreshTime = portsRefreshTime
        self.serial = Serial(*args, **kwargs)
        self._thread = Thread(target=self.run)
        self._runningEvent = Event()
        self.lastConnectionState = False
        self.attempts = 0
        self.time = 0
        self.lastDevicesList = []
    
    def __setitem__(self, key, value):
        if self.serial.isOpen():
            self.serial.close()
        setattr(self.serial, key, value)

    def getPort(self):
        """It returns the current port device."""
        return self.serial.port
    
    def hasDevice(self):
        """It checks if a serial device is setted."""
        return self.serial.port is not None

    def isOpen(self):
        """It checks if serial port device is open."""
        return self.serial.isOpen()

    def attemptsLimitReached(self):
        """Check if read attempts have reached their limit."""
        return self.attempts >= self.maxAttempts

    def start(self):
        """It starts read loop."""
        self._runningEvent.set()
        self._thread.start()

    def getListOfPorts(self):
        """It returns a list with the availables serial port devices."""
        return [port.device for port in list_ports.comports()]

    def connect(self):
        """It will try to connect with the specified serial device."""
        try:
            self.lastConnectionState = self.serial.isOpen()

            if self.serial.isOpen():
                self.serial.close()

            if self.serial.port is not None and self.port is not None:
                self.seria.port = self.port

            self.serial.open()

        except Exception as e:
            print('connection error: ',e)

    def write(self, message:str='', end='\n'):
        """It writes a message to the serial device.

        Args:
            message: string to be sent.
            end: newline character to be concated with the message.
        """
        if self.serial.isOpen():
            try:
                if len(message) > 0:
                    message += end
                    message = message.encode()
                    self.serial.write(message)
            except Exception as e:
                print('Write error: ', e)

    def readData(self):
        """It will try to read incoming data."""
        try:
            data = self.serial.readline().decode().rstrip()
            if len(data) > 0:
                self.emit('data-incoming', data)
                return data
        except Exception as e:
            print('Read data error: ', e)
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
                    self.emit('ports-update',  actualDevicesList)
                self.time = 0

    def run(self):
        """Here the run loop is executed."""
        while self._runningEvent.is_set():
            t0 = time.time()

            if self.lastConnectionState != self.serial.isOpen():
                self.emit('connection-status', self.serial.isOpen())
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

    def disconnect(self):
        """It clears the current serial port device."""
        if self.serial.port is not None:
            self.serial.close()
            self.serial.port = None

    def stop(self):
        """It stops the read loop an closed the connection with the serial device."""
        self._runningEvent.clear()
        self.serial.close()


class Serials:
    """A class for manage multiple serial device at the same time.

    Args:
        devices: a list of serial devices to be controled.
    """
    def __init__(self, devices: dict = {}, *args, **kwargs):
        self.devices = {}
        if len(devices) > 0:
            for name, settings in devices.items():
                if isinstance(settings, dict):
                    self.devices[name] = SerialEmitter(**settings)

    def __len__(self):
        return len(self.devices)

    def hasDevices(self):
        """It checks if there is some serial device on list."""
        return len(self.devices) > 0

    def setDevices(self, devices:list=[], *args, **kwargs):
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
        print('Iniciado serial')
        for device in self.devices.values():
            device.start()

    def startOnly(self, name:str='default'):
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
    
    def stopOnly(self, name='default'):
        """It stops only one specific serial device.
        
        Args:
            name: device name.
        """
        if name in self.devices:
            self.device[name].stop()

    def getListOfPorts(self):
        """It returns a list with the availables serial port devices."""
        return [port.device for port in list_ports.comports()]

    def write(self, to: str = 'default', message: str='' , end: str = '\n'):
        """It writes a message to a specific serial device.

        Args:
            to: name of the serial device.
            message: message to be written.
            end: newline character to be concated with the message.
        """
        if to in self.devices:
            self.device[to].write(message=message, end=end)

    def on(self, eventName: str="", callback=None, *args, **kwargs):
        """A wrapper function for use on/emit functions. It defines a specific event
        to every serial devices listed on current instance.
        
        Args:
            eventName: name of the event to be signaled.
            callback: callback function
        """
        index = 0
        for device in self.devices.values():
            f = None
            if eventName =='data-incoming':
                f = lambda data: callback(device.getPort(), data)
            elif eventName == 'connection-status':
                f = lambda status: callback(device.getPort(), status)
            elif eventName == 'ports-update' and index == 0:
                f = lambda ports: callback(device.getListOfPorts())
                device.on(eventName, f, *args, **kwargs)
            if f is not None and eventName != 'ports-update':   
                device.on(eventName, f, *args, **kwargs)
            
            index += 1
                