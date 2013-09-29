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
	    # Le corresponde la estrategia prepago
	    print "Se procedera a la generacion de la factura."
	    
        else:
	    # Le corresponde la estrategia postpago
	    print "Se procedera a la generacion de la factura."
            break
        
            
        
    
    
    
    return Factura(idCliente,numSerie)
    

class Factura:
    def __init__(self, idCliente,idProducto):                   
        self.idProducto = idProducto
        self.producto = pr.obtenerProducto(idProducto)
        self.cliente = mc.busquedaCliente(idCliente)
        self.observaciones = self.pedirObservaciones()
    
    def pedirObservaciones(self):
        
        while True:
            res = str(raw_input("Desea agregarle observaciones a la factura? [s/n]: "))
            if res == "s":
                return str(raw_input("Introduzca las observaciones:\n"))
            else:
                if res == "n":
                    return ""
                else:
                    print "Opción inválida\n"
        
        
if __name__ == '__main__':
    
    factura = pedirFactura()
    if factura and factura.montoTotalCobrar != -1:
        print factura
