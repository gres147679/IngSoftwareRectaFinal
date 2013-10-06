# -*- coding: utf-8 -*-
import afiliaciones
import moduloCliente as mc
import productos as pr
import validacion
from Factura import Factura


# Fachada para la factura
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
            break  
    
    mc.listarProductos(idCliente)
    print "\nIntroduzca la informacion del producto."
    
    while True:
        numSerie = validacion.validarInput(' Numero de Serie: ')        
        if (not mc.poseeprodCliente(idCliente,numSerie)):
            print " El producto no corresponde a dicho cliente."
            continue
        
        resultado = afiliaciones.ConsultarPlanesPostpago(numSerie)
        
        if len(afiliaciones.ConsultarPlanesPostpago(numSerie)) > 0 or len(afiliaciones.ConsultarPlanesPrepago(numSerie)) > 0:
            obs = pedirObservaciones()
            return Factura(idCliente, numSerie, obs)
        else:
            print "El producto no tiene planes asociados"
            return Null
          
if __name__ == '__main__':
    
    factura = pedirFactura()
    print factura
