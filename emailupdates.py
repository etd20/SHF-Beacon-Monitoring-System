# Imports for sending Webhook
import urequests
# Imports the WiFi
from connectWiFi import WiFi

# Sends a webhook to IFTTT with a json payload
class EmailStatus:
    def __init__(self, ssid, password):
        # Creates a WiFi class that connects to the network
        self.wifi = WiFi(ssid, password)

    # Sends the Webhook with the JSON string to be emailed
    def update_beacon_status(self, beacon, beacon_status, time):
        # If WiFi is not connected, connect to WiFi provided in instance creation
        if not self.wifi.is_connected():
            # Debug message when connected over serial
            print("Beacon is not connected to the network. Automatically connecting now!")
            # Calls WiFi connection
            self.wifi.connect()
        # Name of the beacon being monitored
        value1 = beacon
        # Reason for the email being sent (Beacon not heard in 15 minutes or 24 hours has elapsed)
        value2 = beacon_status
        # What is currently happening on the beacon
        value3 = time
        # API key from IFTTT account, used to send Webhook
        api_key = 'c7tQUOZxIZP4ShAOHb9bCS'
        # JSON payload to send with email (name of the JSON is important- Webhook only triggers if JSON name matches on IFTTT)
        status_update = {'Beacon': value1, 'Update': value2, 'Reason': value3}
        # Via serial, see the JSON payload that will be sent
        print('Printing data...')
        print(status_update)
        # Formatting for API call
        request_headers = {'Content-Type': 'application/json'}
        # Sends the Webhook
        request = urequests.post(
            'https://maker.ifttt.com/trigger/status_update/json/with/key/' + api_key,
            json=status_update,
            headers=request_headers)
        # Prints the return message from IFTTT
        print(request.text)
        # Closes the connection to IFTTT
        request.close()
