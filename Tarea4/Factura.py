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
from metodoFacturacionPostpago import metodoFacturacionPostpago


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
        self.metodoFacturacion = metodoFacturacionPostpago(self.producto,self.idProducto,self.cliente,mesFacturacion,anioFacturacion,obs)
    
    def __str__(self):
      return str(self.metodoFacturacion)
    
if __name__ == '__main__':
    print "Para usar este modulo utilize la interfaz gestionarFactura"
