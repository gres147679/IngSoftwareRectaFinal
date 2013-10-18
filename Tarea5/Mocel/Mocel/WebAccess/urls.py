from django.conf.urls import *
from views import *

urlpatterns = patterns('Mocel.WebAccess.views',
	url(r'^$','index_view',name='vista_principal'),
	#url(r'^agregarCliente/$','agregar_cliente_view',name="vista_agregar_cliente"),

	url(r'^cliente/(\d+)/$','ver_productos'),
	url(r'^producto/([a-zA-Z0-9]+)/$','info_producto'),

	url(r'^login/$','login_view',name='vista_login'),
	url(r'^logout/$','logout_view',name='vista_logout'),
	url(r'^admin/WebAccess/facturar', pedirCliente),
    
    url(r'^pedirCliente/', pedirCliente),
    
    url(r'^buscarFactura/', buscarFactura),
    
    url(r'^buscarTodasFacturas/', buscarTodasFacturas),
)
