import signal
import sys

from PyQt5 import QtBluetooth as QtBt
from PyQt5 import QtCore


class Application(QtCore.QCoreApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_for_devices()
        self.exec()


    def display_status(self):
        print(self.agent.isActive(), self.agent.discoveredDevices())

    def scanFinished(self, devices):
        for device in devices:
            if (device.address().toString() == "A4:DA:32:67:79:17"):
                print("bluetooth devices found !")
                self.m_control = QtBt.QLowEnergyController.createCentral(device)
                self.m_control.connected.connect(lambda : self.connected())
                self.m_control.connectToDevice()
    
    def connected(self):
        self.m_control.discoveryFinished.connect(lambda: self.services())
        self.m_control.discoverServices()

    def services(self):
        for serviceUUID in self.m_control.services():
            service = self.m_control.createServiceObject(serviceUUID)
            print(service.serviceName())
        
        self.stop()

    def stop(self):
        self.m_control.disconnect()
        sys.exit(0)

    def scan_for_devices(self):
        self.agent = QtBt.QBluetoothDeviceDiscoveryAgent(self)
        self.agent.setLowEnergyDiscoveryTimeout(5000)
        self.agent.finished.connect(lambda: self.scanFinished(self.agent.discoveredDevices()))
        self.agent.start()

if __name__ == '__main__':
    import sys
    app = Application(sys.argv)


## OLD ##

"""
from bluetooth.ble import GATTRequester


class Reader:

    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_data()

    def connect(self):
        print("Connecting...", end=" ")
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK.")

    def request_data(self):
        data = self.requester.read_by_uuid(
            "00002a00-0000-1000-8000-00805f9b34fb")[0]
        try:
            print("Device name:", data.decode("utf-8"))
        except AttributeError:
            print("Device name:", data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    Reader(sys.argv[1])
    print("Done.")
"""
