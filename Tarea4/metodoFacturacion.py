# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod  

# Interfaz metodoFacturación
# Define una interfaz para la estrategia que usa la factura para calcular
# el total del monto y la presentación final de la factura

class metodoFacturacion:
  __metaclass__ = ABCMeta
  
  def __init__(self):
    pass
    
  def facturar(self):
    pass