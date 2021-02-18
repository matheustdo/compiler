import os
import re

'''
This function receives the input folder pathname and return a list containing valid input files.
'''
def getInputFiles(pathname):
    try:
        entries = os.listdir(pathname)
        validFiles = []

        for entry in entries:
            if re.search('^entrada[0-9]+.txt$', entry): 
                validFiles.append(entry)
        
        return validFiles
    except:
        print('A pasta input/ não foi encontrada no diretório raíz.')
    
'''
This function receives a filename and read the file content.
'''
def readFile(filename): 
    file = open(filename, "r")
    print(file.read())


inputPath = 'input/'
validFiles = getInputFiles(inputPath)
readFile(inputPath + validFiles[0])