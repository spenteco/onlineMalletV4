from django.db import models
from datetime import datetime

# ----------------------------------------------------------------------
#    
# ----------------------------------------------------------------------

class Corpus(models.Model):

    def __unicode__(self):
        return u"%s" % self.id
    
    id = models.AutoField(primary_key=True)
    corpusName = models.CharField("Corpus Name", blank=False, max_length=128)
    corpusOwner = models.CharField("Owner", max_length=64)
    corpusNotes = models.TextField("Notes", blank=True)

class TextFile(models.Model):

    def __unicode__(self):
        return u"%s" % self.id
    
    id = models.AutoField(primary_key=True)
    textFileName = models.CharField("Text File Name", blank=False, max_length=128)
    textFileOwner = models.CharField("Owner", max_length=64)
    
class CorpusContent(models.Model):

    def __unicode__(self):
        return u"%s" % self.id
    
    id = models.AutoField(primary_key=True)
    owner = models.CharField("Owner", max_length=64)
    corpus = models.ForeignKey(Corpus, null=False)
    textFile = models.ForeignKey(TextFile, null=False)

class MetadataType(models.Model):

    def __unicode__(self):
        return u"%s" % self.id
    
    id = models.AutoField(primary_key=True)
    metadataOwner = models.CharField("Owner", max_length=64)
    metadataType = models.CharField("Metadata type", max_length=64)

class MetadataEntry(models.Model):

    def __unicode__(self):
        return u"%s" % self.id
    
    id = models.AutoField(primary_key=True)
    metadataOwner = models.CharField("Owner", max_length=64)
    metadataCorpus = models.ForeignKey(Corpus, null=True)
    metadataTextFile = models.ForeignKey(TextFile, null=True)
    metadataType = models.ForeignKey(MetadataType, null=True)
    metadataValue = models.CharField("Metadata value", max_length=64)

class StopwordFile(models.Model):

    def __unicode__(self):
        return u"%s" % self.id
    
    id = models.AutoField(primary_key=True)
    stopwordFileSystemName = models.CharField("File System Name", blank=False, max_length=128)
    stopwordFileName = models.CharField("Text File Name", blank=False, max_length=128)
    stopwordDescriptiveName = models.CharField("Text File Name", blank=False, max_length=128, default="")
    stopwordFileOwner = models.CharField("Owner", max_length=64)
    stopwordFileNotes = models.TextField("Notes")
    dateLastModified = models.DateTimeField(auto_now=True, auto_now_add=True, default=datetime.now())
    
# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------
    
class BatchJob(models.Model):
    
    STATUS_CHOICES = (
        ('Queued', 'Queued'),
        ('Running', 'Running'),
        ('Failed', 'Failed'),
        ('Completed', 'Completed'),
    )

    def __unicode__(self):
        return u"%s" % self.id
        
    id = models.AutoField(primary_key=True)
    userId = models.CharField("User id", blank=False, max_length=128)
    dateTimeRequested = models.DateTimeField('When Requested', auto_now_add=True, default=datetime.now())
    timestamp = models.CharField("Unix timestamp", blank=False, max_length=12)
    userEmail = models.CharField("User id", blank=False, max_length=128)
    userFirstName = models.CharField("User id", blank=False, max_length=128)
    jobType = models.CharField("Type", blank=False, max_length=16, default='')
    jobStatus = models.CharField("Job status", choices=STATUS_CHOICES, max_length=32)
    pid = models.CharField("Process id", blank=False, max_length=12)
    logfileName = models.CharField("Logfile name", blank=False, max_length=256)
    jobParameters = models.TextField("Notes", blank=False)
    jobNotes = models.TextField("Notes", blank=True, default='')
    
    
# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

