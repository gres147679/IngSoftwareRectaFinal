#!/usr/bin/python
# -*- coding: utf-8 -*-
# Modulo menu.py

import gestionarFactura
import sys
import validacion
import moduloCliente
import productos
import afiliaciones
import gestionarConsumos
import serviciosadicionales


def main():
    print("BIENVENIDOS")
   
    #Menu de las consultas
    flag = True   

    while flag:
        print "\n---Menu---"
        print "\nElija el modulo de su preferencia: "
        print "   1.- Cliente."
        print "   2.- Producto."
        print "   3.- Afiliaciones."
        print "   4.- Consumos."
        print "   5.- Generacion de facturas."
        print "   6.- Salir"
        
        op = int(validacion.validarNumero('Opcion: '))
        
        ## Opcion de Cliente
        if op == 1:
            
            flag1 = True
            while flag1:
                print "\nMODULO CLIENTE \n"                    
                print "   1.- Registrar un cliente."
                print "   2.- Consultar un cliente."
                print "   3.- Regresar al menu anterior."
        
                op1 = int(validacion.validarNumero('Opcion: '))
                if op1 == 1:
                    print "\n1.- Registrar un cliente."
                    moduloCliente.registroCliente()
                elif op1 == 2:     
                    print "\n2.- Consultar un cliente."
                    
                    print "\nMostrando todos los clientes: "
                    moduloCliente.listarClientes()
                    
                    moduloCliente.consultaClientes()         
                elif op1 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag1 = False
                elif (op1 > 3 or op1 <= 0):
                    print "\nERROR: La opcion no es valida."
                    
        ## Opcion de Producto            
        elif op == 2:     
            flag2 = True
            while flag2:
                print "\nMODULO PRODUCTO\n"                    
                print "   1.- Registrar un producto."
                print "   2.- Consultar un producto."
                print "   3.- Regresar al menu anterior."
        
                op2 = int(validacion.validarNumero('Opcion: '))
                if op2 == 1:
                    print "\n1.- Registrar un producto."
                    productos.nuevoProducto()
                elif op2 == 2:     
                    print "\n2.- Consultar un producto."
                    serie = productos.validarSerie()                    
                    print str(productos.obtenerProducto(serie))
                elif op2 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag2 = False
                elif (op2 > 3 or op2 <= 0):
                    print "\nERROR: La opcion no es valida."
                    
        ## Opcion de Afiliaciones            
        elif op == 3:    
            flag3 = True

            while flag3:
                print "\nMODULO AFILIACIONES\n"                   
                print "   1.- Afiliar un producto."
                print "   2.- Desafiliar un producto."
                print "   3.- Consultar planes de un producto."
                print "   4.- Regresar al menu anterior."     
                           
                op3 = int(validacion.validarNumero('Opcion: '))
                
                print "\nMostrando todos los productos disponibles: "
                productos.listarProductos()

                ## Opcion de Afiliacion
                if op3 == 1:
                    producto31 = productos.validarSerie()   
                    flag31 = True                                       
                    
                    while flag31: 
                        print "\n1.- Afiliar un producto a un :"                   
                        print "   1.- Plan."
                        print "   2.- Paquete de Servicios."
                        print "   3.- Regresar."
                        
                        op31 = int(validacion.validarNumero('Opcion: '))
                        
                        ## Opcion para afiliar un plan
                        if op31 == 1:                            
                            print "\n1.- Plan."
                             
                            if afiliaciones.impPlanes():
                                print "\nMostrando todos los planes disponibles: "                                
                                cod_plan = int(validacion.validarNumero('Introduzca el codigo del plan: '))
                                Afiliacion = afiliaciones.Afiliaciones(producto31,cod_plan)                            
                                Afiliacion.CrearAfiliacion()
                            flag31 = False
                            
                        ## Opcion para afiliar un paquete de servicios
                        elif op31 == 2:     
                            print "\n2.- Paquete de Servicios."
                            
                            #Verifica que el producto tenga asociado un plan
                            if productos.productoTienePlan(producto31):
                                continua = True
                                
                                #Verifica que pueda contratar algun servicio
                                numPaquetes = afiliaciones.numPaquetesAContratar(producto31)
                                p = serviciosadicionales.Producto(producto31);
                                
                                while ((numPaquetes > 0) and (continua)): 
                                                                    
                                    #Muestra los paquetes que el producto puede contratar
                                    print "\nMostrando todos los paquetes de servicios disponibles: "
                                    afiliaciones.paquetesAContratar(producto31)
                                    
                                         
                                    #Elige uno de los paquetes 
                                    while True: 
                                        cod_ser = int(validacion.validarNumero('\nIntroduzca el codigo del paquete de servicio: '))
                                        #Contrata el paquete
                                        if (not afiliaciones.puedeContratar(p.get_id(), cod_ser)):
                                            print "\nERROR: La opcion no es valida."
                                            continue     
                                        elif cod_ser == 4001:
                                            p = serviciosadicionales.MensajesDeTexto(p)
                                            break
                                        elif cod_ser == 4002:
                                            p = serviciosadicionales.SegundosMOCEL(p)
                                            break
                                        elif cod_ser == 4003:
                                            p = serviciosadicionales.SegundosOtrasOperadoras(p)
                                            break
                                        elif cod_ser == 4004:
                                            p = serviciosadicionales.MegabytesDeNavegacion(p)
                                            break
                                        else:
                                            print "\nERROR: La opcion no es valida."                                   


                                    #Procede a afiliar el producto.
                                    af = afiliaciones.Afiliaciones(p.get_id(),p.get_codigo())
                                    af.CrearContratacion()

                                    #Actualiza la cantidad de paquetes disponibles
                                    numPaquetes = afiliaciones.numPaquetesAContratar(producto31)   
                                    
                                    #Muestra la informacion actual del producto
                                    print "\nSu producto ahora posee la siguiente informacion: "
                                    print p

                                    #Verifica si se desea seguir afiliando paquetes
                                    while True: 
                                        x = validacion.validarInput('\nDesea seguir afiliando? (s/n): ')
                                        if x == 's':
                                            break
                                        elif x == 'n':      
                                            continua = False
                                            break                                            
                                        else:
                                            print "\nERROR: La opcion no es valida."
                                
                                if (afiliaciones.numPaquetesAContratar(producto31) == 0):
                                    print "\nYa ha contratado todos los paquetes de servicios."
                                                                        
                            else:
                                print "\nEl producto no esta afiliado a un plan; por lo que no se puede afiliar un paquete de servicios."
                            
                            flag31 = False
                              
                        ## Opcion para regresar al menu de Afiliaciones
                        elif op31 == 3: 
                            print "\n3.- Regresar."                     
                            flag31 = False
                            
                        elif (op31 > 3 or op31 <= 0):
                            print "\nERROR: La opcion no es valida."    
                            
                ## Opcion para desafiliar un producto
                elif op3 == 2:     
                    
                    flag32 = True
                    producto32 = productos.validarSerie()  
                    while flag32:       
                        print "\n2.- Desafiliar."             
                        print "   1.- Desafiliar un producto de su plan asociado."
                        print "   2.- Regresar."
                
                        op32 = int(validacion.validarNumero('Opcion: '))
                        
                        ## Opcion desafiliar un producto de su plan
                        if op32 == 1:
                            print "\nDesafiliar un producto de su plan asociado"
                            
                            Afiliacion = afiliaciones.Afiliaciones(producto32,0)                            
                            codigo_plan = Afiliacion.ConsultarPlanes()
                            if codigo_plan != None:

                                flag321 = True                                
                                while flag321:
                                    print "\nDesea desafiliar el producto %s del plan de codigo %s?"%(producto32,codigo_plan)
                                    print "\nATENCIÓN: Esto hará que se eliminen las contrataciones de paquetes y servicios adicionales del produco"
                                    op321 = validacion.validarInput('(y/n)?')                                    
                                    if op321 == 'y' or op321 == 'Y':
                                        Afiliacion = afiliaciones.Afiliaciones(producto32,codigo_plan)
                                        Afiliacion.DesafiliarProducto()
                                        print "\nSe ha eliminado la afiliacion del producto %s con el plan %s"%(producto32,codigo_plan)
                                        Afiliacion.EliminarContrataciones()
                                        flag321 = False
                                        
                                    elif op321 == 'n' or op321 == 'N':
                                        print "\nSe ha cancelado la desafiliacion"
                                        flag321 = False
                                    
                                    else:
                                        print "\nERROR: La opcion no es valida."
                                        
                            else:
                                print "\nERROR: No puede desafiliar si el producto no tiene un plan asociado"
   
                        ## Opcion regresar al menu de afiliaciones
                        elif op32 == 2: 
                            print "\n3.- Regresar."
                            flag32 = False
                        elif (op32 > 2 or op32 <= 0):
                            print "\nERROR: La opcion no es valida."
                            
                ## Opcion consultar planes y paquetes de un producto         
                elif op3 == 3: 
                    print "\n3.- Consultar plan/paquetes de un producto."
                    producto33 = productos.validarSerie()
                    Afiliacion = afiliaciones.Afiliaciones(producto33,1) 
                    Afiliacion.ConsultarPlanes()

                ## Opcion volver al menu anterior
                elif op3 == 4: 
                    print "\n4.- Regresar al menu anterior."                    
                    flag3 = False 
  
                elif (op3 > 4 or op3 <= 0):
                    print "\nERROR: La opcion no es valida."

        ## Opcion de Consumos 
        elif op == 4:   
            
            flag4 = True
            while flag4:    
                print "\nMODULO CONSUMOS\n"                
                print "   1.- Registrar un consumo."
                print "   2.- Consultar consumos de un producto."
                print "   3.- Regresar al menu anterior."
        
                op4 = int(validacion.validarNumero('Opcion: '))
                if op4 == 1:
                    print "\n1.- Registrar un consumo."
                    
                    print "\nMostrando todos los productos disponibles: "
                    productos.listarProductos()
            
                    gestionarConsumos.crearConsumoInteractivo()
                elif op4 == 2:     
                    print "\n2.- Consultar consumos de un producto."   
                    
                    print "\nMostrando todos los productos disponibles: "
                    productos.listarProductos()
                    gestionarConsumos.consumosProducto()
                elif op4 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag4 = False
                elif (op4 > 3 or op4 <= 0):
                    print "\nERROR: La opcion no es valida."
       
        ## Opcion de generacion de facturas
        elif op == 5:   
            flag5 = True
            while flag5:      
                print "\nMODULO GENERACION DE FACTURAS"              
                print "   1.- Generar la factura de un cliente."
                print "   2.- Regresar al menu anterior."        
                op5 = int(validacion.validarNumero('Opcion: '))
                if op5 == 1:                    
                    print "\n1.- Generar la factura de un cliente."  
                    #Genera la factura
                    fact = gestionarFactura.pedirFactura()
                    if fact:
                        print fact
                   
                elif op5 == 2: 
                    print "\n2.- Regresar al menu anterior."
                    flag5 = False
                elif (op5 > 2 or op5 <= 0):
                    print "\nERROR: La opcion no es valida."  
        
        ## Opcion salir
        elif op == 6: 
            print "\nHasta luego."
            flag = False
        elif (op > 6 or op <= 0):
            print "\nERROR: La opcion no es valida."


if __name__== "__main__":
    main()
    sys.exit()    
        
#END menu.py
