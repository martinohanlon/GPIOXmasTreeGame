
import threading
from time import sleep
import RPi.GPIO as GPIO

illumination_time_default = 0.001

class XmasTree(threading.Thread):

    #Pins
    
    #Model B+ or A+
    #A, B, C, D = 21, 19, 26, 20

    #Other model, probably Model A or Model B
    #A, B, C, D = 7, 9, 11, 8    

    def __init__(self, A = 21,B = 19, C = 26, D = 20):
        #setup threading
        threading.Thread.__init__(self)
        #setup properties
        self.running = False
        self.stopped = False
        self.leds = 0
        self.A, self.B, self.C, self.D = A, B, C, D

    def run(self):
        self.running = True
        #loop until its stopped
        while not self.stopped:
            for i in range(8):
                self._single_led_on(self.leds & (1<<i))
                sleep(illumination_time_default)
        #once stopped turn the leds off
        self.leds_on(0)
        self.running = False

    def stop(self):
        self.stopped = True
        #wait for it to stop running
        while self.running:
            sleep(0.01)

    def leds_on(self, leds):
        self.leds = leds
    
    def _single_led_on(self, n):

        A, B, C, D = self.A, self.B, self.C, self.D
    
        # First, set all the nodes to be input (effectively
        # 'disconnecting' them from the Raspberry Pi)  
        GPIO.setup(A, GPIO.IN)
        GPIO.setup(B, GPIO.IN)
        GPIO.setup(C, GPIO.IN)
        GPIO.setup(D, GPIO.IN)

        # Now determine which nodes are connected to the anode
        # and cathode for this LED
        if   (n==1): anode, cathode = C, A
        elif (n==2): anode, cathode = C, D
        elif (n==4): anode, cathode = D, C
        elif (n==8): anode, cathode = D, B
        elif (n==16): anode, cathode = B, D
        elif (n==32): anode, cathode = A, B
        elif (n==64): anode, cathode = B, A
        elif (n==128): anode, cathode = A, C
        else: return # invalid LED number

        # Configure the anode and cathode nodes to be outputs
        GPIO.setup(anode, GPIO.OUT)
        GPIO.setup(cathode, GPIO.OUT)

        # Make the anode high (+3.3v) and the cathode low (0v)
        GPIO.output(anode, GPIO.HIGH)
        GPIO.output(cathode, GPIO.LOW)


#test
if __name__ == "__main__":
    L0 = 1
    L1 = 2
    L2 = 4
    L3 = 8
    L4 = 16
    L5 = 32
    L6 = 64
    ALL = 1+2+4+8+16+32+64
    
    GPIO.setmode(GPIO.BCM)
    try:
        
        tree = XmasTree()
        tree.start()
        tree.leds_on(ALL)
        
        while(True):    
            sleep(0.1)

    finally:
        tree.stop()
        GPIO.cleanup()
