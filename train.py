import music21
import numpy as np
import matplotlib.pyplot as plt

def vectorizePart(part):
    lengthInQuarters = part.duration.quarterLength
    lengthIn16th = lengthInQuarters * 4
    sequence = np.zeros((int(lengthIn16th), 127))
    measures = part.getElementsByClass('Measure')
    for measure in measures:
        for note in measure.notesAndRests:
            offset = int((note.offset + measure.offset) * 4)
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

iterator =  music21.corpus.chorales.Iterator(numberingSystem='riemenschneider')
# for chorale in iterator:
#     print(chorale.parts[0].partName)

chorale = vectorizeChorale(iterator[100])
result = mergeBitVectors(chorale)
result = np.rot90(result)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(result, aspect='auto', cmap=plt.cm.get_cmap('Greys'), interpolation='nearest')
plt.show()  

    

# Tensor 4D:
# 1. samples: alle 368 bach chorales
# 2. parts: 4, sopran alt tenor bass
# 3. sequence: note events, vectorized in a 2d bit vector:
# [127, length of chorale in 16th]
# 127 = # of midinotes... 1 - is active 0 - note is not active


