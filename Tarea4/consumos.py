#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Para este módulo se han implementado dos clases:
# -La clase consumo: Describe un consumo que será agregado a la base de datos
#
# -La clase facturacion: Describe un pedido de lista de consumos que se hará en la
#  base de datos. Considerando los requerimientos de Innova, se piden consumos
#  para un mes de facturación en particular
#

import psycopg2
import database
import dbparams
import datetime
import re

"""
Define un consumo a agregar en la base de datos.
"""
class consumo:
  
  
  """
  Construye un nuevo consumo, y lo agrega a la base de datos.
  Debe existir un plan o paquete que incluya el servicio que se 
  consume
  
  Parametros:
    -El número de serie del producto que consume
    -La fecha del consumo. En formato de string DD/MM/AAAA
    -El código del servicio que se consume
    -La cantidad de unidades consumidas
  """
  def __init__(self,numserie,fecha,codservicio,cantidad):
    self.numserie = numserie
    self.fecha = fecha
    self.codservicio = codservicio
    self.cantidad = cantidad
  
  
  """
  Representa el consumo como un string
  """
  def __str__(self):
    return '''Código del servicio: %s | Fecha del Consumo: %s | Cantidad: %s''' % (self.codservicio,self.fecha,str(self.cantidad))
  """
  Inserta el consumo en la DB
  """
  def sync(self):
    # Conexión con la base de datos
    self.conexiondb = database.operacion(
      'Operacion que inserta un consumo en la DB',
      'insert into consume values (DEFAULT,\'%s\',%s,\'%s\',%s);' 
      % (self.numserie,self.codservicio,self.fecha,self.cantidad),
      dbparams.dbname,dbparams.dbuser,dbparams.dbpass
      )
    
    self.conexiondb.execute()
    if self.conexiondb.insercionRechazada:
      print 'No se ha podido insertar el consumo'
    self.conexiondb.cerrarConexion()
    #import consumos;consumos.consumo("CBZ27326",1001,"31/05/2013",50)


"""
Verifica si un equipo esta registrado en la DB, dado su código

Parametros:
  -Código del equipo
"""
def existeEquipo(numserie):
  conexiondb = database.operacion(
  'Operacion que busca un equipo en la DB',
  'select count(numserie) from producto where numserie=\'%s\';'  % numserie,
  dbparams.dbname,dbparams.dbuser,dbparams.dbpass
  )
  return conexiondb.execute()[0][0]


"""
Verifica si un servicio esta registrado en la DB, dado su código

Parametros:
  -Código del servicio 
"""
def existeServicio(codserv):
  conexiondb = database.operacion(
  'Operacion que busca un servicio en la DB',
  'select count(codserv) from servicio where codserv=\'%s\';'  % codserv,
  dbparams.dbname,dbparams.dbuser,dbparams.dbpass
  )
  return conexiondb.execute()[0][0]


"""
Crea un consumo en la DB de forma interactiva
 
"""
def crearConsumoInteractivo():
  print 'Se le solicitará la información del consumo'
  print 'Inserte el código del equipo'
  numserie = raw_input('-->')
  while not existeEquipo(numserie):
    print 'El código que ha insertado no corresponde con ningún equipo. Reintente'
    print 'Inserte el código del equipo'
    numserie = raw_input('-->')
    
  print 'Inserte el código del servicio consumido'
  codserv = raw_input('-->')
  while not existeServicio(codserv):
    print 'El código que ha insertado no corresponde con ningún servicio. Reintente'
    print 'Inserte el código del servicio consumido'
    codserv = raw_input('-->')
    
  print 'Inserte la fecha del consumo, en formato DD/MM/AAAA'
  fecha = raw_input('-->')
  while not re.match('\d\d/\d\d/\d\d\d\d',fecha.strip()):
    print 'Ha introducido una fecha inválida. Reintente.'
    print 'Inserte la fecha del consumo, en formato DD/MM/AAAA'
    fecha = raw_input('-->')
  try:
    trozos = fecha.strip().split('/')
    fecha = datetime.date(int(trozos[2]),int(trozos[1]),int(trozos[0]))
  except ValueError:
    print 'Ha introducido una fecha inválida. Reintente.'
    print 'Inserte la fecha del consumo, en formato DD/MM/AAAA'
    fecha = raw_input('-->')
    
  print 'Inserte la cantidad de unidades consumidas'
  cantidad = int(raw_input('-->'))
  while cantidad <= 0:
    print 'Ha introducido una cantidad inválida. Reintente.'
    print 'Inserte la cantidad de unidades consumidas'
    cantidad = int(raw_input('-->'))
  
  miConsumo = consumo(numserie,fecha.strftime('%d/%m/%Y'),codserv,cantidad)
  miConsumo.sync()
  return miConsumo


"""
Define una lista de todos los consumos de un mismo producto

Atributos:
  - Número de serie del producto
  - Inicio de la facturación
"""
def consumosProducto():
  

    print 'Inserte el código del equipo'
    numserie = raw_input('-->')
    while not existeEquipo(numserie):
        print 'El código que ha insertado no corresponde con ningún equipo. Reintente'
        print 'Inserte el código del equipo'
        numserie = raw_input('-->')  
      
    
    # Conexión con la base de datos
    conexiondb = database.operacion(
      'Operacion que lista los consumos para un equipo en el rango dado',
      '''select * from consume where numserie = \'%s\' 
        order by fecha asc;''' % (numserie), 
      dbparams.dbname,dbparams.dbuser,dbparams.dbpass
      )
    result = conexiondb.execute()
    
    
    
    # Para cada tupla consumo, crea un consumo y agregalo a mi lista
    for i in result:
        print consumo(numserie,i[3].strftime('%d/%m/%Y'),i[2],i[4])
        
    if len(result) == 0:
        print "Este producto no posee ningun consumo."    
        
    conexiondb.cerrarConexion()

"""
Define una lista de consumos de un mismo producto

Atributos:
  - Número de serie del producto
  - Inicio de la facturación
  - Fín de la facturacion
  - Lista de consumos
"""
class facturacion:
  
  """
  Crea una facturacion
  Parámetros:
    -Número de serie del producto
    -Inicio de la facturación: En formato DD/MM/YYYY
    -Fín de la facturacion: En formato DD/MM/YYYY
  """
  def __init__(self,numserie,inicio,fin):
    self.numSerieProducto = numserie
    self.inicioFacturacion = inicio
    self.finFacturacion = fin
    self.listaConsumos = []
    
    # Conexión con la base de datos
    self.conexiondb = database.operacion(
      'Operacion que lista los consumos para un equipo en el rango dado',
      '''select * from consume where numserie = \'%s\' and 
      fecha >= to_date(\'%s\','DD/MM/YYYY') and 
      fecha <= to_date(\'%s\','DD/MM/YYYY') order by fecha asc;''' 
      % (self.numSerieProducto,self.inicioFacturacion,self.finFacturacion),
      dbparams.dbname,dbparams.dbuser,dbparams.dbpass
      )
    result = self.conexiondb.execute()
    
    # Para cada tupla consumo, crea un consumo y agregalo a mi lista
    for i in result:
      self.listaConsumos.append(
	consumo(self.numSerieProducto,i[3].strftime('%d/%m/%Y'),i[2],i[4])
      )
    self.conexiondb.cerrarConexion()
  
  """
  Itera sobre la facturacion, iterando sobre la lista de consumos
  """
  def __iter__(self):
    return self.listaConsumos.__iter__()
  
  """
  Representación en string de la facturacion.
  Se representa como la concatenación de los strings de todos los consumos
  """
  def __str__(self):
    myString = ""
    for i in self:
      myString += str(i) + '\n'
    return myString[:len(myString)-1]
    
    
  def buscarConsumosporServicio(self):
    conexion = database.operacion("Buscamos la suma de todos los consumos por servicio",
                            """SELECT con.codserv, sum(con.cantidad) AS total FROM consume AS con 
                            WHERE con.numserie = \'%s\' AND 
                            to_char(con.fecha, 'MM YYYY') = \'%s\' GROUP BY (con.codserv)""" %
                            (self.numSerieProducto, self.inicioFacturacion + " " + self.finFacturacion),
                            dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
       
    return conexion.execute()  
    
    
if __name__ == '__main__':
  #a = facturacion('CBZ27326','30/04/2000','30/04/2015')
  #print a
  print 'Esto no es un ejecutable. Es un módulo. MÓDULO!'
  