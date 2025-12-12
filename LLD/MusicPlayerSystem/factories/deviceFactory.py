from enums.deviceType import DeviceType
from device.bluetoothSpeakerAdaptor import BluetoothSpeakerAdaptor
from device.headPhoneAdaptor import HeadphonesAdaptor
from device.wiredSpeakerAdaptor import WiredSpeakerAdaptor

from external.wiredSpeakerAPI import WiredSpeakerAPI 
from external.headphonesAPI import HeadphonesAPI 
from external.bluetoothSpeakerAPI import BluetoothSpeakerAPI

class DeviceFactory:
    @staticmethod
    def createDevice(devicetype:DeviceType):
        if devicetype==DeviceType.BLUETOOTH:
            return BluetoothSpeakerAdaptor(BluetoothSpeakerAPI())
        elif devicetype==DeviceType.WIRED:
            return WiredSpeakerAdaptor(WiredSpeakerAPI())
        else:
            return HeadphonesAdaptor(HeadphonesAPI())