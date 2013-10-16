from django.shortcuts import render_to_response
from django.template import RequestContext
from Mocel.WebAccess.forms import AgregarClienteForm
from Mocel.WebAccess.models import Cliente


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
