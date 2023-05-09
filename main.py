# Used to call interrupts
from machine import Timer
# Used to process the incoming Morse Code signal
from SignalProcessor import SignalProcessor
# Used to email status updates and connect to the WiFi network
from emailupdates import EmailStatus
# Used to make sure garbage collection happens at opportune times
import gc

# Makes sure only one process is running
if __name__ == '__main__':
    # Over serial, notify that the program is started
    print("Running Program")
    # GPIO port that you are receiving signal on (must be ADC)
    pin_in = 26
    # What voltage is a high signal
    high = 2.93
    # Polling rate (in ms, currently not used)
    poll = 5
    # Length of 1 segment (in ms * 5)
    seg1 = 19
    # Length of 3 segments (in ms * 5)
    seg3 = 59
    # Length of 7 segments (in ms * 5)
    seg7 = 139
    # Length of end of message segment (in ms * 5)
    segend = 160
    # Name of beacon to be listening for
    beacon = "W8EDU/B"
    # Creates the Signal Processor Class
    processor = SignalProcessor(pin_in, high, poll, seg1, seg3, seg7, segend, beacon)
    # Name of the network to connect to (must be 2.4 GHz)
    ssid = 'CaseGuest'
    # Password of the network (set to None if no password)
    password = None
    # Creates the email class
    email = EmailStatus(ssid, password)

    # Callback to check the signal every 5 ms
    def check_signal(timer):
        processor.check_signal()
        
    # Callback to check beacon status every 15 minutes
    def check_email(status):
        # If the beacon is not heard in a 15 minute period
        if(processor.beacon_status() == False):
            # Reset the 24 hour check counter
            processor.reset_beacon_check()
            # Switch the LED from Blue to Red if not already Red
            if(processor.led_out_status() == True):
                processor.flip_led_out()
            # Email a status update that the beacon has not been heard in the last 15 mintues.
            email.update_beacon_status('W8EDU/B', 'Was not heard in the last 15 minutes', 'There might be a problem with the 10 GHz Beacon')
        # If the beacon has been heard in the last 15 minutes
        if(processor.beacon_status() == True):
            # Increment the beacon check status
            processor.beacon_check_increment()
            # Reset the beacon heard boolean to false
            processor.beacon_status_heard()
            # If it has been 24 hours
            if(processor.beacon_check() > 95):
                # Email the 24 hour status beacon update
                email.update_beacon_status('W8EDU/B', 'Daily status update', 'Beacon was heard every 15 minutes for the last 24 hours')
                # Reset the 24 hour check
                processor.reset_beacon_check()

    # Creates a virtual timer
    email_timer = Timer(-1)
    # Every 900,000 ms (15 minutes) check to see if the beacon has been heard
    email_timer.init(period=900000, mode=Timer.PERIODIC, callback=check_email)
    # Creates a virtual timer
    timer = Timer(-1)
    # Every 5 ms, check the receiver signal voltage
    timer.init(period=5, mode=Timer.PERIODIC, callback=check_signal)
