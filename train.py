import music21
import numpy as np
import matplotlib.pyplot as plt
import mido
import time

def play(midi):
    port = mido.open_output('loopMIDI Port 3')
    for msg in midi:
        port.send(msg)
    port.close()

def play_file(filename, port):
    port = mido.open_output('loopMIDI Port 3')
    for msg in mido.MidiFile(filename).play():
        port.send(msg)
    port.close()



def vectorizePart(part):
    lengthInQuarters = part.duration.quarterLength
    lengthIn16th = lengthInQuarters * 4
    sequence = np.zeros((int(lengthIn16th), 127))
    measures = part.getElementsByClass('Measure')
    for measure in measures:
        for note in measure.notesAndRests:
            offset = int((note.offset + measure.offset) * 4)
            if hasattr(note, 'pitch'):
                # this is a note and not a rest
                pitch = note.pitch.midi
                duration = int(note.duration.quarterLength * 4)
                for i in range(duration):
                    sequence[offset + i, pitch] = 1
    return sequence

def vectorizeChorale(chorale):
    result = []
    for part in chorale.parts:
        result.append(vectorizePart(part))
    return result

def mergeBitVectors(vectors):
    result = np.zeros((len(vectors[0]), 127 ))
    for v in range(len(vectors)):
        for i in range(len(vectors[v])):
            for j in range(127):
                result[i][j] = v+1 if vectors[v][i][j] != 0 else result[i][j]
    return result

def playVector(vector):
    port = mido.open_output('loopMIDI Port 3')
    active_notes = set()
    for step in vector:
        for note in range(127):
            if step[note] != 0 and not note in active_notes:
                port.send(mido.Message('note_on', note=note))
                active_notes.add(note)
            elif step[note] == 0 and note in active_notes:
                port.send(mido.Message('note_off', note=note))
                active_notes.discard(note)
        time.sleep(.2)    
    port.close()

def prepare_data():
    chorales = []
    clist = music21.corpus.chorales.ChoraleList()
    for c in clist.byBWV:
        ch = music21.corpus.parse('bach/bwv' + str(c))
        v = vectorizeChorale(ch)
        vmerged = mergeBitVectors(v)
        chorales.append(vmerged)
    print(chorales)

prepare_data()

# chorale = vectorizeChorale(iterator[100])
# result = mergeBitVectors(chorale)
# playVector(result)



# result = np.rot90(result)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.imshow(result, aspect='auto', cmap=plt.cm.get_cmap('Greys'), interpolation='nearest')
# plt.show()  




    

# Tensor 4D:
# 1. samples: alle 368 bach chorales
# 2. parts: 4, sopran alt tenor bass
# 3. sequence: note events, vectorized in a 2d bit vector:
# [127, length of chorale in 16th]
# 127 = # of midinotes... 1 - is active 0 - note is not active


