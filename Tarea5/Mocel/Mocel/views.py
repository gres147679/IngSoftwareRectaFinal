# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from Mocel.WebAccess.forms import AgregarClienteForm
from Mocel.WebAccess.models import *
from django.http import HttpResponse
import datetime

def pedirCliente (request):
    return render(request, 'pedirCliente.html')

def buscarFactura (request):
    if 'cedulaCliente' in request.POST:
        ced = request.POST['cedulaCliente']
        
        if not ced:
            message = 'Por favor, no deje el campo vacio'
        
        else:
            
            listaClientes = Cliente.objects.filter(cedula = ced)
            
            if not listaClientes:
                message = 'El cliente no tiene productos en la base de datos' 
                
            else:           
                cliente = listaClientes[0]
                listaProductos = Producto.objects.filter(cedula = cliente)
                
                if not listaProductos:
                    message = 'El cliente no tiene productos en la base de datos'    
                else:
                    listaFacturas = []
                    for pro in listaProductos:
                        factura = generarFactura(pro)
                        print factura
                        if factura:
                            listaFacturas.append(factura)
                    
                    pro = listaProductos[0]
                    return render(request, 'facturaPstpago.html', {'listaFacturas': listaFacturas})
    else:
        message = 'Por favor, no deje el campo vacio'
        
    return HttpResponse(message)

def generarFactura(Producto):
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
    
    totalConsumido = totalConsumidoPorServicio(Producto)
    
    totalPlan = totalPlanPorServicio(plan)
    
    
    totalPaquete = totalCostoPaquetes(Producto, totalPlan)
    
    listaCobrar = {}
   
    agregarRestoServicios(Producto, totalPlan)
    
    print totalPlan

    totalExceso = resumenConsumos(listaCobrar, totalConsumido, totalPlan)
    
    total = 0
    total = totalExceso + totalPaquete + plan.renta_basica
    
    return {    'producto': Producto,
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

def totalConsumidoPorServicio(Producto):
    
    fechaActual = datetime.date.today()
    listaConsumos = Consume.objects.filter(fecha__year = fechaActual.year, fecha__month= fechaActual.month, numserie = Producto).order_by('codserv')
    
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