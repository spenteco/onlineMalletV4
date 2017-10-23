#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, codecs, math, commands
from nltk.corpus import stopwords
from nltk import *

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

def executeCommand(cmd):

    results = commands.getoutput("export PYTHONIOENCODING=UTF-8; " + cmd)

    return results

# -------------------------------------------------------------------------------------- #
# SEQUENCE THE FILE NAMES SO THEY'RE OUTPUT IN A SENSIBLE ORDER
# -------------------------------------------------------------------------------------- #

def handleFolder(inputFolder, sizeOfChunks, outputTxtFolder):

    p = re.compile(u"(\s|,|\.|;|:|-|\"|\?|!|\(|\)|\'|»|«)")

    for f in os.listdir(inputFolder):

        numberOfChunks = 0

        currentChunkSize = 0
        currentTxt = ""
        currentStem = ""

        fileEncoding = executeCommand('file -ib "' + inputFolder + f + '"')
        if fileEncoding.find(';') > -1:
            fileEncoding = fileEncoding.split(';')[1].strip().replace('charset=', '')
        if fileEncoding in ['binary', 'unknown-8bit', 'application/octet-stream']:
            fileEncoding = 'us-ascii' 

        inF = codecs.open(inputFolder + f, "r", encoding=fileEncoding, errors='replace')
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
# ./chunkTexts.py manuallyTrimmedTxt/ 250 sawnTxt/ sawnStems/
# -------------------------------------------------------------------------------------- #

def main():

    if len(sys.argv) != 4:
        print "USAGE ./chunkTexts.py inputFolder sizeOfChunks outputTxtFolder"
        print len(sys.argv)
        sys.exit(2)

    handleFolder(standardizeTrailingSlash(sys.argv[1]), int(sys.argv[2]), standardizeTrailingSlash(sys.argv[3]))
    
if __name__ == "__main__":
    main()




