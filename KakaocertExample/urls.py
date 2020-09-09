# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^RequestESign$', views.reqeustESignhandler, name='RequestESign'),

    url(r'^GetESignResult$', views.getESignStatehandler, name='GetESignResult'),

    url(r'^VerifyESign$', views.verifyESignhandler, name='VerifyESign'),

    url(r'^RequestVerifyAuth$', views.reqeustVerifyAuthhandler, name='RequestVerifyAuth'),

    url(r'^GetVerifyAuthResult$', views.getVerifyAuthStatehandler, name='GetVerifyAuthResult'),

    url(r'^VerifyAuth$', views.verifyAuthhandler, name='VerifyAuth'),

    url(r'^RequestCMS$', views.reqeustCMShandler, name='RequestCMS'),

    url(r'^GetCMSResult$', views.getCMSStatehandler, name='GetCMSResult'),

    url(r'^VerifyCMS$', views.verifyCMShandler, name='VerifyCMS'),
]
