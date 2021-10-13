#!/bin/bash
arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav