from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('Mocel.WebAccess.views',
	url(r'^agregarCliente/$','agregar_cliente_view',name="vista_agregar_cliente"),
)