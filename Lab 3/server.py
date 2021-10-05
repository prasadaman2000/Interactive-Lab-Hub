from flask import Flask, request, render_template, current_app
import os
from vosk import Model, KaldiRecognizer
import sys
import wave
import json

app = Flask(__name__)
model = Model("model")

@app.route('/')
def index():    
    return current_app.send_static_file("some_text.html")

@app.route('/saySomething/')
def say_it():
    args = request.args.to_dict()

    os.system("sh arbitrary_googletts.sh \"{}\"".format(args['name']))
    os.system("sh arbitrary_googletts.sh \"Record your response now\"")
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

    return "Responded with: " + response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
