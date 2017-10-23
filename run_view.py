#!/usr/bin/env python

import os, sys, time, codecs, commands, re
from datetime import date, time, datetime
import time
import simplejson as json
import smtplib
from email.MIMEText import MIMEText

import site
from onlineMalletV4.applicationSettings import *
site.addsitedir(SITE_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineMalletV4Project.settings')

from onlineMalletV4.models import *
from onlineMalletV4.views.corporaViews import *
from onlineMalletV4.applicationSettings import *
from onlineMalletV4.gitFunctions import *
from django.utils.encoding import smart_str, smart_unicode

import logging


#-----------------------------------------------------------------------
#   MAIN
#-----------------------------------------------------------------------

if __name__ == '__main__':

    getFileTree()
