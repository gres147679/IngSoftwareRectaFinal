from django.shortcuts import render_to_response, render
from django.template import RequestContext
from Mocel.WebAccess.forms import AgregarClienteForm
from Mocel.WebAccess.models import Cliente, Producto, Activa, Afilia
from Mocel.views import generarFactura

def index_view(request):
	return render_to_response('index.html',context_instance = RequestContext(request))
	
def agregar_cliente_view(request):
	if request.method == "POST":
		form = AgregarClienteForm(request.POST)
		info = "Inicializando"

		if form.is_valid():
			#Datos del cliente
			cedula = form.cleaned_data['cedula']
			nombrecl = form.cleaned_data['nombrecl']
			direccion = form.cleaned_data['direccion']

			c = Cliente()
			c.cedula = cedula
			c.nombrecl = nombrecl
			c.direccion = direccion
			c.save() #Guardo la informacion del cliente

			info = "Se agrego el cliente."
		else:
			info = "ERROR: Debe rellenar todos los campos."

		form = AgregarClienteForm()
		ctx = {'form':form, 'informacion':info}

		return render_to_response('crearCliente.html',ctx,context_instance=RequestContext(request))
	
	else: #GET
		form = AgregarClienteForm()
		ctx = {'form':form}
		return render_to_response('crearCliente.html',ctx,context_instance=RequestContext(request))

#
# Lista todos los clientes
#
def ver_clientes(request):
	listaCliente = Cliente.objects.all()
	if not listaCliente:
		mensaje = "ERROR: No hay clientes en la base de datos."
		context = {'lista_clientes': listaCliente, 'informacion':mensaje}
	else: 
		context = {'lista_clientes': listaCliente}
	return render_to_response('listarCliente.html',context,context_instance=RequestContext(request))
  
#
# Lista todos los productos de un cliente
#
def ver_productos(request,idcliente):
	idcl = idcliente
	c = Cliente.objects.get(cedula = idcliente)
	listaProducto = Producto.objects.filter()

	if not listaProducto:
		mensaje = "El cliente no tiene asociado ningun producto."
		context = {'lista_productos' : listaProducto, 'cedulaCliente' : idcl,'informacion':mensaje}
	else:
		context = {'lista_productos' : listaProducto, 'cedulaCliente' : idcl}
	return render_to_response('listarProducto.html',context,context_instance=RequestContext(request))
	
  
def info_producto(request, serieprod):
  producto = Producto.objects.get(numserie = serieprod)
  html = "infoSinPlan.html"
  context = {'producto' : producto}
  
  if (Activa.objects.filter(numserie = producto).count()):
    ac = Activa.objects.get(numserie = producto)
    html = 'infoPrepago.html'
    context = {'producto' : producto, 'saldo' : ac.saldo}
    return render(request, 'infoPrepago.html', context)
  
  if (Afilia.objects.filter(numserie = producto).count()):
    af = Afilia.objects.get(numserie = producto)
    html = 'infoPostpago.html'
    c = generarFactura(producto)
    context.update(c)
    return render(request, 'infoPostpago.html', context)
  
  return render(request, 'infoSinPlan.html', context)
