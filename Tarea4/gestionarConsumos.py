# -*- coding=utf-8 -*-
import psycopg2
import database
import dbparams
import datetime
from consumos import consumo,existeEquipo,existeServicio
import re

def buscarConsumosporServicio(idProducto,mesFacturacion,anioFacturacion):
    conexion = database.operacion("Buscamos la suma de todos los consumos por servicio",
                            """SELECT con.codserv, sum(con.cantidad) AS total FROM consume AS con 
                            WHERE con.numserie = \'%s\' AND 
                            to_char(con.fecha, 'MM YYYY') = \'%s\' GROUP BY (con.codserv)""" %
                            (idProducto, mesFacturacion+ " " + anioFacturacion),
                            dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
       
    return conexion.execute()  

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
  parseado = False
  while not parseado:
    try:
      trozos = fecha.strip().split('/')
      fecha = datetime.date(int(trozos[2]),int(trozos[1]),int(trozos[0]))
      parseado = True
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

