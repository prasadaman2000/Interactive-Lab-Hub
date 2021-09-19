import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
import datetime
from mycode.Shape import create_shape
import random

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

def get_current_time():
    curtime = datetime.datetime.now()
    hour = curtime.hour
    minute = curtime.minute

    return(hour // 10, hour % 10, minute // 10, minute % 10)

def get_random_color():
    return ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0]

    return color565(c1, c2, c3)

oldhour1, oldhour2, oldmin1, oldmin2 = -1, -1, -1, -1

while True:
    hour1, hour2, min1, min2 = get_current_time()

    # print(get_current_time())

    if hour1 != oldhour1:
        oldhour1 = hour1
        h1 = create_shape(hour1, 20, (50, 30), get_random_color())
    
    if hour2 != oldhour2:
        oldhour2 = hour2
        h2 = create_shape(hour2, 20, (130, 30), get_random_color())
    
    if min1 != oldmin1:
        oldmin1 = min1
        m1 = create_shape(min1, 20, (90, 110), get_random_color())
    
    if min2 != oldmin2:
        oldmin2 = min2
        m2 = create_shape(min2, 20, (170, 110), get_random_color())

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    h1.render_shape(draw)
    h2.render_shape(draw)
    m1.render_shape(draw)
    m2.render_shape(draw)

    h1.rotate(0.02)
    h2.rotate(0.02)
    m1.rotate(0.02)
    m2.rotate(0.02)

    # Display image
    disp.image(image, rotation)
    # time.sleep(0.1)
