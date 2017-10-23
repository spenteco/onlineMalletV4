#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, codecs, commands, re
import simplejson as json

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
from django.template.loader import render_to_string
from django.utils.encoding import smart_str, smart_unicode

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

def executeCommand(cmd):

    results = commands.getoutput("export PYTHONIOENCODING=UTF-8; " + smart_str(cmd))

    return results

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

def findAndTagTopicWords(inputDocFolder, outputDocFolder, inputFile, topicWords):

   #print 'inputFile', [inputFile]

    p = re.compile(u'(\s|,|\.|;|:|-|\'|\?|!|\(|\)|\'|»|«)')

    fileEncoding = executeCommand('file -ib "' + inputDocFolder + inputFile + '"')
    if fileEncoding.find(';') > -1:
        fileEncoding = fileEncoding.split(';')[1].strip().replace('charset=', '')
    if fileEncoding in ['binary', 'unknown-8bit', 'application/octet-stream']:
        fileEncoding = 'us-ascii' 

    inF = codecs.open(inputDocFolder + inputFile, 'r', encoding=fileEncoding, errors='replace')

    taggedTokens = []

    for l in inF:

        tokens = p.split(l.replace('\r', ''))

        for token in tokens:
                
            classString = ''
            
            if len(token) > 1:
                
                topics = []
                try:
                    topics = topicWords[inputFile + ' ' + token.lower()]
                except KeyError:
                    noop = 0
                        
                if len(topics) > 0:
                    
                    for t in topics:
                        if classString > '':
                            classString = classString + ' '
                        classString = classString + 'topic_' + t

            if token == '\n':
                taggedTokens.append('<br/>')
            else:
                taggedTokens.append('<span class="hilitedToken ' + classString + '">' + token + '</span>')   

    inF.close()

    hilitedText = ''.join(taggedTokens)

    renderedHtml = '<div class="hilitedText">' + '<h3>' + inputFile + '</h3>' + hilitedText + '</div>'

    outputFileName = inputFile.replace('.txt', '') + '.html'

   #print 'writing', (outputDocFolder + outputFileName)

    outF = codecs.open(outputDocFolder + outputFileName, 'w', encoding='utf-8')
    outF.write(renderedHtml)
    outF.close()

def pullWordsForTopic(inputStateFile, filesAreChunked):

   #print 'LOADING STATE'

    inF = codecs.open(inputStateFile, 'r', encoding='utf-8')

    tempWordTopic = {}

    for l in inF:
        if l[0:1] != '#':

            fixedL = l.strip()

            if len(fixedL.split(' ')) == 6:

                textName = fixedL.strip().split(' ')[1].split('/')[-1]

                if filesAreChunked == True:

                    unchunkedName = ''

                    fileNameParts = textName.split('_')

                    for a in range(0, len(fileNameParts) - 1):
                        if unchunkedName > '':
                            unchunkedName = unchunkedName + '_'
                        unchunkedName = unchunkedName + fileNameParts[a] 

                    textName = unchunkedName

                word = fixedL.strip().split(' ')[4]
                wordTopic = fixedL.strip().split(' ')[5]
                
                tempWordTopic[textName + ' ' + word + ' ' + wordTopic] = 1
                
    inF.close()

   #print 'STATE FILE CLOSED'

    wordTopics = {}

    for k in tempWordTopic.keys():
        
        kFile = k.split(' ')[0]
        kWord = k.split(' ')[1]
        kTopic = k.split(' ')[2]
        
        try:
            wordTopics[kFile + ' ' + kWord].append(kTopic)
        except:
            wordTopics[kFile + ' ' + kWord] = []
            wordTopics[kFile + ' ' + kWord].append(kTopic)

   #print 'FINISHED LOADING STATE'
            
    return wordTopics

# -------------------------------------------------------------------------------------- #
#  ./hiliteTopicWordsInDocs.py  /home/spenteco/projects/onlineMalletV3/onlineMalletDataRepo/results/smp_138254371748/25/smp_138254371748.state /home/spenteco/projects/onlineMalletV3/onlineMalletTemp/smp_138254371748/input/ /home/spenteco/projects/onlineMalletV3/onlineMalletDataRepo/results/smp_138254371748/25/hilite/ 4 25 
# -------------------------------------------------------------------------------------- #

if len(sys.argv) != 6:
   #print 'USAGE: hiliteTopicWordsInDocs.py inputStateFile inputDocFolder outputDocFolder jobId numberOfTopics'
   #print len(sys.argv)
    sys.exit(2)

inputStateFile = sys.argv[1]
inputDocFolder = sys.argv[2]
outputDocFolder = sys.argv[3]
batchJobId = int(sys.argv[4])
batchJobId = int(sys.argv[4])

batchJob = BatchJob.objects.filter(id=batchJobId)[0]

requestParameters = json.loads(batchJob.jobParameters)
filesAreChunked = False
if requestParameters['chunkSize'].strip() > '':
    filesAreChunked = True

print 'inputStateFile', inputStateFile
print 'inputDocFolder', inputDocFolder
print 'outputDocFolder', outputDocFolder
print 'filesAreChunked', filesAreChunked

# ----------------------------------------------------------------------

topicWords = pullWordsForTopic(inputStateFile, filesAreChunked)

# ----------------------------------------------------------------------

for textFileName in os.listdir(unicode(inputDocFolder)):

   #print 'hilighting', textFileName

    findAndTagTopicWords(inputDocFolder, outputDocFolder, textFileName, topicWords)

# ----------------------------------------------------------------------
    



