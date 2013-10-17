from django.contrib import admin
from django.conf.urls import patterns, url
from ..views import pedirCliente

class AdminSiteWithPlus(admin.AdminSite):

    def get_urls(self):
        urls = super(AdminSiteWithPlus, self).get_urls()

	my_urls = patterns('',
	    url(r'^pedirCliente/', pedirCliente)
	)

	return my_urls + urls

customAdminSite = AdminSiteWithPlus()