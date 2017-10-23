#!/usr/bin/env python

import os, sys, time, codecs, commands, re
from datetime import date, time, datetime
import time
import simplejson as json
import smtplib
from email.MIMEText import MIMEText

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
from onlineMalletV4.gitFunctions import *
from django.utils.encoding import smart_str, smart_unicode

import logging

#-----------------------------------------------------------------------
#   
#-----------------------------------------------------------------------
    
def sendEmailNotification(recipients, messageText):

    #   ----------------------------------------------------------------
    
    RECIPIENTS = recipients
    SENDER = 'spenteco@artsci.wustl.edu'
    
    msg = MIMEText(messageText, "plain", "utf-8")
    msg['Subject'] = 'Mallet Batch Job Complete'
    msg['From'] = 'spentecost@email.wustl.edu'
    msg['To'] = 'spenteco@wustl.edu'

    s = smtplib.SMTP('localhost')
    s.sendmail('spentecost@email.wustl.edu', RECIPIENTS, msg.as_string())
    s.quit()

#-----------------------------------------------------------------------
#   
#-----------------------------------------------------------------------

def logMessage(label, msg):

    logging.info(' ')
    logging.info(label + ' ' + msg)

def executeCommand(cmd, printCommand):

    if printCommand == True:
        logMessage('cmd', cmd)

    results = commands.getoutput(smart_str(cmd))

    return results

#-----------------------------------------------------------------------
#   
#-----------------------------------------------------------------------

def cleanFileName(fileName):

    fileNameParts = fileName.split('/')

    #cleanFileName = re.sub('[^a-zA-Z0-9_\.]', '_', fileNameParts[-1])
    #cleanFileName = fileNameParts[-1]
    cleanFileName = re.sub(' ', '_', fileNameParts[-1])

    return cleanFileName

#-----------------------------------------------------------------------
#   
#----------------------------------------------------------------------- 
    
def processJob(requestParameters, batchJob):

    #
    #   CREATE INPUT FOLDERS FOR THE RUN. 
    #

    tempFolder = TEMP_LOCATION + batchJob.userId + '_' + batchJob.timestamp + '/'
    inputFolder = [tempFolder + 'input/']
    stopwordsFolder = tempFolder + 'stopwords/'

    executeCommand('rm -r ' + tempFolder, True)

    executeCommand('mkdir ' + tempFolder, True)
    executeCommand('mkdir ' + inputFolder[0], True)
    executeCommand('mkdir ' + stopwordsFolder, True)

    #
    #   COPY INPUT FILES; SAVE FILE NAMES AND GIT VERSIONS
    #

    inputFilesDetails = []

    for c in requestParameters['corporaFiles']:

        cleanC = cleanFileName(c)

        logMessage('corporaFiles', (c + ' -> ' + cleanC))

        if cleanC.endswith('.txt'):

            executeCommand('cp "' + REPO_LOCATION + CORPUS_REPO_FOLDER + c + '" "' + inputFolder[0] + cleanC + '"', True)
            inputFilesDetails.append([c, ''])

        if cleanC.endswith('.zip'):

            executeCommand('unzip -xj "' + REPO_LOCATION + CORPUS_REPO_FOLDER + c + '" -d ' + inputFolder[0], True)

            lsResults = executeCommand('ls -1 ' + inputFolder[0], False).split('\n')
            for l in lsResults:
                if [l, ''] not in inputFilesDetails:
                    inputFilesDetails.append([l, ''])

        if cleanC.endswith('.tar.gz'):

            executeCommand('tar -xzvf "' + REPO_LOCATION + CORPUS_REPO_FOLDER + c + '" -C ' + inputFolder[0] + ' --strip-components=1', True)

            lsResults = executeCommand('ls -1 ' + inputFolder[0], False).split('\n')
            for l in lsResults:
                if [l, ''] not in inputFilesDetails:
                    inputFilesDetails.append([l, ''])

    for c in requestParameters['individualFiles']:

        cleanC = cleanFileName(c)

        logMessage('individualFiles', (c + ' -> ' + cleanC))

        if cleanC.endswith('.txt'):

            executeCommand('cp "' + REPO_LOCATION + CORPUS_REPO_FOLDER + c + '" "' + inputFolder[0] + cleanC + '"', True)
            inputFilesDetails.append([c, ''])

        if cleanC.endswith('.zip'):

            executeCommand('unzip -xj "' + REPO_LOCATION + CORPUS_REPO_FOLDER + c + '" -d ' + inputFolder[0], True)

            lsResults = executeCommand('ls -1 ' + inputFolder[0], False).split('\n')
            for l in lsResults:
                if [l, ''] not in inputFilesDetails:
                    inputFilesDetails.append([l, ''])

        if cleanC.endswith('.tar.gz'):

            executeCommand('tar -xzvf "' + REPO_LOCATION + CORPUS_REPO_FOLDER + c + '" -C ' + inputFolder[0] + ' --strip-components=1', True)

            lsResults = executeCommand('ls -1 ' + inputFolder[0], False).split('\n')
            for l in lsResults:
                if [l, ''] not in inputFilesDetails:
                    inputFilesDetails.append([l, ''])

    #
    #   DO THE SAME FOR STOPWORDS, THEN COMBINE THEM
    #

    stopwordsFileDetails = []

    for c in requestParameters['stopwords']:

        cleanC = cleanFileName(c)

        executeCommand('cp "' + REPO_LOCATION + STOPWORDS_REPO_FOLDER + c + '" ' + stopwordsFolder + cleanC, True)

        #stopwordsFileDetails.append([c, gitCurrentKeyForFile(REPO_LOCATION + STOPWORDS_REPO_FOLDER, c)]) 
        stopwordsFileDetails.append([c, '']) 
    
    #logging.info(' ')
    #for i in stopwordsFileDetails:
    #    logging.info('stopwords file git version' + ' ' + i[0] + ' ' + i[1] )

    executeCommand('cat ' + stopwordsFolder + '* > ' + stopwordsFolder + 'stopwords.txt', True)

    for i in stopwordsFileDetails:

        cleanI = cleanFileName(i[0])

        executeCommand('rm ' + stopwordsFolder + cleanI, True) 

    #
    #   IF CHUNKING IS REQUIRED, THEN DO IT
    #

    if requestParameters['chunkSize'].strip() > '':

        logging.info(' ')
        logging.info("chunking" + ' ' + str(requestParameters['chunkSize']))

        inputFolder.append(tempFolder + 'chunked/')
        executeCommand('mkdir ' + inputFolder[-1], True)

        executeCommand(BATCH_SCRIPTS_LOCATION + 'chunkTexts.py ' + inputFolder[-2] + ' ' + requestParameters['chunkSize'].strip() + ' ' + inputFolder[-1], True) 

    #
    #   IF DF PRE-PROCESSING IS REQUIRED, THEN DO IT
    #

    if requestParameters['lowDFPercentage'].strip() > '' or requestParameters['highDFPercentage'].strip() > '':

        if requestParameters['lowDFPercentage'].strip() == '':
            requestParameters['lowDFPercentage'] = '-1'

        if requestParameters['highDFPercentage'].strip() == '':
            requestParameters['highDFPercentage'] = '999'

        logging.info(' ')
        logging.info("df processing" + ' ' + str(requestParameters['lowDFPercentage']) + ' ' + str(requestParameters['highDFPercentage']))

        inputFolder.append(tempFolder + 'dfTrim/')
        executeCommand('mkdir ' + inputFolder[-1], True)

        executeCommand(BATCH_SCRIPTS_LOCATION + 'dfTrim.py ' + inputFolder[-2] + ' ' + requestParameters['lowDFPercentage'].strip() + ' ' + requestParameters['highDFPercentage'].strip() + ' ' + inputFolder[-1], True) 

    #
    #   FINALLY, WE CAN RUN TOPIC MODELING . . . 
    #

    malletOutputsFolder = REPO_LOCATION + RESULTS_REPO_LOCATION + batchJob.userId + '_' + batchJob.timestamp + '/'
    executeCommand('mkdir ' + malletOutputsFolder, True)

    stopwordParameter = ''
    if len(requestParameters['stopwords']) > 0:
        stopwordParameter = '--remove-stopwords --extra-stopwords ' + stopwordsFolder + 'stopwords.txt'

    #
    #   IMPORT INTO MALLET
    #

    logging.info(' ')
    logging.info('Importing texts into Mallet')

    cmd = MALLET_BIN_FOLDER + 'mallet import-dir --token-regex \'[\p{L}\p{M}]+\' --input ' + inputFolder[-1] + ' --output ' + tempFolder + batchJob.userId + '_' + batchJob.timestamp + '.mallet  --keep-sequence ' + stopwordParameter

    logging.info(' ')
    logging.info(executeCommand(cmd, True))

    for t in requestParameters['numberOfTopics'].split(',') :

        topicNumber = t.strip()
        if topicNumber > '':

            topicOutputsFolder = malletOutputsFolder + topicNumber + '/'    
            executeCommand('mkdir ' + topicOutputsFolder, True)

            optimizeIntervalParameter = ''
            if requestParameters['optimizeInterval'].strip() > '':
                optimizeIntervalParameter = '--optimize-interval ' + requestParameters['optimizeInterval']

            optimizeBurnInParameter = ''
            if requestParameters['optimizeBurnIn'].strip() > '':
                optimizeBurnInParameter = '--optimize-burn-in ' + requestParameters['optimizeBurnIn']
                
            alphaParameter = ''
            if requestParameters['alpha'].strip() > '':
                alphaParameter = '--alpha ' + requestParameters['alpha']

            iterationsParameter = ''
            if requestParameters['iterations'].strip() > '':
                alphaParameter = '--num-iterations ' + requestParameters['iterations']

            #
            #   TOPIC MODELING
            #

            logging.info(' ')
            logging.info('Running topic modeling for ' + str(topicNumber) + ' topics')

            cmd = MALLET_BIN_FOLDER + 'mallet train-topics --random-seed 1 --input ' + tempFolder + batchJob.userId + '_' + batchJob.timestamp + '.mallet --num-topics ' + str(topicNumber) + ' ' + iterationsParameter + ' ' + alphaParameter + ' ' + optimizeIntervalParameter + ' ' + optimizeBurnInParameter + ' --output-state ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.state.gz  --output-doc-topics ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.topicPcts.tsv --output-topic-keys ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.rawTopicWords.txt --output-model ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.model'

            logging.info(' ')
            logging.info(executeCommand(cmd, True))

            #
            #   COMMON OUTPUTS
            #

            logging.info(' ')
            logging.info('Generating common outputs for ' + str(topicNumber) + ' topics')

            cmd = 'gunzip ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.state.gz'

            logging.info(' ')
            logging.info(executeCommand(cmd, True))

            numberOfTopicWords = '100'
            if requestParameters['numberOfTopicWords'].strip() > '':
                numberOfTopicWords = requestParameters['numberOfTopicWords'].strip()

            cmd = 'export LANG=en_US.UTF-8; echo $LANG; java -classpath ' + BATCH_SCRIPTS_LOCATION + 'JavaUtilitiesForMallet.jar edu.wustl.artsci.hdw.ListWordsInTopics ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.state  ' + numberOfTopicWords + ' 1> ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp +  '.topicWords.tsv'

            logging.info(' ')
            logging.info(executeCommand(cmd, True))

            cmd = BATCH_SCRIPTS_LOCATION + 'getMatrixFromDocFile.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.topicPcts.tsv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.matrix.tsv'

            logging.info(' ')
            logging.info(executeCommand(cmd, True))

            if requestParameters['chunkSize'].strip() == '':

                cmd = BATCH_SCRIPTS_LOCATION + 'distanceMatrix.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.matrix.tsv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.distances.tsv'

                logging.info(' ')
                logging.info(executeCommand(cmd, True))

            cmd = BATCH_SCRIPTS_LOCATION + 'combineMatrixAndMetadata.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.matrix.tsv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.matrixWithMetadata.tsv ' + '"' + requestParameters['chunkSize'].strip() + '"'

            logging.info(' ')
            logging.info(executeCommand(cmd, True))

            if requestParameters['chunkSize'].strip() > '':

                cmd = BATCH_SCRIPTS_LOCATION + 'averageChunkMatrix.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.matrixWithMetadata.tsv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.averagedMatrixWithMetadata.tsv'

                logging.info(' ')
                logging.info(executeCommand(cmd, True))

                chunkCountingThreshhold = '10'
                if requestParameters['chunkCountingThreshhold'].strip() > '':
                    chunkCountingThreshhold = requestParameters['chunkCountingThreshhold'].strip()

                cmd = BATCH_SCRIPTS_LOCATION + 'countChunkMatrix.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.matrixWithMetadata.tsv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.countMatrixWithMetadata.tsv ' + chunkCountingThreshhold

                logging.info(' ')
                logging.info(executeCommand(cmd, True))

                cmd = BATCH_SCRIPTS_LOCATION + 'distanceMatrix.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.averagedMatrixWithMetadata.tsv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.distances.tsv'

                logging.info(' ')
                logging.info(executeCommand(cmd, True))

            #
            #   UBER VIZ AND HEATMAP
            #

            cmd = BATCH_SCRIPTS_LOCATION + 'makeUberViz.py ' + str(batchJob.id) + ' ' + str(topicNumber)

            logging.info(' ')
            logging.info(executeCommand(cmd, True))

            #   NOT CONVERTED TO TAB-SEPARATED OUTPUT

            #cmd = BATCH_SCRIPTS_LOCATION + 'generateHeatMap.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.distances.csv  '+ topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.heatmap.html'

            #logging.info(' ')
            #logging.info(executeCommand(cmd, True))

            #
            #   HILITE TEXTS
            #

            #inputFolder[0]
            #topicOutputsFolder

            hiliteHtmlFolder = topicOutputsFolder + 'hilite/'   
            executeCommand('mkdir ' + hiliteHtmlFolder, True)

            cmd = BATCH_SCRIPTS_LOCATION + 'hiliteTopicWordsInDocs.py ' + topicOutputsFolder + batchJob.userId + '_' + batchJob.timestamp + '.state  ' + inputFolder[0] +  ' ' + hiliteHtmlFolder + ' ' + str(batchJob.id) + ' ' + str(topicNumber)
            logging.info(' ')
            logging.info(executeCommand(cmd, True))

    #
    #   COMMIT THE RESULTS
    #
    
    #gitAddResults()
    #gitAddLogs()
    #commitGit('Commiting test results from ' + batchJob.userId + ' ' + batchJob.timestamp + ' job id ' + str(batchJob.id))

#-----------------------------------------------------------------------
#   
#----------------------------------------------------------------------- 

def printRequestParameters(requestParameters):

    logging.info(' ')
    for c in requestParameters['corpora']:
        logging.info('input corpus' + ' ' + c)

    logging.info(' ')
    for c in requestParameters['corporaFiles']:
        logging.info('input corporaFile' + ' ' + c)

    logging.info(' ')
    for c in requestParameters['individualFiles']:
        logging.info('input individualFile' + ' ' + c)

    logging.info(' ')
    for c in requestParameters['stopwords']:
        logging.info('stopwords' + ' ' + c)

    logging.info(' ')
    logging.info('chunkSize' + ' ' + str(requestParameters['chunkSize']))
    logging.info('lowDFPercentage' + ' ' + str(requestParameters['lowDFPercentage']))
    logging.info('highDFPercentage' + ' ' + str(requestParameters['highDFPercentage']))

    logging.info(' ')
    logging.info('numberOfTopics' + ' ' + str(requestParameters['numberOfTopics']))
    logging.info('alpha' + ' ' + str(requestParameters['alpha']))
    logging.info('optimizeInterval' + ' ' + str(requestParameters['optimizeInterval']))
    logging.info('optimizeBurnIn' + ' ' + str(requestParameters['optimizeBurnIn']))

#-----------------------------------------------------------------------
#   MAIN
#-----------------------------------------------------------------------

if __name__ == '__main__':

    batchJobId = int(sys.argv[1])

    batchJob = BatchJob.objects.filter(id=batchJobId)[0]
    #batchJob.pid = os.getpid()
    #batchJob.logfileName = JOB_LOG_LOCATION + batchJob.userId + '_' + batchJob.timestamp + '.log'
    #batchJob.save()

    #logging.basicConfig(filename=JOB_LOG_LOCATION + batchJob.userId + '_' + batchJob.timestamp + '.log', level=logging.INFO)

    #logging.info(' ')
    #logging.info('runMalletJob starting' + ' ' + datetime.now().strftime('%A, %d. %B %Y %I:%M%p'))
    #logging.info(' ')
    #logging.info('pid' + ' ' + str(os.getpid()))
    #logging.info('userId' + ' ' + batchJob.userId)
    #logging.info('dateTimeRequested' + ' ' + str(batchJob.dateTimeRequested))
    #logging.info('logfileName' + ' ' + batchJob.logfileName)
    #logging.info('jobParameters' + ' ' + batchJob.jobParameters)

    #requestParameters = json.loads(batchJob.jobParameters)

    #printRequestParameters(requestParameters)

    #processJob(requestParameters, batchJob)

    receivers = ['spentecost@email.wustl.edu', batchJob.userEmail]
    
    message ='From:  spenteco@wustl.edu\n' + 'To: ' + batchJob.userEmail + '\n' + 'Subject: Mallet batch job completion' + '\n' + 'The mallet job you requested at ' + str(batchJob.dateTimeRequested) + 'has completed.'

    sendEmailNotification(receivers, message)
        
    #logging.info(' ')
    #logging.info('Send completion email')

    #logging.info(' ')
    #logging.info('runMalletJob ending' + ' ' + datetime.now().strftime('%A, %d. %B %Y %I:%M%p'))
    #logging.info(' ')

    batchJob.jobStatus = 'Completed'
    batchJob.save()
