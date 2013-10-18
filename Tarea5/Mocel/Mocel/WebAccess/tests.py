"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Empresa, Plan, Cliente, Producto, Activa, Afilia, PlanPostpago, PlanPrepago

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
                
class PruebaPlan(TestCase):
    def setUp(self):
     pre = Plan(codplan = 121, nombreplan = "prepago1", tipo = "pr",renta_basica =35, renta_ilimitada = 70)
     pre.save()
     post = Plan(codplan = 122, nombreplan = "postpago1", tipo = "po",renta_basica =35, renta_ilimitada = 70)
     post.save()
     
    def tearDown(self):
     Empresa.objects.filter(RIF = 100).delete()
     Cliente.objects.filter(cedula=101).delete()
     Producto.objects.filter(numserie =201).delete()

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


