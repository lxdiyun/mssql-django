from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'ms.views.home', name='home'),
                       # url(r'^ms/', include('ms.foo.urls')),

                       # Uncomment the admin/doc line below to
                       # enable admin documentation:
                       # url(r'^admin/doc/',
                       # include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('rfid.urls')),
                       url(r'^checkcase/', include('checkcase.urls')),
                       url(r'^checkbook/', include('checkbook.urls')),
                       url(r'^log/', include('triggerlog.urls')),
                       url(r'^report/', include('report.urls')),
                       )
