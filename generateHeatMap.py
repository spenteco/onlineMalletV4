#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, codecs, csv
import numpy

# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

def readDocFile(fileName):
    
    print 'READING', fileName

    matrix = []
    textNames = []

    rowN = 0
    fileIndex = 0

    csvReader = csv.reader(open(fileName, 'rb'), delimiter=',', quotechar='"')
    for row in csvReader:
    
        rowN = rowN + 1

        if rowN > 1:

            textNames.append(row[0])

            matrix.append(row[1: -1])

    return matrix, textNames

def generateHeatMap(inputFileName, outputFileName):

    matrix, textNames = readDocFile(inputFileName)

    allValues = []
    for a in matrix:
        for b in a:
            allValues.append(float(b))

    avg = numpy.average(numpy.array(allValues))
    std = numpy.std(numpy.array(allValues))

    outputLine = ''

    for a in range(0, len(matrix)):
        outputLine = outputLine + '<tr>'
        for b in range(0, len(matrix)):

            textA = textNames[a]
            textB = textNames[b]

            distance = float(matrix[a][b])

            deviation = 'na'
            color = '#000000'

            if distance > 0:
            
                deviation = abs(avg - distance) / std

                if deviation >= 0.0 and deviation < 0.5:
                    color = '#0000ff'   

                if deviation >= 0.5 and deviation < 1.0:
                    color = '#6600ff'   

                if deviation >= 1.0 and deviation < 1.5:
                    color = '#cc00ff'   

                if deviation >= 1.5 and deviation < 2.0:
                    color = '#ff00cc'   

                if deviation >= 2.0 and deviation < 2.5:
                    color = '#ff0066'   

                if deviation >= 2.5:
                    color = '#ff0000'  

            outputLine = outputLine + '<td class="heatmapCell" textA="' + textA + '" textB="' + textB + '" distance="' + str(distance) + '" deviation="' + str(deviation) + '" style="background-color: ' + color + '">&nbsp;&nbsp;</td>'

        outputLine = outputLine + '</tr>' 


    outputLine = '<table>' + outputLine + '</table>'

    outF = codecs.open(outputFileName, 'w', 'utf-8')
    outF.write(outputLine)
    outF.close()
  
# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

def main():

    if len(sys.argv) != 3:
        print 'USAGE ./generateHeatMap.py inputFileName outputFileName'
        print len(sys.argv)
        sys.exit(2)

    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    generateHeatMap(inputFileName, outputFileName)

if __name__ == '__main__':
    main()




