# -*- coding: utf-8 -*-
import database as db
import Afiliaciones
import psycopg2
import psycopg2.extras
import unittest
import cliente as cl
import moduloCliente as mc
import consumos
import productos as pr
import validacion
import dbparams
import datetime
from metodoFacturacion import metodoFacturacion

# Implementación metodoFacturaciónPostpafgo
# Implementa la interfaz para la estrategia que usa la factura para calcular
# el total del monto y la presentación final de la factura. Esta implementación
# factura los equipos postpago

class metodoFacturacionPostpago(metodoFacturacion):
  
  # mes y año de facturación
  def __init__(self,producto,idProducto,cliente,mes,anio,obs):
    # El orden es: producto,idProducto,cliente,mes,anio,obs
    
    self.producto = producto
    self.idProducto = idProducto
    self.cliente = cliente
    self.mesFacturacion = anio
    self.anioFacturacion = mes
    self.observaciones = obs
    
    self.listaCobrar = {}
    self.nombrePlan = ''
    self.totalPlan = 0
    self.totalPaquete = 0
    self.montoTotalCobrar = self.facturar()
    
  
    
  def facturar(self):
        
        resultado = Afiliaciones.ConsultarPlanesPostpago(self.idProducto)
   
        codplan = resultado[0][0]

        #Buscamos la renta del plan que se va a cobrar al producto.      
        conexion = db.operacion("Buscamos la renta del plan que se va a cobrar al producto",
                                """SELECT renta_basica, nombreplan FROM plan WHERE codplan = %s""" % codplan,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        resultado = conexion.execute()
        renta = int(resultado[0][0])
        
        self.nombrePlan = str(resultado[0][1])
        self.totalPlan = renta
        
        #Buscamos la suma de todos los consumos por servicio hechos por el producto en el año y mes introducidos por el usuario.
        #Lo guardamos en un diccionario donde la clave es el codigo del servicio.
        listaConsumos = consumos.facturacion(self.idProducto,self.mesFacturacion,self.anioFacturacion)
        resultado = listaConsumos.buscarConsumosporServicio()
        
        totalConsumido = {}
        for row in resultado:
                totalConsumido[row[0]] = int(row[1])
        
        #Buscamos los servicios ofrecidos por el plan y la cantidad y tarifa ofrecidos por este. 
        #El resultado se guarda en un diccionario donde la clave es el codigo del servicio.
        
        conexion = db.operacion("Buscamos los servicios ofrecidos por el plan, ademas de la cantidad y tarifa ofrecidos por este",
                                """SELECT inc.codserv, inc.cantidad, inc.tarifa, serv.nombreserv FROM incluye AS inc, servicio AS serv 
                                WHERE inc.codplan =  %s and serv.codserv = inc.codserv;""" % codplan,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        
        resultado = conexion.execute()       
         
        totalPlan = {}
        
        for row in resultado:
            totalPlan[row[0]] = [row[1], row[2], row[3]]
                
        #Se busca si el producto este asociado a algun paquete. De estarlo, las cantidades de servicio ofrecidas se agregan al
        #diccionario de los servicios ofrecidos por el plan.
        
        resultado = Afiliaciones.ConsultarPaquetes(self.idProducto)

        for row in resultado:
            codserv = row[0]
            if totalPlan.has_key(codserv):
                totalPlan[codserv][0] = totalPlan[codserv][0] + int(row[1])
            else:
                totalPlan[codserv] = [int(row[1]), row[2], row[3]]
        
        #Se busca el costo total de todos los paquetes a los que esta suscrito el producto. El resultado se almacena
        #en el total a cobrar.
        
        conexion = db.operacion("Costo total de todos los paquetes",
                                """SELECT sum(precio) FROM contrata NATURAL JOIN paquete 
                                WHERE numserie = \'%s\' GROUP BY(contrata.numserie)""" % self.idProducto,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        
        resultado = conexion.execute()
        if len(resultado) == 0:
            total = 0
        else:
            total = int(resultado[0][0])
        
        self.totalPaquete = total
        #Se verifica la suma de los consumos por servicio del producto, si excede el valor ofrecido por el plan/paquete
        #entonces se cobra lo indicado por el plan. En caso que el serivicio sea ofrecido por un paquete, se cobra por exceso
        #el costo del servicio.
        
        
        for con in totalConsumido.keys():
            consumido = totalConsumido[con]
            limite = totalPlan[con][0]
            self.listaCobrar[con] = [totalPlan[con][2], consumido, limite, 0]
            if consumido > limite:
                exceso = (consumido - limite) * totalPlan[con][1]
                total = total + exceso
                self.listaCobrar[con][3] = exceso
        
        
        return total + renta
    
  def __str__(self):
      now = datetime.datetime.now()
      string = '\n=========================================================================================================='
      string += '\n{0:50}FACTURA'.format(' ') + '{0:20}Fecha de emisión: '.format(' ') + str(now.strftime("%d-%m-%Y")) + '\n' + str(self.cliente)
      string += '\n' + str(self.producto)
      string += '\n\n\n{4:40}SERVICIOS CONSUMIDOS (%s-%s)\n\n{0:30} | {1:20} | {2:20} | {3:20}'.format('SERVICIO', 'TOTAL CONSUMIDO', 'L�?MITE DEL PLAN', 'MONTO A COBRAR POR EXCESO',' ') % (self.mesFacturacion, self.anioFacturacion)
      string += '\n----------------------------------------------------------------------------------------------------------'
      for con in self.listaCobrar.keys():
	  string += '\n{0:30} | {1:20} | {2:20} | {3:20}'.format \
		      (self.listaCobrar[con][0], str(self.listaCobrar[con][1]), str(self.listaCobrar[con][2]), str(self.listaCobrar[con][3]))
      string += '\n----------------------------------------------------------------------------------------------------------'
      string += '\n\nMonto a cobrar por el plan ' + self.nombrePlan + ': ' + str(self.totalPlan)
      string += '\nMonto a cobrar por los paquetes afiliados: ' + str(self.totalPaquete)
      string += '\n\nTOTAL: ' + str(self.montoTotalCobrar)
      string += '\n==========================================================================================================\n'
      string += 'Observaciones: ' + str(self.observaciones) + '\n'
      return string
