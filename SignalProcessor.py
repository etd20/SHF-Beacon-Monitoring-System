# Used to talk with ADC
import machine
# Used to set LED status on board
from machine import Pin
# Used to decode Morse Code
from CW import CW
# Used to make sure garbage collection happens at good times
import gc

# Takes an incoming CW signal and decodes it
class SignalProcessor:
    def __init__(self, pin_in, high, poll, seg1, seg3, seg7, segend, beacon):
        # Creates an ADC on pin_in
        self.signal = machine.ADC(pin_in)
        # Sets the beacon indicator to GPIO pin 22 (Blue LED)
        self.beacon_blue = Pin(22, Pin.OUT)
        # Sets the fault indicator to GPIO pin 21 (Red LED)
        self.fault_red = Pin(21, Pin.OUT)
        # Sets the red value to high
        self.fault_red.value(2.5)
        # Sets the blue value to low
        self.beacon_blue.value(0)
        # If False, Red LED on, if True, Blue LED on
        self.led_out = False
        # Voltage barrier where signal is considered high when above and low when at or below
        self.high = high
        # Polling rate in ms (not currently used)
        self.poll = poll
        # Length of a one unit segment (math: seg * callback length = unit length) (ex: 20 * 5ms = 100 ms unit segment)
        self.seg1 = seg1
        # Length of a three unit segment
        self.seg3 = seg3
        # Length of a 7 unit segment
        self.seg7 = seg7
        # Receiver voltage value
        self.value = 0
        # Length of the end of a message (when should a signal be considered done)
        self.segend = segend
        # Increments count, every 1 count is = to callback length (aka 5 ms)
        self.count = 0
        # Length of a signal segment (Ex: 1 = 100ms, 3 = 300ms, 7 = 700ms)
        self.segment = 0
        # Was the last poll a high signal
        self.highsig = False
        # Was the last poll a low signal
        self.lowsig = False
        # Name of beacon we are monitoring
        self.beacon = beacon
        # Creates an empty string to append incoming CW characters to
        self.cw = ""
        # Are we processing a new signal
        self.newsignal = True
        # Are we currently processing a signal
        self.processsignal = False
        # Have we heard the beacon in a recieved CW signal
        self.beaconstatus = False
        # How many times has the beacon online check been done
        self.beaconchecks = 0

    # Checks incoming signal value
    def check_signal(self):
        # Gets the value from the ADC and changes it to voltage
        self.value = self.signal.read_u16() / 21845
        # If the value is above the threshold for high
        if (self.value > self.high):
            # Go to the high process logic
            self.process_high()
        # IF the value is below or equal to high and we have started processing a signal
        if (self.value <= self.high and self.processsignal == True):
            # Go to the low process logic
            self.process_low()
        # If the value is below or equal to high and we have not started processing a signal
        if (self.value <= self.high and self.processsignal == False):
            # If the memory free in the system is below 70,000
            if(gc.mem_free() < 70000):
                # Call garbage collect
                gc.collect()

    # Logic used to process a high signal
    def process_high(self):
        # If the last segment was a low signal
        if (self.lowsig == True):
            # Set the lowsig bool to false
            self.lowsig = False
            # If this is not the first part of a new signal
            if (self.newsignal != True):
                # Add a space depending on the received segment length
                self.add_space(self.segment)
            # If this is the first part of a true signal
            if (self.newsignal == True):
                # Set newsignal to false
                self.newsignal = False
            # Reset segment count logic to 0
            self.count = 0
            self.segment = 0
        # If count is less than one unit
        if (self.count <= self.seg1):
            # Increment the counter
            self.count += 1
        # If the count is greater than one unit but less than 3 units
        if (self.seg1 < self.count <= self.seg3):
            # Sets the segment number to 3
            self.segment = 1
            # Increment the counter
            self.count += 1
        # If the count is greater than 3 units
        if (self.count > self.seg3):
            # Set the segment to 3
            self.segment = 3
            # Increment the counter
            self.count += 1
        # Sets the last signal as a high signal
        self.highsig = True
        # Sets that we are processing a signal
        self.processsignal = True
        
    # Logic used to process a low signal
    def process_low(self):
        # If we are processing a signal
        if (self.processsignal == True):
            # If the last poll was a high signal
            if (self.highsig == True):
                # Set the last poll being high to false
                self.highsig = False
                # Adds the element to be decoded to the string
                self.add_char(self.segment)
                # Resets the segment and count logic
                self.count = 0
                self.segment = 0
            # If the signal is less than one unit
            if (self.count <= self.seg1):
                # Increment the counter
                self.count += 1
            # If the signal is greater than one unit or less than 3 units
            if (self.seg1 < self.count <= self.seg3):
                # Increment the counter
                self.count += 1
                # Set segment length to one
                self.segment = 1
            # If the segment length is greater than three units and less than seven units
            if (self.seg3 < self.count <= self.seg7):
                # Increment the counter by one
                self.count += 1
                # Set the segment length to three
                self.segment = 3
            # If the segment length is greater than seven and less than the end of a message length
            if (self.seg7 < self.count < self.segend):
                # Increment the counter
                self.count += 1
                # Set the segment length to seven
                self.segment = 7
            # If the counter is equal to the end of a message length
            if (self.count == self.segend):
                # Add the final element space
                self.add_space(self.segment)
                # Call the CW decode and beacon check logic
                self.process_signal()
            # Sets the last poll being low true
            self.lowsig = True
        
    # Adds a . or - to the CW string to be decoded based on unit length
    def add_char(self, segment):
        # If the unit length is 1 segment
        if (segment == 1):
            # Add a .
            self.cw = self.cw + "."
        # If the unit length is 3 segments
        if (segment == 3):
            # Add a -
            self.cw = self.cw + "-"

    # Adds a space depending on unit length
    def add_space(self, segment):
        # If the unit length is 1, add no space
        if (segment == 1):
            # Adds no space
            self.cw = self.cw + ""
        # If the unit length is 3, add a space
        if (segment == 3):
            # Add a space
            self.cw = self.cw + " "
        # If the unit length is 7, add a space
        if (segment == 7):
            # adds a space
            self.cw = self.cw + " "
            
    # Processes the recieved morse code signal
    def process_signal(self):
        # Resets the count and segment logic
        self.count = 0
        self.segment = 0
        # Prints the CW string to console via serial
        print(self.cw)
        # Sets that we are looking for a new signal
        self.newsignal = True
        # Sets that we are no longer processing a signal
        self.processsignal = False
        # Create a CW decode object
        cwdecode = CW()
        # Pass the CW message to be decoded to the CW decoder
        message = cwdecode.decrypt(self.cw)
        # Clear the incoming CW buffer
        self.cw = ""
        # Print the decoded CW message to console via serial
        print(message)
        # If the decoded CW message is the beacon we are listening for
        if (message == self.beacon):
            # Print to console that we have heard the beacon
            print("Beacon has been heard!")
            # Sets that we have heard the beacon to true
            self.beaconstatus = True
            # If the LED is currently Red
            if(self.led_out == False):
                # Flips the LEDs from Red to Blue
                self.flip_led_out()
        # If we have not heard the beacon
        if (message != self.beacon):
            # Print to console that the signal heard is not the beacon.
            print("Heard signal is not Beacon!")
        # Delete the CW decoder object
        del cwdecode
        # Run garbage collection to recollect memeory
        gc.collect()
        
    # Returns true if the beacon has been heard, false if not
    def beacon_status(self):
        return self.beaconstatus
    
    # Sets the heard beacon status to false
    def beacon_status_heard(self):
        self.beaconstatus = False
    
    # Returns the number of times we have heard the beacon when checked every 15 minutes
    def beacon_check(self):
        return self.beaconchecks
    
    # Increments the number of times we have heard the beacon in a 15 minute period by one
    def beacon_check_increment(self):
        self.beaconchecks = self.beaconchecks + 1
        
    # Resets the number of times we have heard the beacon
    def reset_beacon_check(self):
        self.beaconchecks = 0
        
    # Flips the LED's from Red to Blue and Blue to Red
    def flip_led_out(self):
        if self.led_out == False:
            self.beacon_blue.value(3)
            self.fault_red.value(0)
        if self.led_out == True:
            self.beacon_blue.value(0)
            self.fault_red.value(2.5)
        self.led_out = not self.led_out
        
    # Returns the current status of the indicator LEDS, Blue if True, Red if False
    def led_out_status(self):
        return self.led_out
            