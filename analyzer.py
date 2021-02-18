import os
import re

'''
This function receives the input folder pathname and return a list containing valid input files.
'''
def getInputFiles(pathname):
    if not os.path.exists(pathname):
        print('A pasta input/ não foi encontrada no diretório raíz.')

    entries = os.listdir(pathname)
    validFiles = []

    for entry in entries:
        if re.search('^entrada[0-9]+.txt$', entry): 
            validFiles.append(entry)
    
    return validFiles
    
'''
This function receives a filename, it's output and input folder and then the file is processed.
'''
def processFile(inputFolder, outputFolder, filename): 
    inputFile = open(inputFolder + filename, "r")
    outputFile = open(outputFolder + filename, "w")

    inputContent = inputFile.read()
    outputFile.write(inputContent)

    outputFile.close()
    inputFile.close()

'''
This function inits the output folder if it is not existant
'''
def initOutputFolder(pathname): 
    if not os.path.exists(pathname):
        os.mkdir(pathname)

inputPath = 'input/'
outputPath = 'output/'
validFiles = getInputFiles(inputPath)
initOutputFolder(outputPath)

for validFile in validFiles:
    processFile(inputPath, outputPath, validFile)
