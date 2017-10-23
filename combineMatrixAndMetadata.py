#!/usr/bin/env python

import os, sys, time, codecs, commands, re

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *

#-----------------------------------------------------------------------
#   
#-----------------------------------------------------------------------

def cleanFileName(fileName):

    fileNameParts = fileName.split('/')

    #cleanFileName = re.sub('[^a-zA-Z0-9_]', '_', fileNameParts[-1])
    cleanFileName = fileNameParts[-1]

    return cleanFileName

# -------------------------------------------------------------------------------------- #
#   ./combineMatrixAndMetadata.py /home/spenteco/projects/onlineMalletV3/onlineMalletDataRepo/results/smp_138245371584/10/smp_138245371584.matrix.csv test.csv 10
#
#   ./combineMatrixAndMetadata.py /home/spenteco/projects/onlineMalletV3/onlineMalletDataRepo/results/smp_138245308348/10/smp_138245308348.matrix.csv test.csv ''
# -------------------------------------------------------------------------------------- #

if len(sys.argv) != 4:
    print 'USAGE: combineMatrixAndMetadata.py inputFile outputFile chunkSize'
    print len(sys.argv)
    sys.exit(2)

inputFile = sys.argv[1]
outputFile = sys.argv[2]
chunkSize = sys.argv[3].strip()

inF = codecs.open(inputFile, 'r', 'utf-8') 
outF = codecs.open(outputFile, 'w', 'utf-8') 

lines = inF.read().split('\n')

fileNames = {}

for index, line in enumerate(lines):
    if index > 0:

        columns = line.split('\t')

        if len(columns) > 1:

            if chunkSize > '':

                fileNameParts = columns[0].split('_')

                unchunkedName = ''
                for a in range(0, len(fileNameParts) - 1):
                    if unchunkedName > '':
                        unchunkedName = unchunkedName + '_'
                    unchunkedName = unchunkedName + fileNameParts[a] 
                
                fileNames[unchunkedName] = {}

            else:
                fileNames[columns[0]] = {}

xrefCleanFilenames = {}
for textFile in TextFile.objects.all():
    cleanName = cleanFileName(textFile.textFileName)
    xrefCleanFilenames[cleanName] = textFile.textFileName

#print 'xrefCleanFilenames', xrefCleanFilenames

metadataTypes = []

for fileName in fileNames:

    try:

        #print
        #print 'fileName', fileName
        #print 'xrefCleanFilenames[fileName]', xrefCleanFilenames[fileName]

        textFile = TextFile.objects.filter(textFileName=xrefCleanFilenames[fileName])[0]
        metadataEntries = MetadataEntry.objects.filter(metadataTextFile=textFile)
        
        for m in metadataEntries:
            metadataTypes.append(m.metadataType.metadataType)
            fileNames[fileName][m.metadataType.metadataType] = m.metadataValue
    
    except KeyError:
        pass

metadataTypes = sorted(list(set(metadataTypes)))

for index, line in enumerate(lines):

        columns = line.split('\t')

        if len(columns) > 1:

            if index == 0:
                columns = metadataTypes + columns
            else:

                lookupFileName = columns[0]

                if chunkSize > '':

                    fileNameParts = columns[0].split('_')

                    unchunkedName = ''
                    for a in range(0, len(fileNameParts) - 1):
                        if unchunkedName > '':
                            unchunkedName = unchunkedName + '_'
                        unchunkedName = unchunkedName + fileNameParts[a] 
                    
                    lookupFileName = unchunkedName

                newColumns = []

                for m in metadataTypes:
                    try:
                        newColumns.append(fileNames[lookupFileName][m])
                    except KeyError:
                        newColumns.append(' ')  

                columns = newColumns + columns

            outline = ''
            for c in columns:
                if outline > '':
                    outline = outline + '\t'
                outline = outline + c

            outF.write(outline + '\n')

inF.close()
outF.close()
