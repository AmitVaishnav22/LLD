from enums.deviceType import DeviceType
from factories.deviceFactory import DeviceFactory

class DeviceManager:
    _instance=None
    def __init__(self):
        self._current_output_device=None
    
    @staticmethod
    def getInstance():
        if DeviceManager._instance is None:
            DeviceManager._instance=DeviceManager()
        return DeviceManager._instance
    
    def connect(self,devicetype:DeviceType):
        self._current_output_device=DeviceFactory.createDevice(devicetype)
        if devicetype == DeviceType.BLUETOOTH:
            print("Bluetooth device connected")
        elif devicetype == DeviceType.WIRED:
            print("Wired device connected")
        elif devicetype == DeviceType.HEADPHONES:
            print("Headphones connected")
    
    def getOutputDevice(self):
        if self._current_output_device is None:
            raise RuntimeError("No output device is connected.")
        return self._current_output_device
    
    def hasOutPutDevice(self):
        return self._current_output_device is not None