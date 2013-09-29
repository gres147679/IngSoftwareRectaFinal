import psycopg2
import sys
import psycopg2.extras
import validacion
import database
import dbparams 
 
# Funcion para pedir los datos del producto por consola    
def pedirProducto():
    print "Favor rellenar los datos pedidos a continuacion: \n"
    #Se piden los datos y se validan
    numserie = nuevaSerie()
    nombre = validacion.validarInput('Nombre del producto: ')
    rif = validarRIF()
    cedula = validarCedula()
    return(numserie,nombre,rif,cedula)
    
# Validamos la sere  de un producto introducido por consola
# La serie debe pertenece a un producto en la BD
def validarSerie():
    #Nombre del Producto
    while True:
        numSerie = validacion.validarInput('Numero de Serie: ')
        if (existeProducto(numSerie)):
            break
        else:
            print "\n Error: No existe un producto con dicho numero de serie."
            
    return numSerie

# Validamos la sere  de un producto introducido por consola
# La serie no debe pertenece a un producto en la BD
def nuevaSerie():
    #Nombre del Producto
    while True:
        numSerie = validacion.validarInput('Numero de Serie: ')
        if (not existeProducto(numSerie)):
            break
        else:
            print "\n Error: Ya existe un producto con dicho numero de serie."
            
    return numSerie

    
#Validamos el RIF  introducido por consola
def validarRIF():
    
    while True:
        x = int(validacion.validarNumero('RIF: '))
        if (existeEmpresa(x)):
            rif = str(x)
            break
        else:
            print "\n Error: La empresa no existe"
    return rif
    
#Validamos el numero de cedula introducido por consola
def validarCedula():
    #Cedula
    cedula = ''
    while True:
            x = int(validacion.validarNumero('cedula: '))
            if (existeCliente(x)):
                cedula = str(x)
                break
            else:
                print "\n Error: No existe un cliente con dicha cedula"
    return cedula
    
# Funcion que nos permite agregar nuevos productos a la base de datos
def nuevoProducto():
    producto = pedirProducto()
    conexiondb = database.operacion(
        'Se inserta el producto a la base de datos',
        'insert into producto values (\'%s\',\'%s\',\'%s\',\'%s\');' % producto,
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
    conexiondb.execute()
    if conexiondb.insercionRechazada:
        print 'No se ha podido insertar el producto'
    else:
        print "El producto se ha registrado exitosamente."     

    conexiondb.cerrarConexion()
    
# Funcion que elimina un producto de la base de datos.Recibe de parametro de entrada el numero de serie
# del producto a eliminar
def eliminarProducto(nserie):
    conexiondb =  database.operacion(
        'Eliminamos un producto',
        'delete from producto where numserie=\'%s\';' % nserie,
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
    conexiondb.execute()
    if conexiondb.insercionRechazada:
        print 'No se ha podido eliminar el producto'
    else:
        print "El producto se ha eliminado exitosamente."     

    conexiondb.cerrarConexion()
    
# Verifica la cantidad de productos agregados a la base de datos    
def cantidadProductos ():

    conexiondb = database.operacion(
    'Contamos la cantidad de Productos en la Base de Datos',
    'SELECT COUNT(*) FROM PRODUCTO;',
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
    return conexiondb.execute()[0][0]
    
# Funcion que nos permite saber si un producto existe en la base de datos
# Recibe de entrada el numero de serie del producto a buscar
def existeProducto(nserie):

    conexiondb = database.operacion(
    'Operacion que busca un producto en la base de datos',
    'SELECT COUNT(*) FROM PRODUCTO WHERE numserie=\'%s\';' % nserie,
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
    return (conexiondb.execute()[0][0] > 0)
    
# Funcion que nos devuelve el producto buscado.
# Recibe de entrada el numero de serie del producto en cuestion.
# En caso de no ser encontrado devuelve None
def obtenerProducto(nserie):
    producto = None
    if (cantidadProductos() == 0):
        print "\n Error: La base de datos esta vacia"
    else:
        if (existeProducto(nserie)):
            conexiondb = database.operacion(
                'Buscamos un cliente en la base de datos',
                'SELECT * from PRODUCTO WHERE numserie = \'%s\';' % nserie,
                dbparams.dbname,dbparams.dbuser,dbparams.dbpass
                )
            resultado = conexiondb.execute()
            for row in resultado:
                producto = 'Producto: ' + str(row['nombreprod'])
                producto += '\nNumero de Serie: ' + str(row['numserie'])
        else:
            print "El producto no existe"
    return producto
#
# Indica si un cliente se encuentra o no en la base de datos.
# 
def existeCliente(idCliente):
    conexiondb = database.operacion(
    'Operacion que busca un cliente en la DB',
    'select count(*) from cliente where cedula=\'%s\';'  % idCliente,
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
    return (conexiondb.execute()[0][0] > 0)
    
def existeEmpresa(rif):
    conexiondb = database.operacion(
    'Operacion que busca una empresa en la DB',
    'select count(*) from empresa where rif= %s ;'  % rif,
    dbparams.dbname,dbparams.dbuser,dbparams.dbpass
    )
    return (conexiondb.execute()[0][0] > 0)

#
# Lista todos los productos en la BD
#
def listarProductos():
    cant = cantidadProductos()
    if (cant == 0):
        print "No hay productos en la BD"
        return False
    else:
        conexiondb = database.operacion(
        'Operacion que lista todos los productos en la DB',
        '''select * from producto ''',
        dbparams.dbname,dbparams.dbuser,dbparams.dbpass
        )
        result = conexiondb.execute()
        
        for row in result:
            writeRow = '  Numero de serie: ' + row['numserie']
            writeRow+= ' | Nombre: ' + row['nombreprod'] 
            writeRow+= ' | RIF: ' + str(row['rif']) 
            writeRow+= ' | Cedula: ' + str(row['cedula'])
            
            print writeRow              
        
        return True  
    
      ##### MAIN #####
if __name__ == "__main__":
  print 'Esto no es un ejecutable. Es un modulo. MODULO!'
  listarProductos()
  nuevoProducto()
    # #eliminarProducto('p4321')
    # print cantidadProductos()
    
    # print existeProducto('p1223')
    # obtenerProducto('p123')
    
    #### END MAIN ####
