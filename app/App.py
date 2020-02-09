from SearchEngine import SearchEngine
from BluetoothManager import BluetoothManager
from GraphicalUserInterface import GraphicalUserInterface

class App:

    def __init__(self):
        BluetoothManager()
        GraphicalUserInterface()
        SearchEngine("Leo&Lucas")

if __name__ == '__main__':
    app = App()
