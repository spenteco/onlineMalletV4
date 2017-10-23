#!/usr/bin/env python

import os, sys, time, codecs, commands
import simplejson as json

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
from django.template.loader import render_to_string
from django.utils.encoding import smart_str, smart_unicode

#-----------------------------------------------------------------------
#   
#-----------------------------------------------------------------------

def executeCommand(cmd, printCommand):

    results = commands.getoutput(smart_str(cmd))
    return results

#-----------------------------------------------------------------------
#   
#-----------------------------------------------------------------------
    
def makeUberViz(requestParameters, batchJob, topicNumber):

    #
    #   INPUT AND OUTPUT FOLDERS
    #

    inputFolder = REPO_LOCATION + RESULTS_REPO_LOCATION + batchJob.userId + '_' + str(batchJob.timestamp) + '/' + str(topicNumber) + '/'

    outputFolder = REPO_LOCATION + RESULTS_REPO_LOCATION + batchJob.userId + '_' + str(batchJob.timestamp) + '/' + str(topicNumber) + '/uberViz/'
    executeCommand('mkdir ' + outputFolder, False)

    filePrefix = batchJob.userId + '_' + batchJob.timestamp

    #
    #   LOAD THE BASELINE MATRIX   
    #

    baselineMatrixFileName = ''

    if requestParameters['chunkSize'].strip() > '':
        baselineMatrixFileName = filePrefix + '.averagedMatrixWithMetadata.tsv'
    else:
        baselineMatrixFileName = filePrefix + '.matrixWithMetadata.tsv'

    inF = codecs.open(inputFolder + baselineMatrixFileName, 'r', encoding='utf-8')
    lines = inF.read().split('\n')
    inF.close()

    headerColumns = []
    matrixData = []
    fileIndex = -1

    for lineIndex, line in enumerate(lines):

        columns = line.split('\t')

        #print
        #print 'line', line, 'columns', columns

        if len(columns) > 1:

            if lineIndex == 0:

                headerColumns = columns

                for cIndex, c in enumerate(columns):
                    if c == 'label':
                        headerColumns[cIndex] = 'text'
                        fileIndex = cIndex
                        break
            else:
                matrixData.append(columns)

    finalHeaderColumns = []
    for cIndex, c in enumerate(headerColumns):
        if cIndex < fileIndex:
            finalHeaderColumns.append({'cellType': 'metadata', 'cellValue': c})   
        if cIndex == fileIndex:
            finalHeaderColumns.append({'cellType': 'fileName', 'cellValue': c})   
        if cIndex > fileIndex:
            finalHeaderColumns.append({'cellType': 'topicPct', 'cellValue': c})   

    finalMatrixData = []
    
    #print 'fileIndex', fileIndex

    for row in matrixData:
        finalMatrixRow = []
        for cIndex, c in enumerate(row):
            if cIndex < fileIndex:
                finalMatrixRow.append({'cellType': 'metadata', 'cellValue': c, 'chunkCount': 0})   
            if cIndex == fileIndex:
                finalMatrixRow.append({'cellType': 'fileName', 'cellValue': c, 'chunkCount': 0})   
            if cIndex > fileIndex:
                finalMatrixRow.append({'cellType': 'topicPct', 'cellValue': c, 'chunkCount': 0})   

        finalMatrixData.append(finalMatrixRow)

    #
    #   LOAD THE BASELINE MATRIX   
    #

    if requestParameters['chunkSize'].strip() > '':

        chunkTotalFileName = filePrefix + '.countMatrixWithMetadata.tsv'

        inF = codecs.open(inputFolder + chunkTotalFileName, 'r', encoding='utf-8')
        lines = inF.read().split('\n')
        inF.close()

        headerColumns = []
        matrixData = []
        fileIndex = -1

        for lineIndex, line in enumerate(lines):

            columns = line.split('\t')

            #print
            #print 'line', line, 'columns', columns

            if len(columns) > 1:

                if lineIndex == 0:

                    headerColumns = columns

                    for cIndex, c in enumerate(columns):
                        if c == 'label':
                            headerColumns[cIndex] = 'text'
                            fileIndex = cIndex
                            break
                else:
                    matrixData.append(columns)

        for countRow in matrixData:
            for finalRow in finalMatrixData:
                if countRow[fileIndex] == finalRow[fileIndex]['cellValue']:
                    for cIndex, c in enumerate(countRow):
                        if cIndex > fileIndex:
                            finalRow[cIndex]['chunkCount'] = c  

    #
    #   GET THE TOPIC WORD DATA
    #

    topicWordsFileName = filePrefix + '.topicWords.tsv'

    inF = codecs.open(inputFolder + topicWordsFileName, 'r', encoding='utf-8')
    lines = inF.read().split('\n')
    inF.close()

    topicWordData = []

    for lineIndex, line in enumerate(lines):

        columns = line.split('\t')

        if len(columns) > 1:

            words = []
            for a in range(1, len(columns)):
                if len(columns[a].split(' ')) > 1:
                    words.append(columns[a].split(' '))

            topicWordData.append({'topic': columns[0], 'words': words})

    #
    #   RENDER THE UBER VIZ TABLE
    #

    renderedHtml = render_to_string(APPLICATION_ROOT + 'onlineMalletV4/onlineMalletV4/templates/uberVizTable.html', { 'finalHeaderColumns': finalHeaderColumns, 'finalMatrixData': finalMatrixData, 'topicWordData': topicWordData})

    outF = codecs.open(outputFolder + 'uberVizTable.html', 'w', encoding='utf-8')
    outF.write(renderedHtml)
    outF.close()

#-----------------------------------------------------------------------
#   MAIN
#-----------------------------------------------------------------------

if __name__ == '__main__':

    batchJobId = int(sys.argv[1])
    topicNumber = int(sys.argv[2])

    batchJob = BatchJob.objects.filter(id=batchJobId)[0]

    requestParameters = json.loads(batchJob.jobParameters)

    makeUberViz(requestParameters, batchJob, topicNumber)
