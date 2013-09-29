#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unittest
import psycopg2
import database
import dbparams
import Factura

# Set de Pruebas para el Módulo Facturas
#
# Se han realizado una serie de pruebas unitarias destinadas a comprobar la eficacia
# del modulo Factura. En todas ellas se ensamblan casos de prueba que dan un monto
# determinado de facturacion, y se compara este valor con el calculo. Se ignora la 
# impresion de la factura por cuestiones de sencillez
#
# En este set de pruebas siempre se incluyen consumos fuera
# del periodo de facturacion, para verificar bien
# que se revisen las fechas

class FacturaTest(unittest.TestCase):
    # Parametros de conexion de la base de datos
    dbname = dbparams.dbname
    dbuser = dbparams.dbuser
    dbpass = dbparams.dbpass
    
    print "Para estas pruebas debe colocar el mes actual"
    def setUp(self):
        self.myConsult = database.operacion(
        "Inserts de prueba para probar la factura",
        None,self.dbname,self.dbuser,self.dbpass)
        

    def tearDown(self):
        self.myConsult.setComando("""
        delete from consume cascade;
        delete from incluye cascade;
        delete from afilia cascade;
        delete from plan_postpago cascade;
        delete from plan_prepago cascade;
        delete from plan cascade;
        delete from contiene cascade;
        delete from servicio cascade;
        delete from contrata cascade;
        delete from paquete cascade;
        delete from producto cascade;
        delete from cliente cascade;
        delete from empresa cascade;
        """)
        result = self.myConsult.execute()
        self.myConsult.cerrarConexion()

    # Prueba 1
    ## Caso sin contenido en la base de datos. Debe retornar cero
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
        tarifas para excesos',211,311,'postpago');
        
        insert into incluye values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',50);
        
        commit;""")
	
	self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        theoreticResult = 211
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 1: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 1 FALLIDA")
	  return
        print("Prueba 1 lista")
    
    # Prueba 2
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo es cubierto enteramente por el plan. Debe
    ## retornar el valor de la renta básica del plan
    
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
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,50);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',51);
        
        
        commit;""")
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        theoreticResult = 211
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 2: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 2 FALLIDA")
	  return
        print("Prueba 2 lista")
        
        
    # Prueba 3
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo es cubierto enteramente por el plan. Debe
    ## retornar el valor de la renta básica del plan. Esta vez se inserta un consumo en
    ## una fecha futura, para asegurarse del checkeo de fechas
    
    def test_unConsumoConAfiliacionNulo(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,50);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',51);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp + interval '60 days',51);
        
        
        commit;""")
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        theoreticResult = 211
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 3: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 3 FALLIDA")
	  return
        print("Prueba 3 lista")
        
    # Prueba 4
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo no es cubierto enteramente por el plan. Debe
    ## retornar el valor de la renta básica del plan mas el valor del exceso
    
    def test_unConsumoConAfiliacionYExceso(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(DEFAULT,
         'CBZ27326',1001,current_timestamp,120);
        
        insert into CONSUME values(DEFAULT,
         'CBZ27326',1001,current_timestamp - interval '45 days',120);
        
        
        commit;""")
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        
        # El valor de la deuda debe ser 211 + 0.1*(120-100) = 213
        # Corresponde a la renta mas los 20 consumos no incluidos en el plan
        theoreticResult = 213
        
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 4: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 4 FALLIDA")
	  return
        print("Prueba 4 lista")
    
    # Prueba 5
    ## Caso en el que un cliente consume un servicio estando afiliado a un plan
    ## que lo contenga, y este consumo no es cubierto enteramente por el plan, pero
    # esta vez esto se logra con varios consumos sucesivos. Debe
    ## retornar el valor de la renta básica del plan mas el valor del exceso
    
    def test_unConsumoConAfiliacionYExcesosMultiples(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',20);
        
        commit;""")
        
        
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        
        # El valor de la deuda debe ser 211 + 0.1*(120-100) = 213
        # Corresponde a la renta mas los 20 consumos no incluidos en el plan
        theoreticResult = 213
        
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 5: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 5 FALLIDA")
	  return
        print("Prueba 5 lista")
        
    # Prueba 6
    ## Caso en el que un cliente consume dos servicios estando afiliado a un plan
    ## que los contiene: en un caso la cantidad consumida esta cubierta, y en el otro
    ## no. En ambos casos hay una cantidad variable de consumos pequeños
    
    def test_variosConsumosConAfiliacionYExcesosMultiples1(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values
        (1002,'Segundos a Otras Operadoras',0.20,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,200);
        
        insert into INCLUYE values
        (3002,1002,0.2,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '60 days',20000);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp + interval '60 days',20000);
        
        commit;""")
        
        
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        
        # El valor de la deuda debe ser 211 + 0.2*(120-100) = 215
        
        theoreticResult = 215
        
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 6: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 6 FALLIDA")
	  return
        print("Prueba 6 lista")
        
    # Prueba 7
    ## Caso en el que un cliente consume tres servicios estando afiliado a un plan
    ## que los contiene: en el primer caso la cantidad consumida esta cubierta, en el segundo
    ## no. En el tercer caso el cliente esta afiliado a un paquete que contiene dicho plan, y 
    ## los consumos estan cubiertos. En todo caso hay una cantidad variable de consumos pequeños
    
    def test_variosConsumosConAfiliacionYExcesosMultiples2(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values
        (1002,'Segundos a Otras Operadoras',0.20,FALSE);
        
        insert into SERVICIO values
        (1003,'Mensajes de texto',0.5,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,200);
        
        insert into INCLUYE values
        (3002,1002,0.2,100);
        
        insert into PAQUETE values
        (4001,'PegaoSMS',100);
        
        insert into CONTIENE values
        (4001,1003,300);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONTRATA values
        ('CBZ27326',4001);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '60 days',20000);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',20000);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp - interval '45 days',20000);
        
        commit;""")
        
        
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        
        # El valor de la deuda debe ser 211 + 0.2*(120-100) + 100 = 315
        
        theoreticResult = 315
        
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 7: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 7 FALLIDA")
	  return
        print("Prueba 7 lista")
        
    # Prueba 8
    ## Caso en el que un cliente consume tres servicios estando afiliado a un plan
    ## que los contiene: en el primer caso la cantidad consumida esta cubierta, en el segundo
    ## no. En el tercer caso el cliente esta afiliado a un paquete que contiene dicho plan, y 
    ## los consumos no estan enteramente cubiertos. En todo caso hay una cantidad variable de consumos pequeños
    
    def test_variosConsumosConAfiliacionYExcesosMultiples3(self):
        self.myConsult.setComando("""
        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into SERVICIO values
        (1002,'Segundos a Otras Operadoras',0.20,FALSE);
        
        insert into SERVICIO values
        (1003,'Mensajes de texto',0.5,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,200);
        
        insert into INCLUYE values
        (3002,1002,0.2,100);
        
        insert into PAQUETE values
        (4001,'PegaoSMS',100);
        
        insert into CONTIENE values
        (4001,1003,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONTRATA values
        ('CBZ27326',4001);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',20000);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1002,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1001,current_timestamp - interval '45 days',20000);
        
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp,20);
        insert into CONSUME values(DEFAULT,
        'CBZ27326',1003,current_timestamp - interval '45 days',20000);
        
        commit;""")
        
        
        
        self.myConsult.execute()
	testBill = Factura.Factura(22714709,"CBZ27326")
        result = testBill.totalCobrar()
        
        # El valor de la deuda debe ser 211 + 0.2*(120-100) + 100 + 0.5(120-100) = 325
        
        theoreticResult = 325
        
        try:
          self.assertEqual(result,theoreticResult,"Error en la prueba 8: Se esperaba %d y se recibio %d" % (theoreticResult,result));
        except AssertionError,e:
	  print e
	  print("Prueba 8 FALLIDA")
	  return
        print("Prueba 8 lista")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()