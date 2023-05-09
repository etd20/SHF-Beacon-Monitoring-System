# Imports the network
import network

# WiFi class that connects to the provided network with the provided password and can check if it's currently connected to a network
class WiFi:
    # Initializes the class with the ssid and password
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        # Gets the WiFi chip ready
        self.station = network.WLAN(network.STA_IF)

    # Connects to the provided network
    def connect(self):
        # Turns on the WiFi
        self.station.active(True)
        # Connects to the provided network
        self.station.connect(self.ssid, self.password)
        # While connecting, don't do anything else
        while not self.station.isconnected():
            # Over serial, notify that the network is being connected to
            print('Connecting to network...')
        # Notifies over serial that the connection is successful
        print('Connection successful')

    # Checks if the Pico W is connected to the network, True if it is, False if it is not
    def is_connected(self):
        return self.station.isconnected()