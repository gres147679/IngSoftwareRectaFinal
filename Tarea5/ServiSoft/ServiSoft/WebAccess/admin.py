from django.contrib import admin
from ServiSoft.WebAccess.models import *
class ClienteAdmin(admin.ModelAdmin):
    fields = ['nombrecl','cedula','direccion']
   

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Usuario)
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
admin.site.register(Contrata)
admin.site.register(Recarga)
