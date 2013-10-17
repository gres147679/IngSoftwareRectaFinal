from django.contrib import admin
from Mocel.WebAccess.models import *
from customAdmin import customAdminSite


class ClienteAdmin(admin.ModelAdmin):
    fields = ['nombrecl','cedula','direccion']


customAdminSite.register(Cliente,ClienteAdmin)

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Producto)
admin.site.register(Empresa)
admin.site.register(Afilia)
admin.site.register(Plan)
admin.site.register(Servicio)
admin.site.register(Contiene)
admin.site.register(Activa)
admin.site.register(Paquete)
admin.site.register(Incluye)
admin.site.register(Consume)
admin.site.register(PlanPostpago)
admin.site.register(PlanPrepago)
admin.site.register(Contrata)