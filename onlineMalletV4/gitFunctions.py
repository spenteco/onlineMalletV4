
import os, subprocess, re
from onlineMalletV4.applicationSettings import *

def addToGit(folder, fileName):
    
    command = 'cd ' + REPO_LOCATION + '; git add "' + folder + fileName + '"'
    
    #print "addToGit command", command
    
    logOutput = ''
    
    try:
        logOutput = subprocess.check_output(command, shell=True)
    except:
        print 'GIT addToGit failed.  Nothing to commit?'
    
    #print
    #print command
    #print logOutput
    #print

def commitGit(commitMessage):
    
    command = 'cd ' + REPO_LOCATION + '; git commit -a -m "' + commitMessage + '"'
    
    #print "commitGit command", command
    
    logOutput = ''
    
    try:
        logOutput = subprocess.check_output(command, shell=True)
    except:
        print 'GIT commitGit failed.  Nothing to commit?'
    
    #print
    #print command
    #print "commitGit command", logOutput
    #print
    
def gitLogForFile(folder, fileName):
    
    command = 'cd ' + REPO_LOCATION + '; git log "' + folder + fileName + '"'
    
    logOutput = ''
    
    try:
        logOutput = subprocess.check_output(command, shell=True)
        
    except:
        print 'GIT gitLogForFile failed.  Nothing to commit?'
        
    logOutput = re.sub(r'Author.+\n', '', logOutput)
    
    #print
    #print command
    #print logOutput
    #print
        
    return logOutput
    
def gitCurrentKeyForFile(folder, fileName):
    
    command = 'cd ' + REPO_LOCATION + '; git log "' + folder + fileName + '"'
    
    logOutput = ''
    
    try:
        logOutput = subprocess.check_output(command, shell=True)
        
    except:
        print 'GIT gitLogForFile failed.  Nothing to commit?'
        
    logOutput = logOutput.split()
    result = logOutput[1]
    
    #print
    #print "GIT FUNCTION", command
    #print "GIT FUNCTION", logOutput
    #print "GIT FUNCTION", result
    #print
        
    return result
    
def gitAddResults():
    
    command = 'cd ' + REPO_LOCATION + '; git status ' + RESULTS_REPO_LOCATION

    #print 'gitAddResults command', command

    logOutput = subprocess.check_output(command, shell=True).split("\n")

    #print 'gitAddResults logOutput', logOutput

    for line in logOutput:
        if line.find(RESULTS_REPO_LOCATION) > -1:
            lineToAdd = line.replace('#', '').strip()

            addToGit('', lineToAdd)
    
def gitAddLogs():
    
    command = 'cd ' + REPO_LOCATION + '; git status ' + LOG_REPO_LOCATION

    #print 'gitAddLogs command', command

    logOutput = subprocess.check_output(command, shell=True).split("\n")

    #print 'gitAddLogs logOutput', logOutput

    for line in logOutput:
        if line.find(LOG_REPO_LOCATION) > -1 and line.find('jobStarterCron_') == -1:
            lineToAdd = line.replace('#', '').strip()

            addToGit('', lineToAdd)

    

