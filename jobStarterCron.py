#!/usr/bin/env python

import os, sys, time, codecs, commands, subprocess
from datetime import date, time, datetime
import site

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
    
#-----------------------------------------------------------------------
#   RUN A SHELL COMMAND
#-----------------------------------------------------------------------

def executeCommand(cmd):

    results = commands.getoutput(cmd).split('\n')  
    
    return results
    
#-----------------------------------------------------------------------
#   GET THE JOB QUEUE FROM THE DATABASE
#-----------------------------------------------------------------------
    
def getJobQueue():

    statusCounts = {}
    runningJobs = []
    queuedJobs = []

    batchJobs = BatchJob.objects.all().order_by('dateTimeRequested')
    for b in batchJobs:
        
        try:
            statusCounts[b.jobStatus] += 1
        except KeyError:
            statusCounts[b.jobStatus] = 1
                
        if b.jobStatus == 'Running':
            runningJobs.append(b)    
                
        if b.jobStatus == 'Queued':
            queuedJobs.append(b)  
            
    #for q in queuedJobs:
    #   print 'q', q.dateTimeRequested, q.id
            
    return statusCounts, runningJobs, queuedJobs
    
#-----------------------------------------------------------------------
#   MAIN
#-----------------------------------------------------------------------
    
#
#   SET UP THE LOG
#    
    
todaysDate = date.isoformat(date.today())

logF = codecs.open(JOB_LOG_LOCATION + 'jobStarterCron_' + todaysDate + '.log', 'a', encoding='utf-8')
logF.write('\n')
logF.write('jobStarterCron starting ' + datetime.now().strftime('%A, %d. %B %Y %I:%M%p') + '\n')
    
#
#   CHECK FOR FAILED JOBS
#    

statusCounts, runningJobs, queuedJobs = getJobQueue()
        
for k, v in statusCounts.iteritems():   
    logF.write(str(v) + ' ' + k + ' jobs\n')
   
results = executeCommand('ps -ef | grep runMalletJob')
relevantLines = []
for line in results:
   if line.find('runMalletJob.py') > -1:
        relevantLines .append(line) 

#print relevantLines

for r in runningJobs:  
    foundPid = False
    for line in relevantLines:
        if line.find(' ' + r.pid + ' ') > -1:
            foundPid = True
            break    
    if foundPid == False:
        r.jobStatus = 'Failed'
        r.save()
        
        logF.write('Marking as failed ' + r.userId + 
                    ' queued at ' +  str(r.dateTimeRequested) + 
                    ' timestamp ' +  str(r.timestamp) + 
                    ' id ' + str(r.id) + '\n')
    
#
#   SUBMIT NEW JOBS, IF WE AREN'T ALREADY RUNNING THE MAX NUMBER
#    

statusCounts, runningJobs, queuedJobs = getJobQueue()  

numberOfQueuedJobs = len(queuedJobs)

if  numberOfQueuedJobs> 0:

    numberOfRunningJobs = len(runningJobs)
    while len(queuedJobs) > 0 and numberOfRunningJobs < BATCH_JOB_LIMIT:
        
        queuedJobs[0].jobStatus = 'Running'
        queuedJobs[0].save()
        
        logF.write('submitting job for ' + queuedJobs[0].userId + 
                    ' queued at ' +  str(queuedJobs[0].dateTimeRequested) + 
                    ' timestamp ' +  str(queuedJobs[0].timestamp) + 
                    ' id ' + str(queuedJobs[0].id) + '\n')
        
        cmd = BATCH_SCRIPTS_LOCATION + 'runMalletJob.py'
        
        logF.write('cmd ' + cmd + '\n')
        
        subprocess.Popen([cmd, str(queuedJobs[0].id)])

        logF.write(cmd + ' ' + str(queuedJobs[0].id) + '\n')

        del queuedJobs[0]
        numberOfRunningJobs += 1
    
#
#   ALL DONE
#    

logF.write('jobStarterCron ending ' + datetime.now().strftime('%A, %d. %B %Y %I:%M%p') + '\n')

logF.close()

