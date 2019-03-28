import music21
import numpy as np
import matplotlib.pyplot as plt

def vectorizePart(part):
    lengthInQuarters = part.duration.quarterLength
    lengthIn16th = lengthInQuarters * 4
    sequence = np.zeros((127, int(lengthIn16th)))
    measures = part.getElementsByClass('Measure')
    for measure in measures:
        for note in measure.notesAndRests:
            offset = int((note.offset + measure.offset) * 4)
            pitch = note.pitch.midi
            duration = int(note.duration.quarterLength * 4)
            for i in range(duration):
                sequence[pitch, offset + i] = 1
    return sequence

def vectorizeChorale(chorale):
    chorale = []
    for part in chorale.parts:
        chorale.append(vectorizePart(part))
    return chorale

iterator =  music21.corpus.chorales.Iterator(numberingSystem='riemenschneider')
# for chorale in iterator:
#     print(chorale.parts[0].partName)

chorale = vectorizeChorale(iterator[1])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(chorale, aspect='auto', cmap=plt.cm.get_cmap('Greys'), interpolation='nearest')
plt.show()        

# Tensor 4D:
# 1. samples: alle 368 bach chorales
# 2. parts: 4, sopran alt tenor bass
# 3. sequence: note events, vectorized in a 2d bit vector:
# [127, length of chorale in 16th]
# 127 = # of midinotes... 1 - is active 0 - note is not active


