from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from tellme2014.tellme  import views
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    # Examples:
#    # url(r'^$', 'tellme2014.views.home', name='home'),
#    # url(r'^tellme2014/', include('tellme2014.foo.urls')),
#
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('tellme2014.tellme.views',
        (r'^$','index'),
        (r'^(?P<url>(cid)|(site)|(line)|(userinfo)|(jtid)|(service))/$','display'),

        (r'^(?P<url>(cid))/add/$','addcid'),
         (r'^(?P<url>(jtid))/add/$','addjtid'),
        (r'^(?P<url>(site))/add/(?P<id>\w+)/$','addsite'),
        (r'^(?P<url>(line))/add/(?P<id>\w+)/$','addline'),
        (r'^(?P<url>(service))/add/(?P<id>\w+)/$','addservice'),
        (r'^(?P<url>(jtid))/add/(?P<id>\w+)/$','addjtid'),
        #(r'^(?P<url>(userinfo))/add/(?P<id>\w+)/$','add'),

        (r'^(?P<url>(cid))/edit/(?P<id>\d+)/$','editcid'),
        (r'^(?P<url>(site))/edit/(?P<id>\w+)/$','editsite'),
        (r'^(?P<url>(line))/edit/(?P<id>\w+)/$','editline'),
        (r'^(?P<url>(service))/edit/(?P<id>\w+)/$','editline'),
       (r'^(?P<url>(jtid))/edit/(?P<id>\w+)/$','editjtid'),
        #(r'^(?P<url>(cid)|(site)|(line)|(userinfo))/edit/(?P<id>\w+)/$','edit'),

        (r'^(?P<url>(cid)|(site)|(line)|(userinfo)|(service))/del/(?P<id>\w+)/$','delete'),
	(r'^(?P<url>(cid)|(site)|(line)|(userinfo)|(service))/addmonitor/(?P<id>\w+)/$','addmonitor'),
	(r'^(?P<url>(cid)|(site)|(line)|(userinfo)|(service))/addmrtg/(?P<id>\w+)/$','mrtgadd'),
        (r'^(?P<url>(cid)|(site)|(line)|(userinfo)|(jtid)|(service))/list/(?P<id>\w+)/(?P<flag>\d{1})/$','list'),
      
        (r'^search/$','search'),
)


urlpatterns += patterns('tellme2014.tellme.login',
        (r'^login/$','login_view'),
        (r'^logout/$','logout_view'),
       # (r'^user/$','register'),
        #(r'^user/del/(?P<id>\d+)/$','delete'),
        (r'^user/change_pass/$','change_pass'),
        #(r'^user/setpassword/(?P<id>\d+)/$','setpassword'),
 )

#urlpatterns += patterns('',
#     (r'^static/bootstrap/(?P<path>.*)$', 'django.views.static.serve',
#      #{'document_root': '/var/www/django/tellme2014/tellme2014/'}),
#     {'document_root':   settings.STATIC_ROOT}),
#)
