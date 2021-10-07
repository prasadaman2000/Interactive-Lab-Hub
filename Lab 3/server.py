from flask import Flask, request, render_template, current_app
import os
from vosk import Model, KaldiRecognizer
import sys
import wave
import json
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

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

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

app = Flask(__name__)
model = Model("model")

def clear_screen():
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)

def write_text(x, y, message, color):
    draw.text((x, y), message, font=font, fill=color)
    disp.image(image, rotation)

@app.route('/')
def index():
    return current_app.send_static_file("some_text.html")

@app.route('/saySomething/')
def say_it():
    args = request.args.to_dict()

    clear_screen()
    write_text(10, 10, "Incoming message!", "#FFFFFF")
    write_text(10, 30, "Playing message...", "#FFFFFF")

    os.system("sh arbitrary_googletts.sh \"{}\"".format(args['name']))

    os.system("sh arbitrary_googletts.sh \"Record your response now\"")

    clear_screen()
    write_text(10, 10, "RECORDING", "#FF0000")

    os.system("sh get_speech.sh")

    wf = wave.open("recorded_mono.wav", "rb")

    # You can also specify the possible word list 
    rec = KaldiRecognizer(model, wf.getframerate())

    response = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            response += result['text'] + " "

    
    clear_screen()
    write_text(10, 10, "Waiting for a message!", "#FFFFFF")

    return "Responded with: " + response

if __name__ == '__main__':
    draw.text((10, 10), "Waiting for a message!", font=font, fill="#FFFFFF")
    disp.image(image, rotation)
    app.run(debug=True, host='0.0.0.0')
