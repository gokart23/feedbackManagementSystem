from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FeedBackManagement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'main.views.landingPage', name='landingPage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'main.views.verifyLogin', name='loginPage'),
    url(r'^addsurvey/(?P<o_id>\w+)/$',AddSurvey,name='add_survey'),
    url(r'^givesurvey/(?P<o_id>\w+)/$',GiveSurvey,name='give_survey'),
    url(r'^getanalytics/(?P<o_id>\w+)/$',AnalyticPage,name='get_analytics'),
    url(r'adduser/', CreateUser, name='addusers'),
    url(r'^addnotice/', AddNotice, name='add_notice'),
    url(r'^logout/$', user_logout, name="user_logout"),
)
