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

import os
from datetime import datetime
    
# ----------------------------------------------------------------------
#   HELPER FUNCTIONS
# ----------------------------------------------------------------------
    
def getFileTree(request):   
    
    fileTree = []
    
    corpora = Corpus.objects.filter(corpusOwner=str(request.user))
    
    corpusM = 0
    n = 0
    
    for c in corpora:
    
        folder = {'corpusName': c.corpusName, 'corpusOwner': c.corpusOwner,  'corpusNotes': c.corpusNotes, 'textFiles': [], 'm': corpusM}
        
        corpusM = corpusM + 1

        corpusMetadataTypesHash = {}
        
        corpusContents = CorpusContent.objects.filter(corpus=c)

        for cc in corpusContents:
            
            textMetadataTypes = []

            metadataEntries = MetadataEntry.objects.filter(metadataOwner=str(request.user), metadataCorpus=c, metadataTextFile=cc.textFile)
            for m in metadataEntries:

                corpusMetadataTypesHash[m.metadataType.metadataType] = 1
                textMetadataTypes.append([m.metadataType.metadataType, m.metadataValue])
            
            folder['textFiles'].append({'textFileName': cc.textFile.textFileName, 'textFileOwner': cc.owner, 'n': n, 'metadataTypes': textMetadataTypes})
            
            n = n + 1
            
        for t in folder['textFiles']:
            for k in corpusMetadataTypesHash.keys():
                kFound = False
                for m in t['metadataTypes']:
                    if k == m[0]:
                        kFound = True
                        break
                if kFound == False:
                    t['metadataTypes'].append([k, ''])    
        
        corpusMetadataTypes = []
        for cIndex, c in enumerate(sorted(corpusMetadataTypesHash.keys())):
            corpusMetadataTypes.append([cIndex, c]) 

        for t in folder['textFiles']:

            newTextMetadataTypes = []
            for a in range(0, len(corpusMetadataTypes)):
                newTextMetadataTypes.append('')

            for cIndex, c in enumerate(corpusMetadataTypes):
                for m in t['metadataTypes']:
                    if m[0] == c[1]:
                        newTextMetadataTypes[cIndex] = [cIndex, c, m[1]]
                        break 

            newTextMetadataTypes.append([len(corpusMetadataTypes), '', ''])

            t['metadataTypes'] = newTextMetadataTypes

        corpusMetadataTypes.append([len(corpusMetadataTypes), ''])
        
        folder['corpusMetadataTypes'] = corpusMetadataTypes

        fileTree.append(folder) 
        
    return fileTree
    
# ----------------------------------------------------------------------
#   CORPUS FILES   
# ----------------------------------------------------------------------

@login_required()
def maintainMetadata(request):
    
    fileTree = getFileTree(request)

    return render_to_response('maintainMetadata.html', {'fileTree': fileTree, 'fileLocation': REPO_LOCATION + CORPUS_REPO_FOLDER})

@login_required()
def updateMetadata(request):
    
    updateParameters = json.loads(request.GET['data'])

    metadataType = None
    metadataTypes = MetadataType.objects.filter(metadataType=updateParameters['metadataType'], metadataOwner=str(request.user))
    if len(metadataTypes) == 0:
        metadataType = MetadataType(metadataType=updateParameters['metadataType'], metadataOwner=str(request.user))
        metadataType.save()
    else:
        metadataType = metadataTypes[0]
    
    corpus = None
    corpora = Corpus.objects.filter(corpusName=updateParameters['corpusName'])
    if len(corpora) > 0:
        corpus = corpora[0]
        
    textFile = None
    textFiles = TextFile.objects.filter(textFileName=updateParameters['fileName'])
    if len(textFiles) > 0:
        textFile = textFiles[0]

    metadataEntry = None
    metadataEntries = MetadataEntry.objects.filter(metadataOwner=str(request.user), metadataCorpus=corpus, metadataTextFile=textFile, metadataType=metadataType)
    if len(metadataEntries) == 0:
        if updateParameters['metadataValue'].strip() > '':
            metadataEntry = MetadataEntry(metadataOwner=str(request.user), metadataCorpus=corpus, metadataTextFile=textFile, metadataType=metadataType, metadataValue=updateParameters['metadataValue'])
            metadataEntry.save()
    else:
        metadataEntry = metadataEntries[0]
        if updateParameters['metadataValue'].strip() > '':
            metadataEntry.metadataValue=updateParameters['metadataValue']
            metadataEntry.save()
        else:
            metadataEntry.delete()

    return render_to_response('ok.html')

