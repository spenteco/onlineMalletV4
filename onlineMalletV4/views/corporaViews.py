from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse

from django.db import models
from django.db import connection
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.encoding import force_unicode
from django.contrib.auth import authenticate

from django.conf import settings

import simplejson as json

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
#from onlineMalletV4.gitFunctions import *

import os, time, sqlite3
from datetime import datetime
    
# ----------------------------------------------------------------------
#   HELPER FUNCTIONS
# ----------------------------------------------------------------------

def getFilesInCorpus(corpusName):

    start_time = time.time()
    
    results = []
    n = 0
    
    for corpus in Corpus.objects.filter(corpusName=corpusName):
            
        corpusContents = CorpusContent.objects.filter(corpus=corpus)
        
        for cc in corpusContents:
            
            results.append({"textFileName": cc.textFile.textFileName, "textFileOwner": cc.textFile.textFileOwner, "n": n})  
        
            n = n + 1 

    end_time = time.time()

    print 'getFilesInCorpus', (end_time - start_time)
            
    return results
    
def getFileTree():  

    #print 'starting getFileTree'

    start_time = time.time()

    temp = Corpus.objects.values('corpusOwner').distinct().order_by('corpusOwner')
    
    owners = []
    for t in temp:
        owners.append(t['corpusOwner'])

    #print 'owners', owners
    
    fileTree = []
    
    m = 0
    n = 0
    
    for owner in owners:

        owner_start_time = time.time()
        #print 'starting', owner
    
        allTextFiles = TextFile.objects.filter(textFileOwner=owner).order_by('textFileName')
    
        textFilesFound = []
        
        corpora = Corpus.objects.filter(corpusOwner=owner).order_by('corpusName')
        
        for c in corpora:
    
            folder = {"corpusName": c.corpusName, "corpusOwner": c.corpusOwner,  "corpusNotes": c.corpusNotes, "textFiles": [], "m": m}
            
            m = m + 1
        
            corpusContents = CorpusContent.objects.filter(corpus=c)
        
            textFileNames = []
    
            for cc in corpusContents:
                textFileNames.append([cc.textFile.textFileName, cc.textFile.textFileOwner])
    
            textFileNames.sort()

            loop_start_time = time.time()

            #print 'settings', settings

            #print 'connections', connections, dir(connections), connections.databases.keys()

            cursor = connection.cursor()
            #cursor = connections['my_db_alias'].cursor()

            cursor.execute('select c.textFileName from onlineMalletV4_corpus a, onlineMalletV4_corpuscontent b, onlineMalletV4_textfile c where a.id = ' + str(c.id) + ' and b.corpus_id = ' + str(c.id) + ' and b.textfile_id = c.id ORDER BY 1')

            rows = cursor.fetchall()
            for row in rows:
                folder["textFiles"].append({"textFileName": row[0], "textFileOwner": owner, "gitLogDetails": "", "n": n})
                n = n + 1
                textFilesFound.append([row[0], owner])
    
            #for t in textFileNames:
        
            #    for cc in corpusContents:
                
            #        if t[0] == cc.textFile.textFileName and t[1] == cc.textFile.textFileOwner:
         
            #            folder["textFiles"].append({"textFileName": cc.textFile.textFileName, "textFileOwner": cc.textFile.textFileOwner, "gitLogDetails": "", "n": n})
                    
            #            n = n + 1
                        
            #            textFilesFound.append([cc.textFile.textFileName, cc.textFile.textFileOwner])

            loop_end_time = time.time()

            #print 'LOOP', owner, (loop_end_time - loop_start_time), 'len(textFileNames)', len(textFileNames), 'len(corpusContents)', len(corpusContents)
                
            fileTree.append(folder) 
            
        textFilesNoCorpus = []
        
        #for a in allTextFiles:
        #    aFound = False
        #    for b in textFilesFound:
        #        if b[0] == a.textFileName and b[1] == a.textFileOwner:
        #            aFound = True
        #            break
        #    if aFound == False:
        #        textFilesNoCorpus.append([a.textFileName, a.textFileOwner])
                
        if len(textFilesNoCorpus) > 0:
    
            folder = {"corpusName": 'TEXTS NOT IN A CORPUS', "corpusOwner": c.corpusOwner,  "corpusNotes": "", "textFiles": [], "m": m}
            
            m = m + 1
            
            for t in textFilesNoCorpus:
         
                folder["textFiles"].append({"textFileName": t[0], "textFileOwner": t[1], "gitLogDetails": "", "n": n})
                
                n = n + 1
            
            fileTree.append(folder) 

        owner_end_time = time.time()

        #print 'DONE', owner, (owner_end_time - owner_start_time)

    end_time = time.time()

    print 'getFileTree', (end_time - start_time)
        
    return fileTree, owners
    
# ----------------------------------------------------------------------
#   CORPUS FILES   
# ----------------------------------------------------------------------

@login_required()
def viewCorpusFiles(request):
    
    fileTree, owners = getFileTree()
    
    return render_to_response('viewCorpusFiles.html', {"fileTree": fileTree, "fileLocation": REPO_LOCATION + CORPUS_REPO_FOLDER, "owners": owners})

@login_required()
def uploadCorpusFiles(request):    

    if request.method == 'POST':
        
        corpusName = request.POST['corpusName']
        notes = request.POST['notes']
        fileExists = request.POST['fileExists']
        
        fileName = request.FILES['uploadedFile'].name
        fileType = request.FILES['uploadedFile'].content_type
        charset = request.FILES['uploadedFile'].charset
        
        if os.path.exists(REPO_LOCATION + CORPUS_REPO_FOLDER + str(request.user) + '/') == False:
            os.mkdir(REPO_LOCATION + CORPUS_REPO_FOLDER + str(request.user) + '/')
        
        #
        #   This seems to handle utf-8 okay.  I'm not sure why . . . 
        #

        #print 'fileName', [fileName], 'fileType', fileType, 'charset', charset

        outputFilePathAndName = REPO_LOCATION + CORPUS_REPO_FOLDER + str(request.user) + '/' + unicode(fileName)

        outF = open(outputFilePathAndName.encode('utf-8'), 'w')
        for l in request.FILES['uploadedFile'].readlines():
            outF.write(l)
        outF.close()
        
        existingCorpus = None
        existingCorpora = Corpus.objects.filter(corpusName=corpusName)
        if len(existingCorpora) > 0:
            existingCorpus = existingCorpora[0]
        else:
            existingCorpus = Corpus(corpusName=corpusName, corpusNotes=notes, corpusOwner=request.user)
            existingCorpus.save()
        
        if fileExists == 'false':
            
            #addToGit(CORPUS_REPO_FOLDER, fileName)
            
            textFile = TextFile(textFileName=fileName, textFileOwner=request.user.username)
            textFile.save()
            
            corpusContents = CorpusContent(corpus=existingCorpus, textFile=textFile)
            corpusContents.save()

        else:
        
            textFile = TextFile.objects.filter(textFileName=fileName, textFileOwner=request.user.username)[0]

            #print 'len(textFile)', len(textFile)
            
            corpusContents = CorpusContent(corpus=existingCorpus, textFile=textFile)
            corpusContents.save()
            
        #commitGit('Corpus ' + corpusName + ' file ' + fileName + ' uploaded on ' + str(datetime.now()) + ' by ' + str(request.user))
        
        return render_to_response('ok.html')
    else:
    
        existingCorpora = []
        
        for c in Corpus.objects.all():
            if c.corpusOwner == request.user.username:
                existingCorpora.append({"corpusName": c.corpusName})
        
        corpusFileFileList = []
        
        allTextFiles = TextFile.objects.all().order_by('textFileName')
        for s in allTextFiles:
                
            corpusFileFileList.append({'textFileName': s.textFileName, 'textFileOwner': s.textFileOwner})
        
        return render_to_response('uploadCorpusFiles.html', {'user': request.user, "existingCorpora": existingCorpora, "corpusFileFileList": corpusFileFileList})
    
@login_required()
def maintainCorpora(request): 

    existingCorpora = []
    
    for c in Corpus.objects.all():
        if c.corpusOwner == request.user.username:
            existingCorpora.append({"corpusName": c.corpusName})

    
    return render_to_response('maintainCorpora.html', {'user': request.user, "existingCorpora": existingCorpora})
    
@login_required()
def createCorpus(request):

    if request.method == 'POST':
        
        corpusName = request.POST['corpusName']
        notes = request.POST['notes']
        
        existingCorpus = Corpus(corpusName=corpusName, corpusNotes=notes, corpusOwner=request.user)
        existingCorpus.save()
    
    return render_to_response('ok.html')
  
@login_required()
def listAllFiles(request):
    
    corpusName = request.GET['corpusName']
    
    corpusContents = getFilesInCorpus(corpusName)
    
    allTextFilesHash = {}
    
    n = 0
        
    textFiles = TextFile.objects.all()

    for t in textFiles:
        
        inCorpus = False
        for c in corpusContents:
            if c["textFileName"] == t.textFileName:
                inCorpus = True
                break
        
        if inCorpus == False:
            
            #gitLogDetails = gitLogForFile(CORPUS_REPO_FOLDER, t.textFileName)
            
            try:
                noop = allTextFilesHash[(t.textFileName, t.textFileOwner)]
            except KeyError:
                allTextFilesHash[(t.textFileName, t.textFileOwner)] = n
            
                n = n + 1
    
    allTextFiles = []
    
    for k, v in allTextFilesHash.iteritems():
        allTextFiles.append({"textFileName": k[0], "textFileOwner": k[1], "n": v})
    
    return render_to_response('fileList.html', {"files": allTextFiles, "whichPane": "allFiles"})
    
@login_required()
def getCorpusContents(request):
    
    corpusName = request.GET['corpusName']
    
    corpusContents = getFilesInCorpus(corpusName)
    
    return render_to_response('corpusContents.html', {"files": corpusContents, "whichPane": "corpusContents"})
    
@login_required()
def addToCorpus(request):
    
    corpusName = request.GET['corpusName']
    textFileName = request.GET['textFileName']
    textFileOwner = request.GET['textFileOwner']
        
    existingCorpus = None
    existingCorpora = Corpus.objects.filter(corpusName=corpusName)
    if len(existingCorpora) > 0:
        existingCorpus = existingCorpora[0]
            
    textFile = None
    tf = TextFile.objects.filter(textFileName=textFileName, textFileOwner=textFileOwner)
    if len(tf) > 0:
        textFile = tf[0]
        
    cc = CorpusContent(corpus=existingCorpus, textFile=textFile)
    cc.save()
    
    return render_to_response('ok.html')
    
@login_required()
def removeFromCorpus(request):
    
    corpusName = request.GET['corpusName']
    textFileName = request.GET['textFileName']
    textFileOwner = request.GET['textFileOwner']
        
    existingCorpus = None
    existingCorpora = Corpus.objects.filter(corpusName=corpusName, corpusOwner=str(request.user))
    if len(existingCorpora) > 0:
        existingCorpus = existingCorpora[0]
            
    textFiles = TextFile.objects.filter(textFileName=textFileName, textFileOwner=textFileOwner)
    for textFile in textFiles:
            
        corpusContent = None
        corpusContents = CorpusContent.objects.filter(corpus=existingCorpus, textFile=textFile)
        
        if len(corpusContents) > 0:
            corpusContent = corpusContents[0]
            corpusContent.delete()
    
    return render_to_response('ok.html')

