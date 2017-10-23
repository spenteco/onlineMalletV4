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

def handleFolder(inputFolder):

    for f in os.listdir(inputFolder):

        fileEncoding = executeCommand('file -ib "' + inputFolder + f + '"')
        if fileEncoding.find(';') > -1:
            fileEncoding = fileEncoding.split(';')[1].strip().replace('charset=', '')
        if fileEncoding in ['binary', 'unknown-8bit', 'application/octet-stream']:
            fileEncoding = 'us-ascii' 

        try: 
            inF = codecs.open(inputFolder + f, "r", encoding=fileEncoding, errors='replace')
            inData = inF.read()
            inF.close()
        except UnicodeDecodeError:
            print 'ERROR f', f, fileEncoding, fileEncoding
            


# -------------------------------------------------------------------------------------- #
# CLEAN UP THE COMMAND LINE FOLDER NAMES
# -------------------------------------------------------------------------------------- #

def standardizeTrailingSlash(folderName):

    if folderName[len(folderName) - 1] != "/":
        folderName = folderName + "/"

    return folderName

# -------------------------------------------------------------------------------------- #
# 
# -------------------------------------------------------------------------------------- #

def main():

    if len(sys.argv) != 2:
        print "USAGE ./testEncoding.py inputFolder"
        print len(sys.argv)
        sys.exit(2)

    handleFolder(standardizeTrailingSlash(sys.argv[1]))
    
if __name__ == "__main__":
    main()




