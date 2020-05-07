# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^RequestESign$', views.reqeustESignhandler, name='RequestESign'),

    url(r'^GetESignResult$', views.getESignResulthandler, name='GetESignResult'),

    url(r'^RequestVerifyAuth$', views.reqeustVerifyAuthhandler, name='RequestVerifyAuth'),

    url(r'^GetVerifyAuthResult$', views.getVerifyAuthResulthandler, name='GetVerifyAuthResult'),

    url(r'^RequestCMS$', views.reqeustCMShandler, name='RequestCMS'),

    url(r'^GetCMSResult$', views.getCMSResulthandler, name='GetCMSResult'),
]
