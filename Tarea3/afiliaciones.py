##***************************************************************************
##************************MODULO DE AFILIACIONES ****************************
##***************************************************************************

##*** Librerias a utilizar **************************************************

import psycopg2
import psycopg2.extras
import unittest

##*** Clase de Afiliaciones *************************************************

class Afiliaciones:
    ## Constructor de la clase
    def __init__ (self,serie_producto,cod_plan):
        self.producto = serie_producto
        self.plan = cod_plan
        
        ## Atributo que conecta a la base de datos
        try:
            self.conectar = psycopg2.connect ("dbname='tarea' user='jljb1990' password=''")
            self.cur = self.conectar.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception, e:
            print "Error conectando con la base de datos. ", e

##*** Metodos de la clase ***************************************************
    
    ## Devuelve algun producto
    def getProducto (self):
        return self.producto
        
    ## Devuelve algun codigo de plan
    def getPlan (self):
        return self.plan
    
    ## Termina la conexion con la base de datos
    def cerrarConexion(self):
        self.cur.close()
        self.conectar.close()
        
    ## Guarda los cambios realizados en la base de datos
    def guardarCambios(self):
        self.conectar.commit()
        
    ## Pide al usuario que determine el tipo de plan al que desea afiliar su 
    ## producto
    def tipoPlan (self):
        tipoplan = 0
        while (tipoplan != '1' and tipoplan != '2'):
            tipoplan = raw_input("""Indique si el plan es 'infinito' o 'paquete'
            Ingrese 1 si es infinito
            Ingrese 2 si es un paquete
            """)
            
        if tipoplan == '1':
            plan = 'infinito'
        else:
            plan = 'paquete' 
            
        return plan
                    
    ## 
    ## Verifica si un plan esta presente en la base de datos. Si existe lo devuelve,
    ## si no, muestra un mensaje de error
    def buscarPlan(self):
        self.cur.execute("SELECT tipo FROM PLAN WHERE codplan = %(codplan)s", 
        {'codplan' : self.plan})
        
        ## Si el plan no se consigue
        if self.cur.rowcount == 0:
            raise Exception("El plan introducido no existe en la base de datos.")
        
        ## Si se consigue el plan, se devuelve 
        return self.cur.fetchone()[0]
    
    ## Crea la afiliacion de un producto con un plan
    def CrearAfiliacion (self):
        try:            
            tipoplan = self.buscarPlan()

            self.cur.execute("SELECT * FROM PRODUCTO WHERE numserie = %(numserie)s", 
            {'numserie' : self.producto})
            
            ## Si el producto no existe en la base de datos.
            if self.cur.rowcount == 0:
                raise Exception("El producto introducido no existe en la base de datos.")
            
            self.cur.execute("SELECT * FROM ACTIVA WHERE numserie = %(numserie)s", 
            {'numserie' : self.producto})
            
            ## Si el producto ya tiene plan
            if self.cur.rowcount != 0:
                raise Exception("El producto introducido ya tiene un plan asociado.")
            
            self.cur.execute("SELECT * FROM AFILIA WHERE numserie = %(numserie)s", 
            {'numserie' : self.producto})
            
            if self.cur.rowcount != 0:
                raise Exception("El producto introducido ya tiene un plan asociado.")

            ## Si el plan es prepago
            if tipoplan == 'prepago':
                self.cur.execute("""INSERT INTO ACTIVA VALUES (%s, %s, %s)""", 
                (self.producto, self.plan, 0))
                
            ## Si el plan es postpago
            else:
                plan = self.tipoPlan()
                self.cur.execute("""INSERT INTO AFILIA VALUES (%s, %s, %s)""",
                (self.producto, self.plan, plan))
                
                
            ## Guardamos los cambios y cerramos la base de datos
            self.guardarCambios()
            self.cerrarConexion()
            
        ## Capturamos los posibles errores.
        except Exception, e:
            print 'Se ha conseguido un error.', e
            
    ## Crea una afiliacion entre un producto y un paquete de servicios
    def CrearContratacion (self):
        try:
            ## Verificamos si el paquete existe en la base de datos
            self.cur.execute("SELECT codpaq FROM PAQUETE WHERE codpaq = %(codpaq)s", {'codpaq' : self.plan})
            if self.cur.rowcount == 0:
                raise Exception("\nEl paquete introducido no existe en la base de datos")
            
            ## Verificamos si la contratacion ya existe en la base de datos
            self.cur.execute("""SELECT codpaq, numserie FROM CONTRATA WHERE codpaq = %(codpaq)s AND 
                                numserie = %(numserie)s""", {'codpaq' : self.plan, 'numserie' : self.producto})
            if self.cur.rowcount != 0:
                raise Exception("\nLa afiliacion entre dichos producto y paquete ya existe")
            
            self.cur.execute("INSERT INTO CONTRATA VALUES (%s, %s)", (self.producto, self.plan))
            print '\nSe ha creado la afiliacion del producto con el paquete deseado'
            
            ## Guardamos los cambios y cerramos la base de datos
            self.guardarCambios()
            self.cerrarConexion()
            
        ## Capturamos los posibles errores.
        except Exception, e:
            print 'Se ha conseguido un error.', e
            
    ## Elimina la afiliacion entre un producto y un plan en especifico
    def DesafiliarProducto (self):
        try:
            self.cur.execute("""SELECT numserie, codplan FROM ACTIVA WHERE codplan = %(codplan)s AND
                        numserie = %(numserie)s""", 
            {'codplan' : self.plan, 'numserie' : self.producto})

            # Si no se encuntra la afiliacion entre los planes prepago
            if self.cur.rowcount == 0:
                self.cur.execute("""SELECT numserie FROM AFILIA WHERE codplan = %(codplan)s AND
                        numserie = %(numserie)s""", 
            {'codplan' : self.plan, 'numserie' : self.producto})
                
                # Si no se encuentra la afiliacion entre los planes postpago
                if self.cur.rowcount == 0:
                    raise Exception("\nEl producto ingresado no se encuentra afiliado con el plan mencionado")
                
                # Si se encuentra la afiliacion entre los planes postpago, eliminamos dicha afiliacion
                else:
                    
                    self.cur.execute("DELETE FROM AFILIA WHERE codplan = %(codplan)s AND numserie = %(numserie)s",
                                {'codplan' : self.plan, 'numserie' : self.producto})
                    print '\nSe ha eliminado la afiliacion exitosamente'
            
            # Si se encuentra la afiliacion entre los planes prepago, eliminamos dicha afiliacion
            else:
                self.cur.execute("DELETE FROM ACTIVA WHERE codplan = %(codplan)s AND numserie = %(numserie)s",
                {'codplan' : self.plan, 'numserie' : self.producto})
                print '\nSe ha eliminado la afiliacion exitosamente'
                
            ## Guardamos los cambios y cerramos la base de datos
            self.guardarCambios()
            self.cerrarConexion()
                    
        ## Capturamos los posibles errores.
        except Exception, e:
            print 'Se ha conseguido un error.', e
            
    ## Informa a que plan o planes esta afiliado un producto
    def ConsultarPlanes (self):
        try:
            self.cur.execute("SELECT nombrepaq FROM CONTRATA NATURAL JOIN PAQUETE WHERE numserie = %(numserie)s", 
            {'numserie' : self.producto})
            
            nombreplan = self.cur.fetchall()
            for i in nombreplan:
                print 'El producto esta asociado al paquete ' + i[0]
                
            if self.cur.rowcount == 0:
                print 'El producto no esta afiliado a ningun paquete'
            
            self.cur.execute("SELECT nombreplan FROM ACTIVA NATURAL JOIN PLAN WHERE numserie = %(numserie)s", 
            {'numserie' : self.producto})
            
            nombreplan = self.cur.fetchall()
            for i in nombreplan:
                print 'El producto esta asociado al plan ' + i[0]
                
            if self.cur.rowcount == 0:
                
                self.cur.execute("SELECT nombreplan FROM AFILIA NATURAL JOIN PLAN WHERE numserie = %(numserie)s", 
                {'numserie' : self.producto}) 
                
                nombreplan = self.cur.fetchall()
                for i in nombreplan:
                    print 'El producto esta asociado al plan ' + i[0]
                    
                if self.cur.rowcount == 0:
                    print 'El producto no tiene plan asociado'
                
            self.guardarCambios()
            self.cerrarConexion()
            
        # Capturamos los posibles errores.
        except Exception, e:
            print 'Se ha conseguido un error.', e
                
    ## Elimina la afiliacion entre un producto y un paquete de servicios.
    def desafiliarContratacion(self):
        try:
            self.cur.execute("""SELECT numserie, codpaq FROM CONTRATA WHERE codpaq = %(codplan)s AND
            numserie = %(numserie)s""", 
            {'codplan' : self.plan, 'numserie' : self.producto})
            
            if self.cur.rowcount == 0:
                print 'El producto no esta afiliado al paquete introducido'
            else:
                self.cur.execute("DELETE FROM CONTRATA WHERE codpaq = %(codplan)s AND numserie = %(numserie)s",
                {'codplan' : self.plan, 'numserie' : self.producto})
                print 'Se ha eliminado la contratacion exitosamente'
            
            self.guardarCambios()
            self.cerrarConexion()
        except Exception, e:
            print 'Se ha conseguido un error. ', e

## Main de pruebas
#if __name__ == '__main__':
#    Afiliacion = Afiliaciones('a1',1)
#    Afiliacion.CrearAfiliacion()
#    Afiliacion = Afiliaciones('a1',10)
#    Afiliacion.CrearContratacion()
#    Afiliacion = Afiliaciones('a1',10)
#    Afiliacion.CrearContratacion()
#    Afiliacion = Afiliaciones('a1',1)
#    Afiliacion.DesafiliarProducto()
#    Afiliacion = Afiliaciones('a1',1)
#    Afiliacion.ConsultarPlanes()
#    Afiliacion = Afiliaciones('a1',10)
#    Afiliacion.desafiliarContratacion()    
