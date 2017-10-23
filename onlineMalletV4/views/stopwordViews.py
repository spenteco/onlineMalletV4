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

import os, sys
from datetime import datetime
    
# ----------------------------------------------------------------------
#   HELPER FUNCTIONS
# ----------------------------------------------------------------------

def monkeyPatchFileName(fileName):

    newFileName = ''

    for a in range(0, len(fileName)):
        if a < len(fileName) - 1 and fileName[a] == '\\' and fileName[a + 1] == '\\':
            pass
        else:
            newFileName += fileName[a]

    return newFileName

def getFromFileSystem(folderName, stopwordFiles):

    #print '\n\n\n'
    #print 'getdefaultencoding()', sys.getdefaultencoding()
    #print 'filesystemencoding', sys.getfilesystemencoding()
    #print '\n\n\n'

    newStopwordFiles = stopwordFiles
    
    for swFs in os.listdir(unicode(folderName)):

        a = folderName 
        b = monkeyPatchFileName(swFs)
        c = b.decode('utf-8')

        if os.path.isdir((a + c).encode('utf-8')) == True:
            getFromFileSystem((a + c) + '/', newStopwordFiles)
        else:
            subFolder = folderName.replace(REPO_LOCATION + STOPWORDS_REPO_FOLDER, '')
            
            newStopwordFiles.append({'fileName': c, 'subFolder': subFolder, 'inDatabase': False, 'onFileSystem': True, 'inGit': False, 'owner': '', 'descriptiveName': '', 'notes': '', 'dateLastModified': '', 'gitLog': ''})
    
    return newStopwordFiles
    
def getStopwordFiles():   
    
    stopwordFiles = getFromFileSystem(REPO_LOCATION + STOPWORDS_REPO_FOLDER, [])
    owners = []
    
    for swDb in StopwordFile.objects.all():
    
        swFound = False
        for sf in stopwordFiles:

            try:                
                type(sf['fileName'])
                if sf['fileName'] == swDb.stopwordFileName and sf['subFolder'][:-1] == swDb.stopwordFileOwner:
                
                    swFound = True
                    sf['inDatabase'] = True
                    sf['owner'] = swDb.stopwordFileOwner
                    sf['descriptiveName'] = swDb.stopwordDescriptiveName
                    sf['notes'] = swDb.stopwordFileNotes
                    sf['dateLastModified'] = swDb.dateLastModified
            except KeyError:
                print 'MISSING', sf                
        
        if swFound == False:
            stopwordFiles.append({'fileName': swDb.stopwordFileName, 'inDatabase': True, 'onFileSystem': False, 'inGit': False, 'owner': swDb.stopwordFileOwner, 'descriptiveName': swDb.stopwordDescriptiveName, 'notes': swDb.stopwordFileNotes, 'dateLastModified': swDb.dateLastModified, 'gitLog': ''})
                
        owners.append(swDb.stopwordFileOwner)
        
    temp = []
    for s in stopwordFiles:
        temp.append([s['fileName'], s])
        
    stopwordFiles = []
    for t in sorted(temp):
        stopwordFiles.append(t[1])
        
    return stopwordFiles, sorted(list(set(owners)))        
    
# ----------------------------------------------------------------------
#   STOP WORDS   
# ----------------------------------------------------------------------

@login_required()
def viewStopwords(request):
    
    stopwordFiles, owners = getStopwordFiles()
            
    #for sw in stopwordFiles:
    #    gitLogDetails = gitLogForFile(STOPWORDS_REPO_FOLDER, sw['fileName'])
    #    if len(gitLogDetails) > 0:
    #        sw['inGit'] = True
    #        sw['gitLog'] = gitLogDetails
    
    return render_to_response('viewStopwords.html', {'stopwordFiles': stopwordFiles, 'fileLocation': REPO_LOCATION + STOPWORDS_REPO_FOLDER, 'owners': owners})

@login_required()
def uploadStopwords(request):
    
    if request.method == 'POST':
        
        descriptiveName = request.POST['descriptiveName']
        notes = request.POST['notes']
        fileExists = request.POST['fileExists']
        
        fileName = request.FILES['uploadedFile'].name
        fileType = request.FILES['uploadedFile'].content_type
        charset = request.FILES['uploadedFile'].charset
        
        #
        #   This seems to handle utf-8 okay.  I'm not sure why . . . 
        #
        
        if os.path.exists(REPO_LOCATION + STOPWORDS_REPO_FOLDER + str(request.user) + '/') == False:
            os.mkdir(REPO_LOCATION + STOPWORDS_REPO_FOLDER + str(request.user) + '/')
        
        outF = open((REPO_LOCATION + STOPWORDS_REPO_FOLDER + str(request.user) + '/' + fileName).encode('utf-8'), 'w')
        for l in request.FILES['uploadedFile'].readlines():
            outF.write(l)
        outF.close()
        
        if fileExists == 'false':
            
            #addToGit(STOPWORDS_REPO_FOLDER, fileName)
            
            sw = StopwordFile(stopwordFileSystemName=str(request.user) + '/' + fileName, stopwordFileName=fileName, stopwordDescriptiveName=descriptiveName, stopwordFileOwner=str(request.user), stopwordFileNotes=notes)
            sw.save()
            
        else:
            
            sw = StopwordFile.objects.filter(stopwordFileSystemName=str(request.user) + '/' + fileName, stopwordFileOwner=str(request.user))[0]
            
            sw.stopwordDescriptiveName = descriptiveName
            sw.stopwordFileNotes = notes
            
            sw.save()
            
        #commitGit('Stopwords uploaded on ' + str(datetime.now()) + ' by ' + str(request.user))
        
        return render_to_response('ok.html')
    else:
            
        stopwordFileList = []
            
        stopwordFiles = StopwordFile.objects.all()
        
        for sw in stopwordFiles:
            
            stopwordFileList.append({'stopwordFileName': sw.stopwordFileName, 'stopwordFileOwner': sw.stopwordFileOwner, 'stopwordDescriptiveName': sw.stopwordDescriptiveName})
        
        return render_to_response('uploadStopwords.html', {'stopwordFileList': stopwordFileList, 'user': request.user})
    
    
