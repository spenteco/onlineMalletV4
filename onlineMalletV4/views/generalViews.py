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

import simplejson as json

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
from onlineMalletV4.gitFunctions import *

import os, commands, codecs
from datetime import date, time, datetime
from django.utils.encoding import smart_str, smart_unicode

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

def executeCommand(cmd):

    #print 'cmd', cmd

    results = commands.getoutput("export PYTHONIOENCODING=UTF-8; " + smart_str(cmd))

    return results

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

@login_required()
def index(request):
    
    batchJobs = BatchJob.objects.filter(userId=request.user).order_by('dateTimeRequested').reverse()

    batchJobInformation = []

    n = 0
    for b in batchJobs:

        p = json.loads(b.jobParameters)

        corpora = '';
        if len(p['corpora']) > 0:
            corpora = ', '.join(p['corpora'])
        else:
            corpora = ', '.join(p['individualFiles'])[0:25] + ' . . . '

        jobNotes = ''
        if b.jobNotes.strip() > '':
            jobNotes = b.jobNotes[0:25] + ' . . . '

        batchJobInformation.append({'id': b.id, 
                                                    'dateTimeRequested': b.dateTimeRequested, 
                                                    'jobStatus': b.jobStatus, 
                                                    'logfileName': b.logfileName, 
                                                    'jobParameters': b.jobParameters,
                                                    'numberOfTopics': p['numberOfTopics'],
                                                    'chunkSize': p['chunkSize'],
                                                    'corpora': corpora,
                                                    'jobType': b.jobType,
                                                    'jobNotes': jobNotes})
        n += 1
        if n == 5:
            break

    todaysDate = date.isoformat(date.today())
    cronLogFileName = JOB_LOG_LOCATION + 'jobStarterCron_' + todaysDate + '.log'

    return render_to_response('index.html', {'is_superuser': request.user.is_superuser, 'batchJobInformation': batchJobInformation, 'cronLogFileName': cronLogFileName})

@login_required()
def logOut(request):
    
    logout(request)
    
    return redirect('/onlineMalletV4/')

# ----------------------------------------------------------------------
#   GENERALIZE FILE VIEWER
# ----------------------------------------------------------------------

def viewFile(request):
    
    filePathAndName = request.GET['file']

    fileEncoding = executeCommand('file -ib "' + filePathAndName + '"')
    if fileEncoding.find(';') > -1:
        fileEncoding = fileEncoding.split(';')[1].strip().replace('charset=', '')
    if fileEncoding in ['binary', 'unknown-8bit', 'application/octet-stream']:
        fileEncoding = 'us-ascii' 
    
    fileContents = codecs.open(filePathAndName.encode('utf-8'), 'r', encoding=fileEncoding, errors='replace').read()
    
    return render_to_response('viewFile.html', {'filePathAndName': filePathAndName, 'fileContents': fileContents})
    
