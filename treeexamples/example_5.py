import tree
import random

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

# Two ways of randomly illuminating LEDs (they do the
# same thing but Way 1 is easier to understand whilst
# Way 2 is a shorter piece of code).

# Way 1
for i in range(100): # repeat 100 times
  random_led = random.randint(0, 6)
  if (random_led == 0):   tree.leds_on_and_wait(L0, 0.2) # D0 on for 0.2s
  elif (random_led == 1): tree.leds_on_and_wait(L1, 0.2) # D1 on for 0.2s
  elif (random_led == 2): tree.leds_on_and_wait(L2, 0.2) # D2 on for 0.2s
  elif (random_led == 3): tree.leds_on_and_wait(L3, 0.2) # D3 on for 0.2s
  elif (random_led == 4): tree.leds_on_and_wait(L4, 0.2) # D4 on for 0.2s
  elif (random_led == 5): tree.leds_on_and_wait(L5, 0.2) # D5 on for 0.2s
  elif (random_led == 6): tree.leds_on_and_wait(L6, 0.2) # D6 on for 0.2s

# Way 2
for i in range(100): # repeat 100 times
  random_led = random.randint(0, 6)
  tree.leds_on_and_wait(1<<random_led, 0.5) # randomly selected LED on for 0.2s
  
  
tree.all_leds_off() # extinguish all LEDs

# All done!
tree.cleanup() # call cleanup() at the end

