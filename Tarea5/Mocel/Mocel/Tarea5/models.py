from django.db import models

# Create your models here.
PLANTYPECHOICES = ('i', 'infinito'), ('p', 'paquete'),
PLANMODECHOICES = ('p', 'prepago'), ('p', 'postpago'),

class Cliente(models.Model):
    cedula = models.PositiveIntegerField(unique=True)
    nombrecl = models.CharField(max_length=50)
    direccion = models.TextField()
    
    def __unicode__(self):
	return "Cedula: " + str(self.cedula) \
	    +" | Nombre: " + str(self.nombrecl)
    
class Empresa(models.Model):
    RIF = models.PositiveIntegerField(unique=True)
    razon_social = models.CharField(max_length=50)
    
    def __unicode__(self):
	return "Empresa: " + str(self.razon_social)

class Paquete(models.Model):
    codpaq = models.PositiveIntegerField(unique=True)
    nombrepaq = models.CharField(max_length=50)
    precio = models.FloatField()
    
    def __unicode__(self):
	return "Codigo: " + str(self.codpaq) \
	    +" | Nombre: " + str(self.nombrepaq)
	
class Plan(models.Model):
    codplan = models.PositiveIntegerField(unique=True)
    nombreplan = models.CharField(max_length=50)
    descripcion = models.TextField()
    renta_basica = models.FloatField()
    renta_ilimitada = models.FloatField()
    tipo = models.CharField(max_length=8,choices=PLANMODECHOICES)
    
    def __unicode__(self):
	return "Codigo: " + str(self.codpaq) \
	    +" | Nombre: " + str(self.nombrepaq)