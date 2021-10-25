import time
import board
import busio
import os
import random

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c) # mpr121[i].value -> capacitor board value

import adafruit_ssd1306

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
# oled.pixel, oled.draw -> look in oled_test.py for examples
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
oled.fill(0)

from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()
apds = APDS9960(i2c)
# Proximity sensor
apds.enable_proximity = True
apds.enable_color = True
# apds.enable_gesture = True

from adafruit_apds9960 import colorutility

# check out my code in ./my_utils
from my_utils.EdgeDetector import EdgeDetector
from my_utils.Button import CapacitorButton
cap_button = CapacitorButton(boardObj=mpr121, idx=0)
cap_edge = EdgeDetector(cap_button, lazy=False)

# messages to choose from
rude_messages = ["don't spam me", "would you like it if i poked you this much", "stop poking me or i will tell the professor to fail you", "stop poking me you annoying child"]
too_bright_messages = ["It's so bright, don't waste electricity", "I know it's bright outside, don't turn on a light", "It is not a good time to turn on the light", "It's so bright, I don't have eyes and I can see"]
dark_messages = ["you should turn on a light", "don't strain your eyes, turn on a light", "Don't you know it's dark?"]

# catch ctrl-c
try:
    while True:
        # get annoyed
        if cap_edge.num_edges() >= 3:
            os.system(f"sh arbitrary_googletts.sh \"{random.choice(rude_messages)}\"")
            # reset edges for next iteration of while loop
            cap_edge.reset_edges()

        # answer "query"
        elif cap_edge.num_edges() >= 1:
            cap_edge.reset_edges()
            os.system(f"sh arbitrary_googletts.sh \"Should you turn on a light?\"")

            r, g, b, _ = apds.color_data
            lux = colorutility.calculate_lux(r, g, b)

            if lux > 5:
                os.system(f"sh arbitrary_googletts.sh \"{random.choice(too_bright_messages)}\"")
            else:
                os.system(f"sh arbitrary_googletts.sh \"{random.choice(dark_messages)}\"")
            # os.system(f"sh arbitrary_googletts.sh \"{dark_messages[2]}\"")


        time.sleep(0.1)

except KeyboardInterrupt:
    cap_edge.delete()
    oled.fill(0)
    oled.show()
