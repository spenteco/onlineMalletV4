from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse

from django.db import models
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.encoding import force_unicode
from django.contrib.auth import authenticate

from django.template import RequestContext

import simplejson as json

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
from onlineMalletV4.gitFunctions import *

import os, time, codecs
from datetime import datetime

from corporaViews import getFileTree
from stopwordViews import getStopwordFiles
    
# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------
    
@login_required()
def runLda(request):
    
    fileTree, corpusOwners = getFileTree()
    stopwordFiles, stopwordOwners = getStopwordFiles()
    
    scrubbedFileTree = []
    for f in fileTree:
        if len(f['textFiles']) > 0:
            scrubbedFileTree.append(f)
    
    return render_to_response('runLda.html', {'stopwordFiles': stopwordFiles, "fileTree": scrubbedFileTree, "corpusOwners": corpusOwners, "stopwordOwners": stopwordOwners, "corpusFileLocation": REPO_LOCATION + CORPUS_REPO_FOLDER, "stopwordFileLocation": REPO_LOCATION + STOPWORDS_REPO_FOLDER}, context_instance=RequestContext(request))
    
@login_required()
def submitLdaJob(request):
    
    postData = request.POST['data']
    
    jobParameters = json.loads(postData)
    
    batchJob = BatchJob(userId=request.user,
                        timestamp=str(int(time.time() * 100.0)),  
                        userEmail=request.user.email,  
                        userFirstName=request.user.first_name,  
                        jobStatus='Queued',  
                        pid='',  
                        logfileName='',  
                        jobParameters=postData,
                        jobType='LDA')

    batchJob.save()
    
    return render_to_response('submitLdaJob.html', {'message': 'job submitted'})
    
@login_required()
def listJobs(request):
    
    #batchJobs = BatchJob.objects.filter(userId=request.user).order_by('dateTimeRequested').reverse()
    batchJobs = BatchJob.objects.order_by('userId', 'dateTimeRequested').reverse()

    batchJobInformation = {}

    for b in batchJobs:

        try:
            noop = batchJobInformation[b.userId]
        except KeyError:    
            batchJobInformation[b.userId] = []

        p = json.loads(b.jobParameters)

        corpora = '';
        if len(p['corpora']) > 0:
            corpora = ', '.join(p['corpora'])
        else:
            corpora = ', '.join(p['individualFiles'])[0:25] + ' . . . '

        jobNotes = ''
        if b.jobNotes.strip() > '':
            jobNotes = b.jobNotes[0:25] + ' . . . '

        batchJobInformation[b.userId].append({'id': b.id, 
                                                'dateTimeRequested': b.dateTimeRequested, 
                                                'jobStatus': b.jobStatus, 
                                                'logfileName': b.logfileName, 
                                                'jobParameters': b.jobParameters,
                                                'numberOfTopics': p['numberOfTopics'],
                                                'chunkSize': p['chunkSize'],
                                                'corpora': corpora,
                                                'jobType': b.jobType,
                                                'jobNotes': jobNotes})

    requestUser = unicode(request.user)

    return render_to_response('listJobs.html', {'requestUser': requestUser, 'batchJobInformation' : batchJobInformation})
    
@login_required()
def showJobDetails(request):

    id = request.GET['id']

    job = BatchJob.objects.filter(id=id)[0]

    p = json.loads(job.jobParameters)

    topics = p['numberOfTopics'].split(',')
    topicOutputs = []
    for t in topics:

        filePrefix = REPO_LOCATION + RESULTS_REPO_LOCATION + job.userId + '_' + job.timestamp + '/' + t + '/' + job.userId + '_' + job.timestamp
        
        topicOutputFiles = {'numberOfTopics': t,
                            "matrix":  filePrefix + '.matrix.tsv',
                            "topicPcts":  filePrefix + '.topicPcts.tsv',
                            "topicWords":  filePrefix + '.topicWords.tsv',
                            "rawTopicWords":  filePrefix + '.rawTopicWords.txt',
                            "matrixWithMetadata":  filePrefix + '.matrixWithMetadata.tsv',
                            "distanceMatrix":  filePrefix + '.distances.tsv',
                            "heatMap":  filePrefix + '.heatmap.html',
                            "model":  filePrefix + '.model',
                            "uberviz":  REPO_LOCATION + RESULTS_REPO_LOCATION + job.userId + '_' + job.timestamp + '/' + t + '/uberViz/uberVizTable.html'}

        if p['chunkSize'].strip() > '':
            topicOutputFiles['averagedMatrixWithMetadata']  =  filePrefix + '.averagedMatrixWithMetadata.tsv'
            topicOutputFiles['countMatrixWithMetadata']  =  filePrefix + '.countMatrixWithMetadata.tsv'

        topicOutputs.append(topicOutputFiles)  

    iterations = ''
    try:
        iterations = p['iterations']
    except KeyError:
        pass

    jobDetails = {'id': job.id, 
                            'userId': job.userId, 
                            'timestamp': job.timestamp, 
                            'dateTimeRequested': job.dateTimeRequested, 
                            'jobStatus': job.jobStatus, 
                            'logfileName': job.logfileName, 
                            'jobParameters': job.jobParameters,
                            'numberOfTopics': p['numberOfTopics'],
                            'numberOfTopicWords': p['numberOfTopicWords'],
                            'chunkCountingThreshhold': p['chunkCountingThreshhold'],
                            'corpora': ', '.join(p['corpora']),
                            'corporaFiles': ', '.join(p['corporaFiles']),
                            'individualFiles': ', '.join(p['individualFiles']),
                            'stopwords': ', '.join(p['stopwords']),
                            'chunkSize': p['chunkSize'],
                            'lowDFPercentage': p['lowDFPercentage'],
                            'highDFPercentage': p['highDFPercentage'],
                            'iterations': iterations,
                            'alpha': p['alpha'],
                            'optimizeInterval': p['optimizeInterval'],
                            'optimizeBurnIn': p['optimizeBurnIn'],
                            'topicOutputs': topicOutputs,
                            'jobType': job.jobType,
                            'jobNotes': job.jobNotes}

    return render_to_response('showJobDetails.html', {'job' : jobDetails})
    
@login_required()
def getResultsFile(request):

    fileName = request.GET['fileName']
    download = file(fileName.encode('utf-8'), 'r')

    if fileName.endswith(".tsv"):
        response = HttpResponse(download.read(), content_type='text/tsv; charset=utf-8')
    else:
        response = HttpResponse(download.read(), content_type='text/plain; charset=utf-8')
    
    response['Content-Disposition'] = 'attachment; filename="' + fileName.encode('utf-8').split('/')[-1] + '"'

    return response

@login_required()
def startUberViz(request):

    fileName = request.GET['fileName']
    jobId = request.GET['id']
    topics = int(request.GET['topics'])

    topicNumbers = []
    for a in range(0, topics):
        topicNumbers.append(a)

    job = BatchJob.objects.filter(id=int(jobId))[0]

    fileLocation = REPO_LOCATION + RESULTS_REPO_LOCATION + job.userId + '_' + str(job.timestamp)+ '/' + str(topics) + '/hilite/'

    p = json.loads(job.jobParameters)
    runChunked = False
    if p['chunkSize'].strip() > '':
        runChunked = True

    return render_to_response('startUberViz.html', {'fileName' : fileName, 'runChunked': runChunked, 'topicNumbers': topicNumbers, 'timestamp': job.timestamp, 'userid': job.userId, 'numberOfTopics': topics, 'fileLocation': fileLocation})

@login_required()
def showHeatMap(request):

    fileName = request.GET['fileName']

    return render_to_response('showHeatMap.html', {'fileName' : fileName})

@login_required()
def updateJobNotes(request):

    jobId = request.GET['jobId']
    jobNotes = request.GET['jobNotes']

    job = BatchJob.objects.filter(id=int(jobId))[0]
    job.jobNotes = jobNotes
    job.save()

    return render_to_response('ok.html')
