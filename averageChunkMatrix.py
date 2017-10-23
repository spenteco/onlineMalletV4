#!/usr/bin/env python

import os, sys, time, codecs, commands

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *

# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

if len(sys.argv) != 3:
    print 'USAGE: averageChunkMatrix.py inputFile outputFile'
    print len(sys.argv)
    sys.exit(2)

inputFile = sys.argv[1]
outputFile = sys.argv[2]

inF = codecs.open(inputFile, 'r', 'utf-8') 
outF = codecs.open(outputFile, 'w', 'utf-8') 

lines = inF.read().split('\n')

headerLine = ''
fileIndex = -1
fileData = {}
percentTotals = []

for lineIndex, line in enumerate(lines):

    columns = line.split('\t')

    if len(columns) > 1:

        if lineIndex == 0:
            
            headerLine = line
            
            for cIndex, c in enumerate(columns):
                if c == 'label':
                    fileIndex = cIndex
                    break

            for a in range(cIndex + 1, len(columns)):
                percentTotals.append(0.0)

        else:

            fileNameParts = columns[fileIndex].split('_')

            unchunkedName = ''

            for a in range(0, len(fileNameParts) - 1):
                if unchunkedName > '':
                    unchunkedName = unchunkedName + '_'
                unchunkedName = unchunkedName + fileNameParts[a] 

            metadataColumns = []
            for a in range(0, fileIndex):
                metadataColumns.append(columns[a])
            
            try:
                noop = fileData[unchunkedName]
            except KeyError:

                fileData[unchunkedName] = {'numberOfFiles': 0, 'percentTotals': [], 'metadata': metadataColumns}
                
                for b in range(fileIndex + 1, len(columns)):
                    fileData[unchunkedName] ['percentTotals'].append(0.0)

            fileData[unchunkedName] ['numberOfFiles'] += 1

            for a in range(fileIndex + 1, len(columns)):
                fileData[unchunkedName] ['percentTotals'][a - fileIndex - 1] += float(columns[a])

outF.write(headerLine + '\n')

for fileName in sorted(fileData.keys()):

    outputLine = ''
    
    for c in fileData[fileName]['metadata']:
        if outputLine > '':
            outputLine = outputLine + '\t'
        outputLine = outputLine + c
        
    if outputLine > '':
        outputLine = outputLine + '\t'
    outputLine = outputLine + fileName

    for c in fileData[fileName]['percentTotals']:
        outputLine = outputLine  + '\t' + str(c / fileData[fileName]['numberOfFiles'])
    
    outF.write(outputLine + '\n')

inF.close()
outF.close()
