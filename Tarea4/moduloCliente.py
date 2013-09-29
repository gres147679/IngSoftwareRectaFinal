# Clase moduloCliente.py
#!/usr/bin/env python
#!/usr/bin/py
# -*- coding: utf-8 -*-

import sys
import cliente
import validacion
import database
import dbparams

#Librerias de conexion con postgresql
import psycopg2
import psycopg2.extras
            
#
# Cuenta cuantos clientes hay en la DB
#
def numeroClientes():
    conexiondb = database.operacion('Operacion que cuenta el numero de clientes en la DB',
    'select count(*) from cliente;',
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
    
    return conexiondb.execute()[0][0]

#
# Indica si un cliente se encuentra o no en la base de datos.
#     
def existeCliente(idCliente):
    conexiondb = database.operacion(
    'Operacion que busca un equipo en la DB',
    'select count(*) from cliente where cedula=\'%s\';'  % idCliente,
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
    return (conexiondb.execute()[0][0] > 0)
  
#
# Obtiene y valida los datos de un cliente insertados por consola
#
def datosCliente():
    print("Introduzca los siguientes datos: ")
    
    # Verifica que la cedula no se encuentre en el sistema        
    while True:

        x = int(validacion.validarNumero('    Cedula: '))        
        if (existeCliente(x)):
            print "\nERROR: La cedula introducida ya se encuentra en el sistema. Intente de nuevo."
        else:   
            ci = str(x)
            break
    
    # Verifica que la entrada del nombre sea valida.
    nombre = validacion.validarInput('    Nombre: ')
    
    # Verifica que la entrada de la direccion sea valida.
    direccion = validacion.validarInput('    Direccion: ')
    return (ci,nombre,direccion)

#
# Se registra un cliente.
#
def registroCliente():
            
    #Inserta el cliente introducido
    datos = datosCliente()
    
    conexiondb = database.operacion(
    'Operacion que inserta un cliente en la DB',
    'insert into cliente values (%s,\'%s\',\'%s\');' % datos,
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
   
    conexiondb.execute()
    if conexiondb.insercionRechazada:
        print 'No se ha podido insertar el cliente'
    else:
        print "El cliente se ha registrado exitosamente."     

    conexiondb.cerrarConexion()

#
# Se consulta un cliente
#     
def consultaClientes():
    flag = True
    
    #Se verifica que la base de datos no este vacia
    if (numeroClientes() == 0):
        print "ERROR: No se puede consultar al cliente. La base de datos esta vacia.\n"
    else:
        idCliente = validacion.validarNumero('Introduzca la cedula del cliente: ')
        #Se verifica que la cedula introducida exista
        while flag:    
            if (existeCliente(idCliente)):
                cl = busquedaCliente(idCliente)
                print str(cl)
                flag = False
            else:
                print "\nERROR: La cedula introducida no se encuentra en el sistema. Intente de nuevo.\n"
                idCliente = validacion.validarNumero('Introduzca la cedula del cliente: ')
  
 
#
# Se busca un cliente, y retorna sus datos en la clase Cliente.
# Si el cliente no se encuentra en la base de datos, retorna None.
#     
def busquedaCliente(idCliente):
    
    cl = None
    #Se verifica que la base de datos no este vacia
    if (numeroClientes() == 0):
        print "ERROR: No se puede buscar al cliente. La base de datos esta vacia."
    else:
        if (existeCliente(idCliente)):
            conexiondb = database.operacion(
            'Operacion que busca un cliente en la DB',
            '''SELECT cedula, nombrecl, direccion FROM CLIENTE 
            WHERE cedula = \'%s\';''' % idCliente,
            dbparams.dbname,dbparams.dbuser,dbparams.dbpass
            )
            result = conexiondb.execute()
            for row in result:                     
                cl = cliente.cliente(row[0], row[1], row[2])

    return cl
 
#
# Indica si el cliente idCliente posee un producto serieProd
#     
def poseeprodCliente(idCliente,serieProd):
    if (existeCliente(idCliente)):
        conexiondb = database.operacion(
        'Operacion que busca un cliente en la DB',
        '''select count(*) from producto where cedula = \'%s\'
           and numserie = \'%s\';''' % (idCliente,serieProd),
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass
        )
        return (conexiondb.execute()[0][0] > 0)
    else:
        return False
 
          
#
# Se busca un cliente, y retorna la cantidad de productos que haya comprado.
# Si el cliente no existe, retorna -1.
#     
def cantprodCliente(idCliente):
    if (existeCliente(idCliente)):
        conexiondb = database.operacion(
        'Operacion que busca un cliente en la DB',
        '''select count(*) from producto where cedula = \'%s\';''' % idCliente,
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass
        )
        return conexiondb.execute()[0][0]
    else:
        return -1
#
# Lista los productos de un cliente
# Retorna true si el cliente posee productos en la BD
#
def listarProductos(idCliente):
    cant = cantprodCliente(idCliente)
    if (cant == -1):
        print "El cliente no se encuentra en la BD."
        return False
    elif (cant == 0):
        print "El cliente no posee productos en la BD."
        return False
    else:
        conexiondb = database.operacion(
        'Operacion que lista los productos de un cliente en la DB',
        '''select numserie,nombreprod,rif from producto where cedula = \'%s\';''' % idCliente,
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass
        )
        result = conexiondb.execute()
        
        print "El cliente cuya cedula es %s posee los siguientes productos: " % idCliente
        for row in result:
            writeRow = '  Numero de serie: ' + row['numserie']
            writeRow+= ' | Nombre: ' + row['nombreprod'] 
            writeRow+= ' | RIF: ' + str(row['rif']) 
            
            print writeRow              
        
        return True

def listarClientes():
    cant = numeroClientes()
    if (cant == 0):
        print "No hay clientes en la BD"
        return False
    else:
        conexiondb = database.operacion(
        'Operacion que lista todos los clientes en la DB',
        '''select * from cliente ''',
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass
        )
        result = conexiondb.execute()
        
        for row in result:
            writeRow = '  Cedula: ' + str(row['cedula'])
            writeRow+= ' | Nombre: ' + row['nombrecl'] 
            writeRow+= ' | Direccion: ' + row['direccion'] 
            
            print writeRow              
        
        return True  

#MAIN DE PRUEBA        
if __name__== "__main__":
    
    cl = busquedaCliente(123)
    listarProductos(22714709)
    listarClientes()
    print poseeprodCliente(1234,123)
    
    
       
#     print numeroClientes()
#     print cantprodCliente(123)
#      consultaClientes()
#      registroCliente()
#      
#     cl = busquedaCliente(124)
#     if cl!= None:
#         print str(cl)
#     else:
#         print "No existe"   

     
    
#END moduloCliente.py