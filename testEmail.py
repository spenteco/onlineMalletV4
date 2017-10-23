#!/usr/bin/env python

import os, sys, time, codecs, commands
from datetime import date, time, datetime
import time
import simplejson as json
import smtplib
from smtplib import SMTPException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *
from onlineMalletV4.applicationSettings import *
from onlineMalletV4.gitFunctions import *

import logging

#-----------------------------------------------------------------------
#   MAIN
#-----------------------------------------------------------------------

if __name__ == '__main__':

    batchJobId = int(sys.argv[1])

    batchJob = BatchJob.objects.filter(id=batchJobId)[0]

    sender = 'spenteco@wustl.edu'
    receivers = ['spentecost@email.wustl.edu', batchJob.userEmail]

    message ='From:  ' + sender + '\n' + 'To: ' + batchJob.userEmail + '\n' + 'Subject: Mallet batch job completion' + '\n' + batchJob.userFirstName + ',' + '\n' + 'The mallet job you requested at ' + str(batchJob.dateTimeRequested) + 'has completed.'

    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, message)    
    except SMTPException:      
        print 'oops'
