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

def handleFolder(inputFolder, lowDf, highDf, outputFolder):

    numberOfTexts = 0
    tokenDf = {}

    p = re.compile(u"(\s|,|\.|;|:|-|\"|\?|!|\(|\)|\'|»|«)")

    for f in os.listdir(inputFolder):

        #print 'reading', f

        numberOfTexts += 1

        fileEncoding = executeCommand('file -ib "' + inputFolder + f + '"')
        if fileEncoding.find(';') > -1:
            fileEncoding = fileEncoding.split(';')[1].strip().replace('charset=', '')
        if fileEncoding in ['binary', 'unknown-8bit', 'application/octet-stream']:
            fileEncoding = 'us-ascii' 

        inF = codecs.open(inputFolder + f, "r", encoding=fileEncoding, errors='replace')
        inData = inF.read()
        inF.close()
    
        distinctTokens = list(set(p.split(inData)))

        for t in distinctTokens:
            try:
                tokenDf[t.lower()] += 1
            except KeyError:
                tokenDf[t.lower()] = 1

    lowDfN = float(lowDf) / 100;
    highDfN = float(highDf) / 100;

    tokensToDelete = {}

    for t, count in tokenDf.iteritems():

        if float(count) / float(numberOfTexts) < lowDfN:
            tokensToDelete[t] = 1

        if float(count) / float(numberOfTexts) > highDfN:
            tokensToDelete[t] = 1

    #print 'len(tokensToDelete)', len(tokensToDelete)

    for f in os.listdir(inputFolder):

        numberOfTexts += 1

        inF = codecs.open(inputFolder + f, "r", encoding="utf-8")
        inData = inF.read()
        inF.close()

        outF = codecs.open(outputFolder + f, "w", encoding="utf-8")
    
        tokens = p.split(inData)

        for t in tokens:
            try:
                noop = tokensToDelete[t.lower()]
            except KeyError:
                outF.write(t + '\n')

        outF.close()

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

    if len(sys.argv) != 5:
        print "USAGE ./dfTrim.py inputFolder lowDf highDf outputTxtFolder"
        print len(sys.argv)
        sys.exit(2)

    handleFolder(standardizeTrailingSlash(sys.argv[1]), sys.argv[2], sys.argv[3], standardizeTrailingSlash(sys.argv[4]))
    
if __name__ == "__main__":
    main()




