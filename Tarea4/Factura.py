# -*- coding: utf-8 -*-
import afiliaciones
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
import afiliaciones as af
from metodoFacturacionPostpago import metodoFacturacionPostpago
from metodoFacturacionPrepago import metodoFacturacionPrepago


class Factura(object):
    def __init__(self, idCliente,idProducto, obs):                   
        self.idProducto = idProducto
        self.producto = pr.obtenerProducto(idProducto)
        self.cliente = mc.busquedaCliente(idCliente)
        self.obs = obs
        
        if len(af.ConsultarPlanesPrepago(idProducto)) > 0:
            self.factura = metodoFacturacionPrepago(self.cliente, self.producto,idProducto, self.obs)
        elif len(af.ConsultarPlanesPostpago(idProducto)) > 0:
            self.factura = metodoFacturacionPostpago (self.cliente, self.producto,idProducto, self.obs)
    
    def __str__(self):
      return str(self.factura)
    
if __name__ == '__main__':
    factura = Factura(22714709,'CBZ27326','')
    print factura