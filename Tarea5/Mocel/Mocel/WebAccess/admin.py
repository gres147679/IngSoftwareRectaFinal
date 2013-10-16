from django.contrib import admin
from Mocel.WebAccess.models import Cliente,Producto,Empresa,Afilia,Activa,Plan,Servicio,Contiene,Paquete,Incluye,Contrata

class ClienteAdmin(admin.ModelAdmin):
    fields = ['nombrecl','cedula','direccion']
   

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
admin.site.register(Contrata)