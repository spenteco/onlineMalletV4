#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

def getFromFileSystem(folderName):

    print 'folderName', folderName

    for swFs in os.listdir(unicode(folderName)):

        a = folderName         
        b = swFs
        print type(swFs), [swFs]

        if os.path.isdir((a + b).encode('utf-8')) == True:
            getFromFileSystem(folderName + swFs + '/')
        else:
            print 'swFs', swFs, os.path.isdir((a + b).encode('utf-8'))

print
print
print 'sys.getdefaultencoding()', sys.getdefaultencoding()
print 'sys.getfilesystemencoding()', sys.getfilesystemencoding()
print 'sys.version_info', sys.version_info

#import os
#print os.popen("locale").read()

getFromFileSystem('/home/data2/onlineMallet/onlineMalletDataRepo/stopwords/')
