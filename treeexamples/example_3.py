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

# Pattern: all LEDs illuminated except for one each time

for i in range(3): # repeat 3 times
  tree.leds_on_and_wait(ALL-L0, 0.5) # all on except for LED 0
  tree.leds_on_and_wait(ALL-L1, 0.5) # all on except for LED 1
  tree.leds_on_and_wait(ALL-L2, 0.5) # etc.
  tree.leds_on_and_wait(ALL-L3, 0.5)
  tree.leds_on_and_wait(ALL-L4, 0.5)
  tree.leds_on_and_wait(ALL-L5, 0.5)
  tree.leds_on_and_wait(ALL-L6, 0.5)

  
tree.all_leds_off() # extinguish all LEDs

# All done!
tree.cleanup() # call cleanup() at the end

