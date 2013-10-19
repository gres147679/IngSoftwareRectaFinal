from django.shortcuts import render_to_response, render, HttpResponse
from django.template import RequestContext
from ServiSoft.WebAccess.forms import *
from ServiSoft.WebAccess.models import *
from ServiSoft.views import generarFactura
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
import datetime

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
	listaProducto = Producto.objects.filter(cedula = c)

	if not listaProducto:
		mensaje = "El cliente no tiene asociado ningun producto."
		context = {'lista_productos' : listaProducto, 'cedulaCliente' : idcl,'informacion':mensaje}
	else:
		context = {'lista_productos' : listaProducto, 'cedulaCliente' : idcl}
	return render_to_response('listarProducto.html',context,context_instance=RequestContext(request))
	
  
def info_producto(request, serieprod):
	producto = Producto.objects.get(numserie = serieprod)
	context = {'producto' : producto}
  
	if (Activa.objects.filter(numserie = producto).count()):
		ac = Activa.objects.get(numserie = producto)
		context = {'producto' : producto, 'saldo' : ac.saldo}
		return render_to_response('infoPrepago.html',context,context_instance=RequestContext(request))
  
	if (Afilia.objects.filter(numserie = producto).count()):
		af = Afilia.objects.get(numserie = producto)
		fechaActual = datetime.date.today()
		c = generarFactura(producto,fechaActual.month,fechaActual.year)
		context.update(c)
		return render_to_response('infoPostpago.html',context,context_instance=RequestContext(request))
  
	return render_to_response('infoSinPlan.html',context,context_instance=RequestContext(request))



#funcion auxiliar que autentica el usuario
def autenticar(username, password):

  if not username.isdigit():
    return False  

  if Cliente.objects.filter(cedula = username).count():
    cl = Cliente.objects.get(cedula = username)
    if Usuario.objects.filter(cedula = cl).count():
      user = Usuario.objects.get(cedula = cl)
      
      return user.password == password
    
  return False

def login_view(request):
  	mensaje = ""
  	if request.user.is_authenticated():
  		return HttpResponseRedirect('/')
  	else:
  		if request.method == "POST":
			form = loginForm(request.POST)
			info = "Inicializando"

			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				#usuario = authenticate(username=username,password=password)

				if autenticar(username,password):
					#login(request,usuario)
					redirect = '/cliente/' + str(username)
					return HttpResponseRedirect(redirect)
				else:
					mensaje = "ERROR: usuario y/o password incorrecto."
		form = loginForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))
		
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def pedirCliente (request):
    return render(request, 'pedirCliente.html', {'form': pedirDatosFacturacionForm} )

def buscarTodasFacturas(request):
    listaClientes = Cliente.objects.all()
    listaFacturas = []
    fechaActual = datetime.date.today()
    if listaClientes:
        for cliente in listaClientes:
            listaProductos = Producto.objects.filter(cedula = cliente)
            for producto in listaProductos:
                factura = generarFactura(producto, fechaActual.month, fechaActual.year)
                if factura:
                    listaFacturas.append(factura)
                        
        return render(request, 'facturaPstpago.html', {'listaFacturas': listaFacturas})
    else:
        return HttpResponse("No hay clientes en la base de datos")
    
def buscarFactura (request):
    if request.method == 'POST':
        form = pedirDatosFacturacionForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            ced = cd['cedula']
            mes = cd['mes']
            anio = cd['anio']
            
            listaClientes = Cliente.objects.filter(cedula = ced)
            
            if not listaClientes:
                return render(request, 'pedirCliente.html', {'form': form, 'error' : "El cliente no existe en la base de datos"})   
                
            else:           
                cliente = listaClientes[0]
                listaProductos = Producto.objects.filter(cedula = cliente)
                
                if not listaProductos:
                    return render(request, 'pedirCliente.html', {'form': form, 'error' : "El cliente no tiene productos en la base de datos"})   
                else:
                    listaFacturas = []
                    for pro in listaProductos:
                        factura = generarFactura(pro, mes, anio)
                        if factura:
                            listaFacturas.append(factura)
                    
                    pro = listaProductos[0]
                    return render(request, 'facturaPstpago.html', {'listaFacturas': listaFacturas})
        else:
            return render(request, 'pedirCliente.html', {'form': form, 'error' : "Debe rellenar todos los campos"})
        
def generarFactura(Producto, mes, anio):
    afilia = Afilia.objects.filter(numserie = Producto)
    
    if not afilia:
        activa = Activa.objects.filter(numserie = Producto)
        
        if not activa:
            return None
        
        else:
            postpago = False
            planP = activa[0].codplan
        
    else:
        postpago = True
        
        planP = afilia[0].codplan
        
    plan = planP.codplan
    
    rentaPlan = plan.renta_basica
    
    nombrePlan = plan.nombreplan
    
    totalConsumido = totalConsumidoPorServicio(Producto, mes, anio)
    
    totalPlan = totalPlanPorServicio(plan)
    
    
    totalPaquete = totalCostoPaquetes(Producto, totalPlan)
    
    listaCobrar = {}
   
    agregarRestoServicios(Producto, totalPlan)

    totalExceso = resumenConsumos(listaCobrar, totalConsumido, totalPlan)
    
    total = 0
    total = totalExceso + totalPaquete + plan.renta_basica

    fechaActual = datetime.date.today()

    return {    'anioFacturacion': anio,
                'mesFacturacion': mes,
                'fechaActual': fechaActual,
                'producto': Producto,
                'postpago': postpago,
                'total': total,
                'listaCobrar': listaCobrar,
                'totalPlan' : plan.renta_basica,
                'totalPaquetes': totalPaquete,
                'totalExceso': totalExceso,
                'cliente': Producto.cedula,
                }

def agregarRestoServicios(Producto, totalPlan):
    
    for servicio in Consume.objects.filter(numserie = Producto):
        codserv = servicio.codserv.codserv
        if not totalPlan.has_key(codserv):
            totalPlan[codserv] = [0, servicio.codserv.costo, str(servicio.codserv.nombreserv)]

def resumenConsumos (listaCobrar, totalConsumido, totalPlan):
    
    total = 0
    
    for con in totalConsumido.keys():
            consumido = totalConsumido[con]
            limite = totalPlan[con][0]
            listaCobrar[con] = [totalPlan[con][2], consumido, limite, 0]
            if consumido > limite:
                exceso = (consumido - limite) * totalPlan[con][1]
                total = total + exceso
                listaCobrar[con][3] = exceso
    
    return total

def totalCostoPaquetes(Producto, totalPlan):
    listaPaquetes = Contrata.objects.filter(numserie = Producto)
    costoPaquetes = 0
        
    for row in listaPaquetes:
        listaServicioPaquete = Contiene.objects.filter(codpaq = row.codpaq)
        
        for servicio in listaServicioPaquete:
            codserv = servicio.codserv.codserv
            if totalPlan.has_key(codserv):
                totalPlan[codserv][0] = totalPlan[codserv][0] + int(servicio.cantidad)
            else:
                totalPlan[codserv] = [int(servicio.cantidad), servicio.codserv.costo, str(servicio.codserv.nombreserv)]
            
            print str(servicio.codserv.codserv) + ' ' + str(servicio.cantidad)
        
        costoPaquetes += row.codpaq.precio

    return costoPaquetes
 
def totalPlanPorServicio(plan):
    listaPlan = Incluye.objects.filter(codplan = plan)
    
    for row in listaPlan:
        print str(row.codserv.codserv) + ' ' + str(row.cantidad) + ' ' + str(row.tarifa)
    
    totalPlan = {}
    
    for row in listaPlan:
        totalPlan[row.codserv.codserv] = [row.cantidad, row.tarifa, str(row.codserv.nombreserv)]    
    
    return totalPlan

def totalConsumidoPorServicio(Producto, mes, anio):
    
    listaConsumos = Consume.objects.filter(fecha__year = anio, fecha__month= mes, numserie = Producto).order_by('codserv')
    
    for consumo in listaConsumos:
        print str(consumo.fecha) + ' ' + consumo.numserie.numserie + ' ' + consumo.codserv.nombreserv + ' ' + str(consumo.cantidad)
        
    totalConsumido = {}
    
    for consumo in listaConsumos:
        codserv = consumo.codserv.codserv
        if totalConsumido.has_key(codserv):
            totalConsumido[codserv] = totalConsumido[codserv] + int(consumo.cantidad)
        else:
            totalConsumido[codserv] = int(consumo.cantidad)
            
            
    return totalConsumido
