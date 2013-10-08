#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import psycopg2
import database
import dbparams
import Factura
import metodoFacturacionPrepago
import sys,os
import datetime
import afiliaciones
import serviciosadicionales
import productos
import difflib

# Set de Pruebas para el MÃ³dulo Facturas
#
# Se han realizado una serie de pruebas unitarias destinadas a comprobar la eficacia
# del modulo Factura. En todas ellas se ensamblan casos de Prueba que dan un monto
# determinado de facturacion, y se compara este valor con el calculo. Se ignora la 
# impresion de la factura por cuestiones de sencillez
#
# En este set de pruebas siempre se incluyen consumos fuera
# del periodo de facturacion, para verificar bien
# que se revisen las fechas

class FacturaPrepagoTest(unittest.TestCase):
    # Parametros de conexion de la base de datos
    dbname = dbparams.dbname
    dbuser = dbparams.dbuser
    dbpass = dbparams.dbpass
    
    print "Realizando 2 pruebas sobre servicios adicionales..."
    print "La salida estandar solamente se mostrará si ocurre algún error"
    def setUp(self):
        self.myConsult = database.operacion(
        "Inserts de Prueba Prepago para probar la factura",
        None,self.dbname,self.dbuser,self.dbpass)
        d = datetime.datetime.today()
        mes = d.strftime("%m")
        anio = d.strftime("%Y")
        
        

    def tearDown(self):
        self.myConsult.setComando("""
        delete from consume cascade;
        delete from incluye cascade;
        delete from afilia cascade;
        delete from activa cascade;
        delete from plan_postpago cascade;
        delete from plan_prepago cascade;
        delete from plan cascade;
        delete from contiene cascade;
        delete from servicio cascade;
        delete from contrata cascade;
        delete from paquete cascade;
        delete from recarga cascade;
        delete from producto cascade;
        delete from cliente cascade;
        delete from empresa cascade;
        """)
        result = self.myConsult.execute()
        self.myConsult.cerrarConexion()

    # Prueba 1
    ## Un celular prepago se afilia a un plan y luego se afilia a un paquete
    ## de mensajes de texto
    def test_paqueteTexto(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into plan values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'prepago');
        
        insert into incluye values
        (3002,1001,0.1,100);
        
        insert into ACTIVA values
        ('CBZ27326',3002,0);
        
        insert into recarga values('CBZ27326',current_timestamp - interval '40 days',300);
        
        commit;
        """)
	
	self.myConsult.execute()
	producto31 = 'CBZ27326'
	productoTest = serviciosadicionales.Producto(producto31);
        productoTest = serviciosadicionales.MensajesDeTexto(productoTest)
        
        # Se obtiene la ultima parte de la descripcion del producto, que corresponde
        # a la descripcion del servicio adicional
        result = str(productoTest._desc).split('+')[1].strip()
        theoreticResult="Servicio de Mensajes de Texto"
        
        cost = productoTest._costo
        theoreticCost = 100
        
        try:
          self.assertTrue(result==theoreticResult and theoreticCost == cost,"Error en la Prueba Decoraciones  1");
        except AssertionError,e:
	  raise e
	  print("\nPrueba Decoraciones 1 FALLIDA")
	  return
        print("\nPrueba Decoraciones 1 lista")
    
    # Prueba 1
    ## Un celular prepago se afilia a un plan y luego se afilia a todos los
    ## paquetes implementados
    def test_todosPaquetes(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into plan values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'prepago');
        
        insert into incluye values
        (3002,1001,0.1,100);
        
        insert into ACTIVA values
        ('CBZ27326',3002,0);
        
        insert into recarga values('CBZ27326',current_timestamp - interval '40 days',300);
        
        commit;
        """)
	
	self.myConsult.execute()
	producto31 = 'CBZ27326'
	productoTest = serviciosadicionales.Producto(producto31);
        productoTest = serviciosadicionales.MensajesDeTexto(productoTest)
        productoTest = serviciosadicionales.SegundosMOCEL(productoTest)
        productoTest = serviciosadicionales.SegundosOtrasOperadoras(productoTest)
        productoTest = serviciosadicionales.MegabytesDeNavegacion(productoTest)
        
        
        # Se obtiene la ultima parte de la descripcion del producto, que corresponde
        # a la descripcion del servicio adicional
        preresult = str(productoTest._desc).split('+')[1:]
        result = ""
        for i in preresult:
	  result += i.strip()
        theoreticResult="Servicio de Mensajes de TextoServicio de Segundos adicionales a MOCELServicio \
de Segundos adicionales a otras operadorasServicio de Megabytes de Navegacion"        
       
	cost = productoTest._costo
	theoreticCost = 600
        
        try:
          self.assertTrue(result==theoreticResult and cost == theoreticCost,"Error en la Prueba Decoraciones  2");
        except AssertionError,e:
	  raise e
	  print("\nPrueba Decoraciones 2 FALLIDA")
	  return
        print("\nPrueba Decoraciones 2 lista")
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(buffer=True)
