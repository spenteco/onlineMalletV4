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

def handleFolder(folderName):

    for fileName in os.listdir(unicode(folderName)):

        if os.path.isdir((folderName + fileName).encode('utf-8')) == True:
            handleFolder(folderName + fileName + '/')
        else:
            if fileName.endswith('.csv'):
                
                inF = codecs.open(folderName + fileName, 'r', encoding='utf-8')
                inData = inF.read()
                inF.close()

                fileNameParts = fileName.split('.')
                newFileName = '.'.join(fileNameParts[:-1]) + '.tsv'

                if inData.find('\t') > -1:
                    print 'rename', fileName, newFileName
                    executeCommand('mv ' + folderName + fileName + ' ' + folderName + newFileName);
                else:
                    print 'rewrite', fileName, newFileName
                    executeCommand('rm ' + folderName + fileName);
                    outF = codecs.open(folderName + newFileName, 'w', encoding='utf-8')
                    outF.write(inData.replace(',', '\t'))
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

    if len(sys.argv) != 2:
        print "USAGE ./renameCsvToTsv.py inputFolder"
        print len(sys.argv)
        sys.exit(2)

    handleFolder(standardizeTrailingSlash(sys.argv[1]))
    
if __name__ == "__main__":
    main()




