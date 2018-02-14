import codecs
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import sys
import time
import datetime

(date, time) = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S').split(' ')

# This rule changes how the main title is presented
def titleRule(newNoteTextInList):
    title = newNoteTextInList[0]
    newNoteTextInList[0] = ""
    titleSize = len(title)
    n = 100 - titleSize
    for i in range(n+1):
        if(i == int(n/2)):
            newNoteTextInList[0] = newNoteTextInList[0] + title
        elif(i == int(n/2)-1 or i == int(n/2)+1):
            newNoteTextInList[0] = newNoteTextInList[0] + " "
        else:
            newNoteTextInList[0] = newNoteTextInList[0] + "="
    return newNoteTextInList

# This rule adds a header, with date and time stamps and some basic information
def headerRule(newNoteTextInList):
    numberOfTabs = 7
    dateAndTimeLines = ["====================================================================================================",
                        "\t"*numberOfTabs + "Guilherme Bortoto de Moraes\t\tNºUSP 9360760",
                        "\t"*numberOfTabs + date + "\t\t\t\t\t\t" + time,
                        "\t"*numberOfTabs,
                        "\t"*numberOfTabs + "Notefy v0.1",
                        "====================================================================================================",
                        "\t"*numberOfTabs,
                        "\t"*numberOfTabs]
    newNoteTextInList = dateAndTimeLines + newNoteTextInList
    return newNoteTextInList

# The rules in this list will be applied in order
rules = [titleRule, headerRule]

def ShowError(errorValue):
    if(errorValue == 1):
        print("Error 1: The file is not a .txt file")
        sys.exit("Error 1")

def readFile():
    print('---readFile() called')
    Tk().withdraw()
    fileName = askopenfilename()
    print('readFile - fileName = ' + fileName)
    if(fileName.find('.txt') < 0):
        ShowError(1)
    print('readFile - The fileName is valid')
    note = codecs.open(fileName, 'r', 'UTF-8')
    print('readFile - The file has been opened, returning pointer')
    return (note, fileName.split('/')[-1])

def createFile(note, fileName):
    print('---createFile(..., ' + fileName + ') called')
    newName = date + ' ' + fileName;
    newNote = codecs.open(newName, 'w', 'UTF-8')
    print('createFile- A new file with the name "' + newName + '" has been opened, returning pointer')
    return newNote

def applyRules(newNoteTextInList):
    print('---applyRules(...) called')
    for i in range(len(rules)):
        functionName = str(rules[i]).split("<function ")[1].split(" at ")[0]
        print('Applying rule "' + functionName + '"')
        newNoteTextInList = rules[i](newNoteTextInList)
    print('applyRules - Returning newNoteTextInList')
    return newNoteTextInList

def textToLines(text):
    print('---textToLines(...) called')
    text = text.replace('\r', '')
    return text.split('\n')

def linesToText(lines):
    print('---linesToText(...) called')
    return '\n'.join(lines)

if __name__ == '__main__':
    print('Notefy v0.1')
    print('__main__ is been executed')
    (note, fileName) = readFile()
    newNote = createFile(note, fileName)

    print("__main__ - Copying the note's text to the new note")
    newNoteText = note.read()

    newNoteTextInList = textToLines(newNoteText)

    print("__main__ - Closing the original's note file")
    note.close()

    newNoteTextInList = applyRules(newNoteTextInList)

    newNoteText = linesToText(newNoteTextInList)

    print("__main__ - Writting the new text into the new note")
    newNote.write(newNoteText)

    print("__main__ - Closing the new note's file")
    newNote.close()

    print("__main__ - Done!")
