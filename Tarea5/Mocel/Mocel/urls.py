from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Mocel.views.home', name='home'),
    # url(r'^Mocel/', include('Mocel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
<<<<<<< HEAD
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^',include('Mocel.WebAccess.urls')),
=======
    url(r'^admin/', include(admin.site.urls)),
>>>>>>> e2295decfc9d7de24dc4726950b1148f0b6dffe2
)
