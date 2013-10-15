from django.db import models

# ToDo: Existen productos con costo, que es un Float mayor que cero
# Django no tiene un tipo para esto, asi que hay que implementarlo

# Create your models here.
PLANTYPECHOICES = ('i', 'infinito'), ('p', 'paquete'),
PLANMODECHOICES = ('p', 'prepago'), ('p', 'postpago'),

class Cliente(models.Model):
    cedula = models.PositiveIntegerField('Cedula',unique=True)
    nombrecl = models.CharField('Nombre',max_length=50)
    direccion = models.TextField('Direccion')
    
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
	return "Codigo: " + str(self.codplan) \
	    +" | Nombre: " + str(self.nombreplan)
	
class PlanPostpago(models.Model):
    codplan = models.ForeignKey('Plan')
    
    def __unicode__(self):
	return str(self.codplan)
    
class PlanPrepago(models.Model):
    codplan = models.ForeignKey('Plan')
    
    def __unicode__(self):
	return str(self.codplan)

class Producto(models.Model):
    numserie = models.CharField('Numero de serie',max_length=10,unique=True)
    nombreprod = models.CharField('Nombre del producto',max_length=50)
    RIF = models.ForeignKey('Empresa')
    cedula = models.ForeignKey('Cliente')
    planPrepago  = models.ManyToManyField(PlanPrepago, through='Activa',blank=True)
    planPostpago = models.ManyToManyField(PlanPostpago, through='Afilia',blank=True)
    
    def __unicode__(self):
	return "Serial: " + str(self.numserie) \
	    +" | Nombre: " + str(self.nombreprod)
	
class Activa(models.Model):
    codplan = models.ForeignKey('PlanPrepago')
    numserie = models.ForeignKey('Producto')
    saldo = models.FloatField()
    
class Afilia(models.Model):
    codplan = models.ForeignKey('PlanPostpago')
    numserie = models.ForeignKey('Producto')
    tipoplan = models.CharField(max_length=8,choices=PLANTYPECHOICES)

class Servicio(models.Model):
    codserv = models.PositiveIntegerField(unique=True)
    nombreserv = models.CharField(max_length=50)
    costo = models.FloatField()
    unico = models.BooleanField(default=False)
    
    def __unicode__(self):
	return "Nombre: " + self.nombreserv
    
class Consume(models.Model):
    numserie = models.ForeignKey('Producto')
    codserv = models.ForeignKey('Servicio')
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()
    
class Contiene(models.Model):
    codpaq = models.ForeignKey('Paquete')
    codserv = models.ForeignKey('Servicio')
    cantidad = models.PositiveIntegerField()

class Contrata(models.Model):
    numserie = models.ForeignKey('Producto')
    codpaq = models.ForeignKey('Paquete')

class Contiene(models.Model):
    codplan = models.ForeignKey('Plan')
    codserv = models.ForeignKey('Servicio')
    cantidad = models.PositiveIntegerField()
    tarifa = models.FloatField()
    
class Recarga(models.Model):
    numserie = models.ForeignKey('Producto')
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()