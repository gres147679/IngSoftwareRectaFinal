# Modulo menu.py
#!/usr/bin/env python
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import validacion
import moduloCliente
import productos
import consumos
import Afiliaciones
import Factura

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
                    
                    print "Mostrando todos los clientes: "
                    moduloCliente.listarClientes()
                    
                    moduloCliente.consultaClientes()         
                elif op1 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag1 = False
                elif (op1 > 3 or op1 <= 0):
                    print "\nERROR: La opcion no es valida."
                    
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
        elif op == 3:    
            flag3 = True

            while flag3:
                print "\nMODULO AFILIACIONES\n"                   
                print "   1.- Afiliar un producto."
                print "   2.- Desafiliar un producto."
                print "   3.- Consultar planes de un producto."
                print "   4.- Regresar al menu anterior."     
                           
                op3 = int(validacion.validarNumero('Opcion: '))
                
                print "Mostrando todos los productos disponibles: "
                productos.listarProductos()
                
                if op3 == 1:
                    producto31 = productos.validarSerie()   
                    flag31 = True                                       
                    
                    while flag31: 
                        print "\n1.- Afiliar un producto a un :"                   
                        print "   1.- Plan."
                        print "   2.- Paquete de Servicios."
                        print "   3.- Regresar."
                
                        op31 = int(validacion.validarNumero('Opcion: '))
                        if op31 == 1:
                            
                            print "\n1.- Plan."
                            
                            print "Mostrando todos los planes disponibles: "
                            Afiliaciones.impPlanes()
                            
                            cod_plan = int(validacion.validarNumero('Introduzca el codigo del plan: '))
                            Afiliacion = Afiliaciones.Afiliaciones(producto31,cod_plan)                            
                            Afiliacion.CrearAfiliacion()
                            flag31 = False
                            
                        elif op31 == 2:     
                            print "\n2.- Paquete de Servicios."
                            
                            print "Mostrando todos los paquetes de servicios disponibles: "
                            Afiliaciones.impPaquetes()
                            
                            cod_ser = int(validacion.validarNumero('Introduzca el codigo del paquete de servicio: '))
                            Afiliacion = Afiliaciones.Afiliaciones(producto31,cod_ser)                            
                            Afiliacion.CrearContratacion()
                            flag31 = False
                              
                        elif op31 == 3: 
                            print "\n3.- Regresar."                     
                            flag31 = False
                            
                        elif (op31 > 3 or op31 <= 0):
                            print "\nERROR: La opcion no es valida."
                            

                elif op3 == 2:     
                    
                    flag32 = True
                    producto32 = productos.validarSerie()  
                    while flag32:       
                        print "\n2.- Desafiliar un producto a un: ."             
                        print "   1.- Plan."
                        print "   2.- Paquete de Servicios."
                        print "   3.- Regresar."
                
                        op32 = int(validacion.validarNumero('Opcion: '))
                        if op32 == 1:
                            print "\n1.- Plan."
                            
                            print "Mostrando todos los planes disponibles: "
                            Afiliaciones.impPlanes()
                            
                            cod_plan = int(validacion.validarNumero('Introduzca el codigo del plan: '))
                            Afiliacion = Afiliaciones.Afiliaciones(producto32,cod_plan)                            
                            Afiliacion.DesafiliarProducto()
                            
                        elif op32 == 2:     
                            print "\n2.- Paquete de Servicios."
                            
                            print "Mostrando todos los paquetes de servicios disponibles: "
                            Afiliaciones.impPaquetes()
                            
                            cod_ser = int(validacion.validarNumero('Introduzca el codigo del paquete de servicio: '))
                            Afiliacion = Afiliaciones.Afiliaciones(producto32,cod_ser)                            
                            Afiliacion.desafiliarContratacion()                          
                            
                        elif op32 == 3: 
                            print "\n3.- Regresar."
                            flag32 = False
                        elif (op32 > 3 or op32 <= 0):
                            print "\nERROR: La opcion no es valida."
                            
                           
                elif op3 == 3: 
                    print "\n3.- Consultar planes de un producto."
                    producto33 = productos.validarSerie()
                    Afiliacion = Afiliaciones.Afiliaciones(producto33,1) 
                    Afiliacion.ConsultarPlanes()

                elif op3 == 4: 
                    print "\n4.- Regresar al menu anterior."                    
                    flag3 = False 
  
                elif (op3 > 4 or op3 <= 0):
                    print "\nERROR: La opcion no es valida."

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
                    
                    print "Mostrando todos los productos disponibles: "
                    productos.listarProductos()
            
                    consumos.crearConsumoInteractivo()
                elif op4 == 2:     
                    print "\n2.- Consultar consumos de un producto."   
                    
                    print "Mostrando todos los productos disponibles: "
                    productos.listarProductos()
                    consumos.consumosProducto()
                elif op4 == 3: 
                    print "\n3.- Regresar al menu anterior."
                    flag4 = False
                elif (op4 > 3 or op4 <= 0):
                    print "\nERROR: La opcion no es valida."
                    
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
                    fact = Factura.pedirFactura()
                    if fact:
		      print fact
                   
                elif op5 == 2: 
                    print "\n2.- Regresar al menu anterior."
                    flag5 = False
                elif (op5 > 2 or op5 <= 0):
                    print "\nERROR: La opcion no es valida."  
                                                
        elif op == 6: 
            print "\nHasta luego."
            flag = False
        elif (op > 6 or op <= 0):
            print "\nERROR: La opcion no es valida."


if __name__== "__main__":
    main()
    sys.exit()    
        
#END menu.py
