# -*- coding: utf-8 -*-
import Afiliaciones
import psycopg2
import psycopg2.extras
import unittest
import cliente as cl
import moduloCliente as mc
import consumos
import productos as pr
import validacion
import database as db
import dbparams
import datetime
import metodoFacturacionPostpago

def pedirObservaciones():
        
        while True:
            res = str(raw_input("Desea agregarle observaciones a la factura? [s/n]: "))
            if res == "s":
                return str(raw_input("Introduzca las observaciones:\n"))
            else:
                if res == "n":
                    return ""
                else:
                    print "Opción inválida\n"    

def buscarMes():
        return str(raw_input("Por favor, introduzca el mes de facturacion (MM): "))
    
def buscarAnio():
    return str(raw_input("Por favor, introduzca el año de facturacion (YYYY): "))

def pedirFactura():
    
    if (pr.cantidadProductos() == 0):
        print "No hay ningun producto en el sistema."
        print "No se puede generar una factura."
        return
    
    
    print "Introduzca la informacion del cliente."
    idCliente = None
    
    while True:
        idCliente = int(validacion.validarNumero(' Cedula: '))        
        if (not mc.existeCliente(idCliente)):
            print " El cliente no se encuentra en el sistema."
        else:   
            if (not Afiliaciones.verificarCliente(idCliente)):
                print " El cliente no posee productos postpago en el sistema."
            else:
                break  
    
    mc.listarProductos(idCliente)
    print "\nIntroduzca la informacion del producto."
    
    while True:
        numSerie = validacion.validarInput(' Numero de Serie: ')        
        if (not mc.poseeprodCliente(idCliente,numSerie)):
            print " El producto no corresponde a dicho cliente."
            continue
        
        resultado = Afiliaciones.ConsultarPlanesPostpago(numSerie)
        
        if not resultado or len(resultado) == 0:
            # Este producto no está afiliado a un plan postpago
            resultado = Afiliaciones.ConsultarPlanesPrepago(numSerie)
            if not resultado or len(resultado) == 0:
	      print "Este producto no esta afiliado a ningun plan"
	    else:
	      # Este producto está afiliado a un plan prepago
	      print "Se procedera a la generacion de la factura."
	      obs = pedirObservaciones()
	      # Asignacion y ejecucion de la estrategia metodoFacturacionPrepago
	      myBill = Factura(idCliente,numSerie)
	      print myBill
	      break
        else:
	  # Este producto está afiliado a un plan postpago
	  mes = buscarMes()
	  anio = buscarAnio()
	  obs = pedirObservaciones()
	  print "Se procedera a la generacion de la factura."
	  # Asignacion y ejecucion de la estrategia metodoFacturacionPostpago
	  myBill = Factura(idCliente,numSerie,mes,anio,obs)
	  print myBill
          break
        
    

class Factura:
    def __init__(self, idCliente,idProducto):                   
        self.idProducto = idProducto
        self.producto = pr.obtenerProducto(idProducto)
        self.cliente = mc.busquedaCliente(idCliente)
        # Crea un metodoFacturacionPrepago
        # Todavia no existe, pero la firma debe ser
        #self.metodoFacturacion = metodoFacturacionPrepago.metodoFacturacionPostpago(idProducto)
        
    def __init__(self, idCliente,idProducto,mesFacturacion,anioFacturacion,obs):                   
        self.idProducto = idProducto
        self.producto = pr.obtenerProducto(idProducto)
        self.cliente = mc.busquedaCliente(idCliente)
        # Crea un metodoFacturacionPostpago
        self.metodoFacturacion = metodoFacturacionPostpago.metodoFacturacionPostpago(self.producto,self.idProducto,self.cliente,mesFacturacion,anioFacturacion,obs)
    
    def __str__(self):
      return str(self.metodoFacturacion)
if __name__ == '__main__':
    
    factura = pedirFactura()
    if factura and factura.montoTotalCobrar != -1:
        print factura
