# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()
apds = APDS9960(i2c)

apds.enable_proximity = True
apds.enable_color = True

while True:
    print(apds.proximity)
    print(apds.color_data)
    time.sleep(0.2)
