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

# Pattern: flash each LED in turn

for i in range(5): # repeat 5 times
  tree.leds_on_and_wait(L0, 0.3) # LED 0 on for 0.3 seconds
  tree.leds_on_and_wait(L1, 0.3) # LED 1 on for 0.3 seconds
  tree.leds_on_and_wait(L2, 0.3) # etc.
  tree.leds_on_and_wait(L3, 0.3)
  tree.leds_on_and_wait(L4, 0.3)
  tree.leds_on_and_wait(L5, 0.3)
  tree.leds_on_and_wait(L6, 0.3)

  
tree.all_leds_off() # extinguish all LEDs

# All done!
tree.cleanup() # call cleanup() at the end

