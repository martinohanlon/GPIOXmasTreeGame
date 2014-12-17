import tree
import time

# Some constants to identify each LED
L0 = 1
L1 = 2
L2 = 4
L3 = 8
L4 = 16
L5 = 32
L6 = 64
ALL = 1+2+4+8+16+32+64
NO_LEDS = 0

tree.setup() # you must always call setup() first!

# Two slightly different ways of flashing *all* LEDs on and off.

# Way 1
for i in range(3): # repeat 3 times
  tree.leds_on_and_wait(ALL, 0.5)     # all on for 0.5s
  tree.leds_on_and_wait(NO_LEDS, 0.5) # all off for 0.5s
  
# Way 2
for i in range(3): # repeat 3 times
  tree.leds_on_and_wait(ALL, 0.5) # all on for 0.5s
  tree.all_leds_off()             # extinguish all LEDs
  time.sleep(0.5)                 # wait for 0.5s

  
tree.all_leds_off() # extinguish all LEDs

# All done!
tree.cleanup() # call cleanup() at the end

