import time
import board
import busio
from my_utils.EdgeDetector import EdgeDetector
from my_utils.Button import CapacitorButton

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
cap_button = CapacitorButton(boardObj=mpr121, idx=0)
cap_edge = EdgeDetector(cap_button, lazy=False)

try:
    while True:
    # print(cap_button.get_value())
        print(cap_edge.num_edges())
        time.sleep(2)

except KeyboardInterrupt:
    cap_edge.delete()
