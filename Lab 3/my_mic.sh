#arecord -f cd -r 16000 -d 5 -t wav recorded.wav && sox recorded.wav recorded_mono.wav remix 1,2

#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Please count backwards from ten"

arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
python3 my_words.py recorded_mono.wav