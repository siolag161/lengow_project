from django.conf.urls import *

urlpatterns = patterns('',
                       url(r'^', include('api.v0.urls')),  # only one version supported
                       )
