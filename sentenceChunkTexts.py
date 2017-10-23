#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, codecs, math, commands
from nltk.corpus import stopwords
from nltk import *

# -------------------------------------------------------------------------------------- #
# SEQUENCE THE FILE NAMES SO THEY'RE OUTPUT IN A SENSIBLE ORDER
# -------------------------------------------------------------------------------------- #

def handleFolder(inputFolder, outputTxtFolder):

    for f in os.listdir(inputFolder):

        numberOfChunks = 0

        inF = codecs.open(inputFolder + f, "r", encoding="utf-8")
        inData = inF.read()
        inF.close()
    
        tokens = p.split(inData)

        for t in tokens:
        
            token = t.lower().strip()

            currentTxt = currentTxt + t
        
            if len(token) > 0:

                currentChunkSize = currentChunkSize + 1

                if currentChunkSize == sizeOfChunks:

                    numberOfChunks = numberOfChunks + 1
                
                    outF = codecs.open(outputTxtFolder + f + "_" + str(numberOfChunks), "w", encoding="utf-8")
                    outF.write(currentTxt + "\n")
                    outF.close()

                    currentChunkSize = 0
                    currentTxt = ""

        numberOfChunks = numberOfChunks + 1
    
        outF = codecs.open(outputTxtFolder + f + "_" + str(numberOfChunks), "w", encoding="utf-8")
        outF.write(currentTxt + "\n")
        outF.close()

        currentChunkSize = 0
        currentTxt = ""

# -------------------------------------------------------------------------------------- #
# CLEAN UP THE COMMAND LINE FOLDER NAMES
# -------------------------------------------------------------------------------------- #

def standardizeTrailingSlash(folderName):

    if folderName[len(folderName) - 1] != "/":
        folderName = folderName + "/"

    return folderName

# -------------------------------------------------------------------------------------- #
# ./sentenceChunkTexts.py manuallyTrimmedTxt/ 250 sawnTxt/ sawnStems/
# -------------------------------------------------------------------------------------- #

def main():

    if len(sys.argv) != 3:
        print "USAGE ./sentenceChunkTexts.py inputFolder outputTxtFolder"
        print len(sys.argv)
        sys.exit(2)

    handleFolder(standardizeTrailingSlash(sys.argv[1]), standardizeTrailingSlash(sys.argv[2]))
    
if __name__ == "__main__":
    main()




