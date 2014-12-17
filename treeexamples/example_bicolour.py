import tree

# some constants to identify each LED
L1 = 2
L2 = 4
L3 = 8
L4 = 16
L5 = 32
L6 = 64
AMBER = 1 # LED 0 = amber
RED = 128 # LED 0 = red
GREEN = 256 # LED 0 = green
NO_LEDS = 0
BOTTOM6 = 2+4+8+16+32+64 # the 6 standard red LEDs

# note that we must tell setup() that we have a bicolour LED
tree.setup() # you must always call setup() first!

# All the red LEDs will be permanently illuminated and we rotate
# between the various colours for the bicolour LED at the top.
for i in range(7): # repeat 7 times
  tree.leds_on_and_wait(BOTTOM6, 0.8) # top LED off
  tree.leds_on_and_wait(BOTTOM6 + GREEN, 0.8) # top LED green
  tree.leds_on_and_wait(BOTTOM6 + RED,   0.8) # top LED red
  tree.leds_on_and_wait(BOTTOM6 + AMBER, 0.8) # top LED amber
  
  tree.leds_on_and_wait(NO_LEDS, 0.8) # all LEDs off
  tree.leds_on_and_wait(GREEN, 0.8) # top LED green
  tree.leds_on_and_wait(RED,   0.8) # top LED red
  tree.leds_on_and_wait(AMBER, 0.8) # top LED amber
  
tree.all_leds_off() # extinguish all LEDs

# All done!
tree.cleanup() # call cleanup() at the end

