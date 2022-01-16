import mido
from time import sleep


hexNoteList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g'] # converted to base 16
inport = mido.open_input("Clock", virtual=True)
outport = mido.open_output()

counter1 = 0
counter2 = 0

def binaryRead(fname):  # function for extracting hex values from text or image
    with open(fname, 'rb') as file:
        rf = bytearray(file.read())
        hexList = [hex(i) for i in rf]
        improvedHex = [t.strip('0x') for t in hexList]
        return improvedHex


data = binaryRead()
dataList = []

for d in range(len(data)):
    newData = data[d]
    for char in range(len(newData)):
        dataList.append(newData[char])


for message in inport:
    counter1 += 1
    if (counter1 == 6) or (message.type == "start"):
        counter1 = 0
        counter2 += 1
        midiNote = hexNoteList.index(dataList[counter2 - 1])
        noteOn = mido.Message("note_on", channel=0, note=midiNote)
        noteOff = mido.Message("note_off", channel=0, note=midiNote)
        outport.send(noteOn)
        sleep(.05)
        outport.send(noteOff)
    if counter2 == dataList:
        counter2 = 0
    if message.type == "stop":
        counter1 = 0
        counter2 = 0