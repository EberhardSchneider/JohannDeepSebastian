import time
import mido

def play_file(filename, port):
    for msg in MidiFile(filename).play():
        port.send(msg)

port = mido.open_output('loopMIDI Port 3')
play_file('c:\\dev\\python\\fuge.mid')
