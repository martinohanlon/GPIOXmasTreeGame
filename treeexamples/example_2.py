import tree

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

# Pattern: two or three LEDs are on at the same time.
# Note that each pair is on for 0.4 seconds

for i in range(7): # repeat the pattern 7 times
  tree.leds_on_and_wait(L1+L4, 0.4)      # LED 1 and LED 4
  tree.leds_on_and_wait(L5+L3+L0, 0.4) # LEDs 5, 3 and 0
  tree.leds_on_and_wait(L2+L6, 0.4)      # LEDs 2 and 6
  tree.leds_on_and_wait(L5+L3+L0, 0.4) # LEDs 5, 3 and 0

  
tree.all_leds_off() # extinguish all LEDs

# All done!
tree.cleanup() # call cleanup() at the end






