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
    
    print "Realizando 8 pruebas sobre la factura Prepago..."
    print "La salida estandar solamente se mostrará si ocurre algún error"
    def setUp(self):
        self.myConsult = database.operacion(
        "Inserts de Prueba Prepago para probar la factura",
        None,self.dbname,self.dbuser,self.dbpass)
        d = datetime.datetime.today()
        mes = d.strftime("%m")
        anio = d.strftime("%Y")
        with open('entradaPruebas.txt', 'w+') as the_file:
	  the_file.write(str(mes)+'\n')
	  the_file.write(str(anio))
	  the_file.close()
        
        

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
        os.remove("entradaPruebas.txt")

    # Prueba 1
    ## Un celular prepago se afilia a un plan y no consume. Activa una tarjeta
    ## Debe resultar en el saldo de la tarjeta menos la renta del plan
    def test_casoBase(self):
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
	sys.stdin = open('entradaPruebas.txt','r') 
	testBill = Factura.Factura(22714709,"CBZ27326","")
	sys.stdin.close()
        result = afiliaciones.Afiliaciones("CBZ27326","").getSaldo()
        theoreticResult = 300
        try:
          self.assertEqual(result,theoreticResult,"Error en la Prueba Prepago 1: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("\nPrueba Prepago 1 FALLIDA")
	  return
        print("\nPrueba Prepago 1 lista")
    
    # Prueba Prepago 2
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo es cubierto enteramente por el plan.
    ## El saldo debe valer la recarga
    
    def test_unConsumoConAfiliacion(self):
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
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,50);
        commit;
        """)
        
        self.myConsult.execute()
	sys.stdin = open('entradaPruebas.txt','r') 
	testBill = Factura.Factura(22714709,"CBZ27326","")
	sys.stdin.close()
        result = afiliaciones.Afiliaciones("CBZ27326","").getSaldo()
        theoreticResult = 300
        try:
          self.assertEqual(result,theoreticResult,"Error en la Prueba Prepago 2: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("\nPrueba Prepago 2 FALLIDA")
	  return
        print("\nPrueba Prepago 2 lista")
        
        
    # Prueba Prepago 3
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo no es cubierto enteramente por el plan. Debe
    ## retornar el mismo monto que la prueba anterior. Este caso prueba si
    ## el sistema  rechaza consumos que no pueden facturarse
    
    def test_unConsumoConAfiliacionNoCabe(self):
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
        
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '20 days',101);
        
        
        
        commit;""")
        
        self.myConsult.execute()
	sys.stdin = open('entradaPruebas.txt','r') 
	testBill = Factura.Factura(22714709,"CBZ27326","")
	sys.stdin.close()
        result = afiliaciones.Afiliaciones("CBZ27326","").getSaldo()
        theoreticResult = 300
        result2 = len(testBill.metodoFacturacion.listaConsumos)
        try:
          self.assertTrue(result == theoreticResult and result2 == 0
          ,"Error en la Prueba Prepago 3: Se esperaba %d y %d, pero se recibio %d y %d" % (theoreticResult,0,result,result2));
        except AssertionError,e:
	  print e
	  print("\nPrueba Prepago 3 FALLIDA")
	  return
        print("\nPrueba Prepago 3 lista")
    
    # Prueba Prepago 4
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo no es cubierto enteramente por el plan. Esta
    ## vez se realizan varios consumos que en total exceden el plan. Debe
    ## retornar el mismo monto que la prueba anterior. Este caso prueba si
    ## el sistema  rechaza consumos que no pueden facturarse
    
    def test_variosConsumosConAfiliacionNoCaben(self):
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
        
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '20 days',51);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '21 days',49);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '21 days',3);
        
        
        commit;""")
        
        self.myConsult.execute()
	sys.stdin = open('entradaPruebas.txt','r') 
	testBill = Factura.Factura(22714709,"CBZ27326","")
	sys.stdin.close()
        result = afiliaciones.Afiliaciones("CBZ27326","").getSaldo()
        theoreticResult = 300
        result2 = len(testBill.metodoFacturacion.listaConsumos)
        try:
          self.assertTrue(result == theoreticResult and result2 == 0
          ,"Error en la Prueba Prepago 4: Se esperaba %d y %d, pero se recibio %d y %d" % (theoreticResult,0,result,result2));
        except AssertionError,e:
	  print e
	  print("\nPrueba Prepago 4 FALLIDA")
	  return
        print("\nPrueba Prepago 4 lista")
        
    # Prueba Prepago 5
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo no es cubierto enteramente por el plan, pero
    ## si por un paquete adicional. 
    ## Esta vez se realizan varios consumos que en total exceden el plan. Debe
    ## retornar el mismo monto que la prueba anterior. Este caso prueba si
    ## el sistema  rechaza consumos que no pueden facturarse
    
    def test_variosConsumosConAfiliacionYPaquete(self):
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
        
        insert into PAQUETE values
        (4001,'PegaoSMS',100);
        
        insert into CONTIENE values
        (4001,1001,300);
        
        insert into CONTRATA values
        ('CBZ27326',4001);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '20 days',51);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '21 days',49);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '21 days',3);
        
        
        commit;""")
        
        self.myConsult.execute()
	sys.stdin = open('entradaPruebas.txt','r') 
	testBill = Factura.Factura(22714709,"CBZ27326","")
	sys.stdin.close()
        result = afiliaciones.Afiliaciones("CBZ27326","").getSaldo()
        theoreticResult = 300
        theoreticResult2 = 3
        result2 = len(testBill.metodoFacturacion.listaConsumos)
        try:
          self.assertTrue(result == theoreticResult and result2 == theoreticResult2
          ,"Error en la Prueba Prepago 4: Se esperaba %d y %d, pero se recibio %d y %d" % (theoreticResult,theoreticResult2,result,result2));
        except AssertionError,e:
	  print e
	  print("\nPrueba Prepago 4 FALLIDA")
	  return
        print("\nPrueba Prepago 4 lista")
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
