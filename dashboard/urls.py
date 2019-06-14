from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    url(r'^database$', views.database, name='database'),
    url(r'^recurrentexp$', views.recurrentexp, name='recurrentexp'),
    url(r'^humanassets$', views.humanassets, name='humanassets'),
    url(r'^ictmaturityscore$', views.ictmaturityscore, name='ictmaturityscore'), 
    url(r'^accesslogweek$', views.accesslogweek, name='accesslogweek'),    
    url(r'^postcomment$', views.postcomment, name='postcomment'),   
    url(r'^socialnetworks$', views.socialnetworks, name='socialnetworks'),
    url(r'^businesscontinuity$', views.businesscontinuity, name='businesscontinuity'), 
    url(r'^contactcenter$', views.contactcenter, name='contactcenter'),  
    url(r'^datacenter$', views.datacenter, name='datacenter'),  
    url(r'^videomn$', views.videomn, name='videomn'),  
    url(r'^hardware$', views.hardware, name='hardware'),  
    url(r'^software$', views.software, name='software'),  
    url(r'^cloud$', views.cloud, name='cloud'), 
    url(r'^mobile$', views.mobile, name='mobile'), 
    url(r'^security$', views.security, name='security'), 
    url(r'^analytics$', views.analytics, name='analytics'), 
    url(r'^capex$', views.capex, name='capex'),
    url(r'^scenarios$', views.scenarios, name='scenarios'),     
    url(r'^help$', views.help, name='help'),   
    url(r'^gethumanassetdataall$', views.gethumanassetdataall, name='gethumanassetdataall'),   
    url(r'^gethumanassetdatajob$', views.gethumanassetdatajob, name='gethumanassetdatajob'),   
    url(r'^gethumanassetdataexp$', views.gethumanassetdataexp, name='gethumanassetdataexp'),
    url(r'^gethumanassetdataskill$', views.gethumanassetdataskill, name='gethumanassetdataskill'),
    url(r'^connectivity$', views.connectivity, name='connectivity'),   
    url(r'^accesslogmonth$', views.accesslogmonth, name='accesslogmonth'),    
    url(r'^accesslogytd$', views.accesslogytd, name='accesslogytd'),    
    url(r'^accesslogpytd$', views.accesslogpytd, name='accesslogpytd'),    
    url(r'^dynamiccat$', views.dynamiccat, name='dynamiccat'),    
    url(r'^postcommentsmtp$', views.postcommentsmtp, name='postcommentsmtp'),    
    
]