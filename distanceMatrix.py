#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, codecs
from xml.dom import minidom, Node

from math import sqrt

# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

def readDocFile(fileName):
    
    print "READING", fileName

    matrix = []
    textNames = []

    rowN = 0
    fileIndex = 0

    #csvReader = csv.reader(open(fileName, 'rb'), delimiter=',', quotechar='"')
    #csvReader = unicodecsv.reader(fileName, encoding='utf-8', delimiter='\t')

    csvReader = codecs.open(fileName, 'r', encoding='utf-8').read().split('\n')

    for row in csvReader:

        if row.strip() > '':
    
            rowN = rowN + 1

            cols = row.split('\t')

            if rowN == 1:
                
                for cIndex, c in enumerate(cols):
                    if c == 'label':
                        fileIndex = cIndex
                        break
            else:

                textNames.append(cols[fileIndex])

                matrix.append(cols[fileIndex + 1: -1])

    return matrix, textNames

def calculateDistances(textNames, matrix):

    distanceTable = []

    for a in textNames:
        distanceRow = []
        for b in textNames:
            distanceRow.append(0.0)
        distanceTable.append(distanceRow)

    for a in range(0, len(textNames)):
        for b in range(0, len(textNames)):
            if a != b:

                for c in range(0, len(matrix[a])):
                    distanceTable[a][b] = distanceTable[a][b] + (abs(float(matrix[a][c]) - float(matrix[b][c])) * abs(float(matrix[a][c]) - float(matrix[b][c])))

    for a in range(0, len(textNames)):
        for b in range(0, len(textNames)):
            distanceTable[a][b] = sqrt(distanceTable[a][b])

    return distanceTable

def myDistanceMeasure(inputFileName, outputFileName):

    matrix, textNames = readDocFile(inputFileName)
    distanceTable = calculateDistances(textNames, matrix)

    outF = codecs.open(outputFileName, 'w', encoding='utf-8')

    outF.write('\t')
    for t in textNames:
        outF.write(t + '\t')
    outF.write('\n')

    for a in range(0, len(textNames)):
        outF.write(textNames[a] + '\t')
        for b in range(0, len(textNames)):
            outF.write(str(distanceTable[a][b]) + '\t')
        outF.write('\n')
    
    outF.close()
  
# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

def main():

    if len(sys.argv) != 3:
        print "USAGE ./distanceMatrix.py inputFileName outputFileName"
        print len(sys.argv)
        sys.exit(2)

    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    myDistanceMeasure(inputFileName, outputFileName)

if __name__ == "__main__":
    main()




