from onlineMalletV4.models import *
from django.contrib import admin
from django.shortcuts import redirect
import datetime

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

class CorpusAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'corpusName', 'corpusOwner',)
    search_fields = ['corpusName', 'corpusOwner',]
    
admin.site.register(Corpus, CorpusAdmin)

class MetadataTypeAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'metadataType',)
    search_fields = ['metadataType',]
    
admin.site.register(MetadataType, MetadataTypeAdmin)

class MetadataEntryAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'metadataValue')
    search_fields = ['metadataValue']
    
admin.site.register(MetadataEntry, MetadataEntryAdmin)

class TextFileAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'textFileName', 'textFileOwner',)
    search_fields = ['textFileName', 'textFileOwner',]
    
admin.site.register(TextFile, TextFileAdmin)

class StopwordFileAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'stopwordFileName', 'stopwordDescriptiveName', 'stopwordFileOwner',)
    search_fields = ['stopwordFileName', 'stopwordFileOwner', 'stopwordDescriptiveName', 'stopwordFileNotes',]
    
admin.site.register(StopwordFile, StopwordFileAdmin)

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

class BatchJobAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'userId', 'dateTimeRequested', 'jobStatus')
    list_filter = ('userId', 'jobStatus')
    search_fields = ['jobParameters', ]
    
admin.site.register(BatchJob, BatchJobAdmin)

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------
