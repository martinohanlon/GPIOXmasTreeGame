# Example code for [charlieplexed] GPIO Xmas Tree for 
# Raspberry Pi by Andrew Gale.

import RPi.GPIO as GPIO
import time

# The tree connects to the 6 GPIO pins furthest away from the
# corner of Raspberry Pi i.e. *physical* pin numbers 21-26 on
# the model A or B and 35-40 on the B+.

# Some Kickstarter supporters opted to receive a 'bi-colour'
# LED as their stretch goal reward. This fits in the top
# LED position (i.e. LED_0) but actually contains a second
# LED that we shall call LED_7

# Bicolour LED fitted or not?
bicolour_fitted = False # the default is False

# The time for which each LED is illuminated.
# This is the place to tweak the brightness of the bicolour
# LEDs by altering their illumination time.
illumination_time_bicolour_green = 0.004 # the ON time for the bicolour green LED
illumination_time_bicolour_red = 0.004 # the ON time for the bicolour red LED
illumination_time_default = 0.001 # the ON time for all the other LEDs

# The following constants will be configured by tree.setup()
# but we will set them to -1 for now.
A, B, C, D = -1, -1, -1, -1  # The four Charlieplexing nodes
total_illumination_time = -1 # Time for one whole cycle

# The following code to detect which version of Raspberry Pi
# you are using is courtesy of Matt Hawkins at
# http://www.raspberrypi-spy.co.uk

def getrevision():
  # Extract board revision from cpuinfo file
  myrevision = "0000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:8]=='Revision':
        length=len(line)
        myrevision = line[11:length-1]
    f.close()
  except:
    myrevision = "0000"
 
  return myrevision



def single_led_on(n):
  if (A==-1):
    print "***********************************************"
    print "**                                           **"
    print "** ERROR: you MUST call tree.setup() first!! **"
    print "**                                           **"
    print "***********************************************"
    raise Exception('You MUST call tree.setup() first!!')
    
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
 
  
def leds_on_and_wait(leds, wait_time):
  # This routine is passed an 8-bit value (in the "leds"
  # parameter) with one bit representing each LED. This routine
  # checks each bit in turn and, if it's set to '1' then it
  # turns the LED on for 0.001 seconds (or whatever is defined
  # in the constants at the top). The whole routine
  # loops around as many times as it can in the time specified
  # in the "wait_time" parameter, thereby creating the illusion
  # that all LEDs are on simultaneously (due to persistence
  # of vision) when, in reality, only one is on at a time.
  
  # When used with a bicolour LED at the top of the tree, this
  # routine is passed a 9-bit value.
  # Bit 7 is for the red LED in the bicolour LED.
  # Bit 8 is for the green LED in the bicolour LED.
  # Bit 0: to maintain compatibility with code for a non-bicolour version of
  # the tree, if bit 0 is set then we want the bicolour LED to light BOTH LEDs
  # to mimic the yellow of the non-bicolour version of the tree.
  
  if (bicolour_fitted):
    if (leds & 1):
      # bit 0 is set, so display bicolour as amber/yellow
      leds = (leds & 0b001111110) # preserve the 6 standard red LED bits
      leds |= (128+1) # enable the red and green bicolour LEDs
    elif (leds & 128):
      # bit 7 is set so display bicolour as red
      leds = (leds & 0b001111110) # preserve the 6 standard red LED bits
      leds |= 128 # enable the red bicolour LEDs
    elif (leds & 256):
      # bit 8 is set so display bicolour as green
      leds = (leds & 0b001111110) # preserve the 6 standard red LED bits
      leds |= 1 # enable the green bicolour LEDs
      
  for j in range(int(wait_time/total_illumination_time)):
    for i in range(8):
      single_led_on(leds & (1<<i))
      
      if (bicolour_fitted and i==0):
        time.sleep(illumination_time_bicolour_green)
      elif (bicolour_fitted and i==7):
        time.sleep(illumination_time_bicolour_red)
      else:
        time.sleep(illumination_time_default)
      
        
def all_leds_off():
  single_led_on(0)
  
def setup():
  global A
  global B
  global C
  global D
  global total_illumination_time
  
  GPIO.setmode(GPIO.BCM)
  
  # choose the correct GPIO pins depending on model
  revision = getrevision()
  #print "** revision: ", revision
  if ((revision == "0010") or (revision == "0012")):
    #print "Model B+ or A+"
    A, B, C, D = 21, 19, 26, 20
  else:
    #print "Other model, probably Model A or Model B"
    A, B, C, D = 7, 9, 11, 8
  #A, B, C, D = 7, 9, 11, 8
  
  if (bicolour_fitted):
    total_illumination_time = 6 * illumination_time_default
    total_illumination_time += illumination_time_bicolour_green
    total_illumination_time += illumination_time_bicolour_red
  else:
    total_illumination_time = 8 * illumination_time_default
    
  #print "total_illumination_time: ", total_illumination_time
  
def cleanup():
  GPIO.cleanup()
  
