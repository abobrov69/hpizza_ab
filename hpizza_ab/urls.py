from django.conf.urls import patterns, include, url
#from views import MsgListView, BlogMainView, MsgDelete, MsgUpdate, display_meta, MsgView, BlogMainViewAnchor, AboutView
from django.conf import settings
import os
from tst import TstView

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples: d
    # url(r'^$', 'blog1.views.home', name='home'),
    # url(r'^blog1/', include('blog1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^tst/$', TstView.as_view()),
    )