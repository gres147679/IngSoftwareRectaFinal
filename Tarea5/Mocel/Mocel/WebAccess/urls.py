from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('Mocel.WebAccess.views',
	url(r'^$','index_view',name='vista_principal'),
	url(r'^agregarCliente/$','agregar_cliente_view',name="vista_agregar_cliente"),
	url(r'^cliente/$','ver_clientes'),
	url(r'^cliente/(\d+)/$','ver_productos'),
	url(r'^producto/(\d+)/$','info_producto'),
)
