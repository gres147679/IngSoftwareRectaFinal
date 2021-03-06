"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from views import generarFactura

                
class PruebaPlan(TestCase):
    def setUp(self):
     pre = Plan(codplan = 121, nombreplan = "prepago1", tipo = "pr",renta_basica =35, renta_ilimitada = 70)
     pre.save()
     post = Plan(codplan = 122, nombreplan = "postpago1", tipo = "po",renta_basica =35, renta_ilimitada = 70)
     post.save()

    #Se creo un plan prepago con codigo 121     
    def testPrepago(self):
      pl = Plan.objects.get(codplan = 121)
      cantPrepago = PlanPrepago.objects.filter(codplan = pl).count()
      self.assertEqual(cantPrepago, 1)
      
    #Se creo un plan postpago con codigo 122     
    def testPostpago(self):
      pl = Plan.objects.get(codplan = 122)
      cantPostpago = PlanPostpago.objects.filter(codplan = pl).count()
      self.assertEqual(cantPostpago, 1)

#class PruebaFactura(TestCase):
#    def setUp(self):
#      e = Empresa.objects.create(RIF = 100, razon_social = 'Empresa1')
#      c = Cliente.objects.create(cedula=101, nombrecl ='cliente1', direccion = 'dir1')
#      pl = Plan(codplan = 121, nombreplan = "prepago1", tipo = "pr",renta_basica =35, renta_ilimitada = 70)
#      pl.save()
#      p = Producto.objects.create(numserie =201, nombreprod ="abcd",cedula = c, RIF = e)
#      pre = PlanPrepago.objects.get(codplan = pl)
#      Activa.objects.create(codplan = pre, numserie = p, saldo = 25)
#      paq = Paquete.objects.create(codpaq = 301, nombrepaq = 'paquete1', precio = 30)
#      Contrata.objects.create(codpaq = paq, numserie = p)
      
    # Se prueba el monto del plan  
    #def testMontoPlan(self):
        #p = Producto.objects.get(numserie = 201)
        #f = generarFactura(p, 10,2013)
        #montoPlan =  f['totalPlan']
   
        #self.assertEqual(montoPlan, 35)
        
    #Se prueba el monto del paquete     
    #def testPaquete(self):
        #p = Producto.objects.get(numserie = 201)
        #f = generarFactura(p, 10,2013)
        #montoPaq =  f['totalPaquetes']
        
        #self.assertEqual(montoPaq, 30)
        
    #Se prueba el monto total    
    #def testMontoTotal(self):
        #p = Producto.objects.get(numserie = 201)
        #f = generarFactura(p, 10,2013)
        #montoTotal =  f['total']
        
        #self.assertEqual(montoTotal, 65 )
      
#class PruebaFactura2(TestCase):
#    def setUp(self):
#      #Creacion del producto
#      e = Empresa.objects.create(RIF = 100, razon_social = 'Empresa1')
#      c = Cliente.objects.create(cedula=101, nombrecl ='cliente1', direccion = 'dir1')
#      pl = Plan(codplan = 121, nombreplan = "prepago1", tipo = "pr",renta_basica =211, renta_ilimitada = 300)
#      pl.save()
#      p = Producto.objects.create(numserie =201, nombreprod ="abcd",cedula = c, RIF = e)
      
      ##Afiliacion de producto a planes y paquetes
      #pre = PlanPrepago.objects.get(codplan = pl)
      #Activa.objects.create(codplan = pre, numserie = p, saldo = 25)
      #paq1 = Paquete.objects.create(codpaq = 301, nombrepaq = 'paquete1', precio = 30)
      #paq2 = Paquete.objects.create(codpaq = 302, nombrepaq = 'paquete2', precio = 45)
      #Contrata.objects.create(codpaq = paq1, numserie = p)
      #Contrata.objects.create(codpaq = paq2, numserie = p)
      
      ##Indicar los servicios
      #s1 = Servicio.objects.create(codserv = 3001, nombreserv = 'serv1', costo = 1.5) 
      #s2 = Servicio.objects.create(codserv = 3002, nombreserv = 'serv2', costo = 3.0)
      #s3 = Servicio.objects.create(codserv = 3003, nombreserv = 'serv3', costo = 5.0) 
      
      ##Indicar que incluye/contiene cada plan/paquete
      #Incluye.objects.create(codplan = pl, codserv = s1, cantidad = 50, tarifa = 0)
      #Incluye.objects.create(codplan = pl, codserv = s2, cantidad = 100, tarifa = 0)
      #Contiene.objects.create(codpaq = paq1, codserv = s2, cantidad = 50)
      #Contiene.objects.create(codpaq = paq1, codserv = s3, cantidad = 25)
      
      ##Consumos del producto
      #Consume.objects.create(numserie = p, codserv = s1, fecha = '2011-01-01 10:10', cantidad = 55)
      #Consume.objects.create(numserie = p, codserv = s2, fecha = '2011-01-02 10:15', cantidad = 145)
      
      
    # Se prueba el monto del plan  
#    def testMontoPlan(self):
#        p = Producto.objects.get(numserie = 201)
#        f = generarFactura(p, 01,2011)
#        montoPlan =  f['total']
#        self.assertEqual(montoPlan,0)
   
        #self.assertEqual(montoPlan, 211)
        
    ##Se prueba el monto del paquete     
    #def testPaquete(self):
        #p = Producto.objects.get(numserie = 201)
        #f = generarFactura(p, 01,2011)
        #montoPaq =  f['totalPaquetes']
        
        #self.assertEqual(montoPaq, 75)
        
    ##Se prueba el monto total    
    #def testMontoTotal(self):
        #p = Producto.objects.get(numserie = 201)
        #f = generarFactura(p, 01,2011)
        #montoTotal =  f['total']
        
        #self.assertEqual(montoTotal, 286)

# Prueba de Triggers

# Prueba que el servicio unico debe ser ofrecido solo una vez
# En el caso que se crea con una cantidad mayor que uno, falla
class ServicioUnico1(TestCase):
    def setUp(self):
      serv = Servicio.objects.create(codserv = 3002, nombreserv = 'serv1', costo = 1.5, unico = True)
      
      paq = Paquete.objects.create(codpaq = 301, nombrepaq = 'paquete1', precio = 30)
      cont = Contiene.objects.create(codpaq = paq, codserv = serv, cantidad = 1)
      
      plan  = Plan(codplan = 123, nombreplan = "plan basico", tipo = "pr",renta_basica =25, renta_ilimitada = 50)
      plan.save()
      inc = Incluye.objects.create(codplan = plan, codserv = serv, cantidad = 1, tarifa = 10)
      
    def testServicioUnicoPaquete(self):
      paq = Paquete.objects.get(codpaq =301)
      cont = Contiene.objects.filter(codpaq= paq).count()
      self.assertEqual(cont, 1)
  
    def testServicioUnicoPlan(self):
      plan = Plan.objects.get(codplan =123)
      inc = Incluye.objects.filter(codplan= plan).count()
      self.assertEqual(inc, 1)



# Prueba que un producto no puede consumir si no esta asociado a un plan
#class PruebaConsume(TestCase):
    #def setUp(self):
      #s1 = Servicio.objects.create(codserv = 3003, nombreserv = 'serv1', costo = 1.5) 
      #e = Empresa.objects.create(RIF = 100, razon_social = 'Empresa1')
      #c = Cliente.objects.create(cedula=101, nombrecl ='cliente1', direccion = 'dir1')
      #p = Producto.objects.create(numserie =201, nombreprod ="abcd",cedula = c, RIF = e)
      
      #cons = Consume(numserie = p, codserv = s1, fecha = '2011-01-01 10:10', cantidad = 55)
      #cons.save()

    #def testConsume(self):
      #p = Producto.objects.get(numserie =201)
      #c = Consume.objects.filter(numserie = p).count()
      #self.assertEqual(c, 0)
 
## Prueba que un producto no puede consumir si no posee saldo
#class PruebaConsume2(TestCase):
    #def setUp(self):
      #e = Empresa.objects.create(RIF = 100, razon_social = 'Empresa1')
      #c = Cliente.objects.create(cedula=101, nombrecl ='cliente1', direccion = 'dir1')
      #pl = Plan(codplan = 121, nombreplan = "prepago1", tipo = "pr",renta_basica =211, renta_ilimitada = 300)
      #pl.save()
      #p = Producto.objects.create(numserie =201, nombreprod ="abcd",cedula = c, RIF = e)
      #pre = PlanPrepago.objects.get(codplan = pl)
      #Activa.objects.create(codplan = pre, numserie = p, saldo = -5)
      
      #Consume.objects.create(numserie = p, codserv = s1, fecha = '2011-01-01 10:10', cantidad = 55)
      

    #def testConsume2(self):
      #p = Producto.objects.get(numserie =201)
      #c = Consume.objects.filter(numserie = p).count()
      #self.assertEqual(c, 0) 

# Prueba de actualizacion de saldo por recarga   
class PruebaSaldoRecarga(TestCase):
    def setUp(self):
      e = Empresa.objects.create(RIF = 102, razon_social = 'Empresa1')
      c = Cliente.objects.create(cedula=101, nombrecl ='cliente1', direccion = 'dir1')
      pl = Plan(codplan = 127, nombreplan = "prepago1", tipo = "pr",renta_basica =211, renta_ilimitada = 300)
      pl.save()
      p = Producto.objects.create(numserie =201, nombreprod ="abcd",cedula = c, RIF = e)
      
      pre = PlanPrepago.objects.get(codplan = pl)
      ac =Activa.objects.create(codplan = pre, numserie = p, saldo = 25)
      
      r = Recarga.objects.create(numserie = p, cantidad = 50, fecha ='2011-01-01 10:10:00')
     

    def testRecarga(self):
      p = Producto.objects.get(numserie = 201)
      ac = Activa.objects.get(numserie = p)
      self.assertEqual(ac.saldo, 75)
     
# Prueba de actualizacion de saldo por consumo   
#class PruebaSaldoConsumo(TestCase):
#    def setUp(self):
#      #Crea un producto y lo asocia a un plan prepago
#      e = Empresa.objects.create(RIF = 102, razon_social = 'Empresa1')
#      c = Cliente.objects.create(cedula=101, nombrecl ='cliente1', direccion = 'dir1')
#      pl = Plan(codplan = 128, nombreplan = "prepago1", tipo = "pr",renta_basica =211, renta_ilimitada = 300)
#      pl.save()
#      p = Producto.objects.create(numserie =203, nombreprod ="abcd",cedula = c, RIF = e)
#      pre = PlanPrepago.objects.get(codplan = pl)
#      ac = Activa.objects.create(codplan = pre, numserie = p, saldo = 50)
#      
#      #Crea un servicio que es incluido por el plan
#      serv = Servicio.objects.create(codserv = 3032, nombreserv = 'serv1', costo = 1.5)
##      paq1 = Paquete.objects.create(codpaq = 301, nombrepaq = 'paquete1', precio = 30)
##      Contiene.objects.create(codpaq = paq1, codserv = serv, cantidad = 10)
#      inc = Incluye(codplan = pl, codserv = serv, cantidad = 10, tarifa = 1.5)
#      inc.save()
#      
#      #Consume una cantidad mayor de servicio ofrecido por el plan
#      Consume.objects.create(numserie = p, codserv = serv, fecha = '2011-01-01 10:10:00', cantidad = 20)
#     

#    def testRecarga(self):
#      p = Producto.objects.get(numserie = 201)
#      ac = Activa.objects.get(numserie = p)
#      print ac.saldo
#      self.assertEqual(ac.saldo, 35)

