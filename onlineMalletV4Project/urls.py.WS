from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(settings.SITE_PREFIX + r'admin/' , include(admin.site.urls)),
    url(settings.SITE_PREFIX + r'accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(settings.SITE_PREFIX + r'logout/$', 'onlineMalletV4.views.generalViews.logOut'),
    
    url(settings.SITE_PREFIX + r'viewfile/', 'onlineMalletV4.views.generalViews.viewFile'),
    
    url(settings.SITE_PREFIX + r'viewstopwords/$', 'onlineMalletV4.views.stopwordViews.viewStopwords'),
    url(settings.SITE_PREFIX + r'uploadstopwords/$', 'onlineMalletV4.views.stopwordViews.uploadStopwords'),
    
    url(settings.SITE_PREFIX + r'viewcorpusfiles/$', 'onlineMalletV4.views.corporaViews.viewCorpusFiles'),
    url(settings.SITE_PREFIX + r'uploadcorpusfiles/$', 'onlineMalletV4.views.corporaViews.uploadCorpusFiles'),
    url(settings.SITE_PREFIX + r'createnewcorpus/$', 'onlineMalletV4.views.corporaViews.createCorpus'),
    url(settings.SITE_PREFIX + r'maintaincorpora/$', 'onlineMalletV4.views.corporaViews.maintainCorpora'),
    url(settings.SITE_PREFIX + r'maintainmetadata/$', 'onlineMalletV4.views.metadataViews.maintainMetadata'),
    url(settings.SITE_PREFIX + r'updatemetadata/$', 'onlineMalletV4.views.metadataViews.updateMetadata'),
    
    url(settings.SITE_PREFIX + r'listallfiles/$', 'onlineMalletV4.views.corporaViews.listAllFiles'),
    url(settings.SITE_PREFIX + r'getcorpuscontents/', 'onlineMalletV4.views.corporaViews.getCorpusContents'),
    url(settings.SITE_PREFIX + r'addtocorpus/', 'onlineMalletV4.views.corporaViews.addToCorpus'),
    url(settings.SITE_PREFIX + r'removefromcorpus/', 'onlineMalletV4.views.corporaViews.removeFromCorpus'),
    
    url(settings.SITE_PREFIX + r'runlda/$', 'onlineMalletV4.views.topicModelingViews.runLda'),
    url(settings.SITE_PREFIX + r'submitldajob/$', 'onlineMalletV4.views.topicModelingViews.submitLdaJob'),
    url(settings.SITE_PREFIX + r'listjobs/$', 'onlineMalletV4.views.topicModelingViews.listJobs'),
    url(settings.SITE_PREFIX + r'showjobdetails/$', 'onlineMalletV4.views.topicModelingViews.showJobDetails'),
    url(settings.SITE_PREFIX + r'getresultsfile/$', 'onlineMalletV4.views.topicModelingViews.getResultsFile'),
    url(settings.SITE_PREFIX + r'updatejobnotes/$', 'onlineMalletV4.views.topicModelingViews.updateJobNotes'),
    
    url(settings.SITE_PREFIX + r'startuberviz/$', 'onlineMalletV4.views.topicModelingViews.startUberViz'),
    url(settings.SITE_PREFIX + r'showheatmap/$', 'onlineMalletV4.views.topicModelingViews.showHeatMap'),
    
    #
    #   KEEP THIS ONE AT THE BOTTOM OF THE LIST; URLS NOT DESCRIBED ABOVE END UP HERE
    #
    
    url(settings.SITE_PREFIX + r'' , 'onlineMalletV4.views.generalViews.index'),
)
