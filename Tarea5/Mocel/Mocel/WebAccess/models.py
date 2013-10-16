from django.db import models
from django.db.models.signals import post_delete
from signalActions import borradoPlan
from django.core.validators import MinValueValidator

# A continuacion se encuentra la traduccion de las entidades de la DB
# a modelos de Django
#
# Estandares:
# - Los nombres de atributos se mantienen, tal cual estan en el ER
# - Se define el metodo __unicode__ en cada clase, para tener una
#   representacion leible de cada entidad
# - En el caso de los precios (productos, paquetes, etc) se usan los 
#   validadores de django, que se pasan al constructor del atributo
# - Se usa la metaclase para colocar nombres bonitos a los modelos

# Create your models here.
PLANTYPECHOICES = ('i', 'infinito'), ('p', 'paquete'),
PLANMODECHOICES = ('pr', 'prepago'), ('po', 'postpago'),

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
    precio = models.FloatField(validators = [MinValueValidator(0)])
    
    def __unicode__(self):
	return "Codigo: " + str(self.codpaq) \
	    +" | Nombre: " + str(self.nombrepaq)
	
class PlanPostpago(models.Model):
    codplan = models.ForeignKey('Plan')
    
    def __unicode__(self):
	return str(self.codplan)
    
class PlanPrepago(models.Model):
    codplan = models.ForeignKey('Plan')
    
    def __unicode__(self):
	return str(self.codplan)

class Plan(models.Model):
    class Meta:
        verbose_name_plural = 'Planes'
        
    # Se hace override del metodo por defecto del modelos
    # La idea es insertar la tupla correspondiente en la 
    # categoria planPrepago o planPostpago segun corresponda
 
    
    def save(self):
	try:
	    super(Plan,self).save()
	except Exception,e:
	    raise e
	
	if self.tipo == "pr":
	    # Si el plan fue cambiado, busco su instancia en PlanPrepago para 
	    # borrarla. No consigo como saber que valor fue editado, para no hacer
	    # esto a cada rato
	    if self.pk is not None:
		aBorrar = PlanPostpago.objects.filter(codplan=self)
	    if not len(PlanPrepago.objects.filter(codplan=self)):
		plan = PlanPrepago(codplan=self)
		plan.save()
	else:
	    if self.pk is not None:
		aBorrar = PlanPrepago.objects.filter(codplan=self)
	    if not len(PlanPostpago.objects.filter(codplan=self)):
		plan = PlanPostpago(codplan=self)
		plan.save()
	
	# Borro su entrada en la categoria
	aBorrar.delete()
	
		
    codplan = models.PositiveIntegerField(unique=True)
    nombreplan = models.CharField(max_length=50)
    descripcion = models.TextField()
    renta_basica = models.FloatField(validators = [MinValueValidator(0)])
    renta_ilimitada = models.FloatField(validators = [MinValueValidator(0)])
    tipo = models.CharField(max_length=8,choices=PLANMODECHOICES)
    
    def __unicode__(self):
	return "Codigo: " + str(self.codplan) \
	    +" | Nombre: " + str(self.nombreplan)

class Producto(models.Model):
    numserie = models.CharField('Numero de serie',max_length=10,unique=True)
    nombreprod = models.CharField('Nombre del producto',max_length=50)
    RIF = models.ForeignKey('Empresa')
    cedula = models.ForeignKey('Cliente')
    planPrepago  = models.ManyToManyField(PlanPrepago, through='Activa')
    planPostpago = models.ManyToManyField(PlanPostpago, through='Afilia')
    
    def __unicode__(self):
	return "Serial: " + str(self.numserie) \
	    +" | Nombre: " + str(self.nombreprod)
	
class Activa(models.Model):
    class Meta:
        verbose_name = 'una afiliacion a plan Prepago'
        verbose_name_plural = 'Afiliaciones a planes Prepago'
    
    codplan = models.ForeignKey('PlanPrepago')
    numserie = models.ForeignKey('Producto')
    saldo = models.FloatField(validators = [MinValueValidator(0)])
    
class Afilia(models.Model):
    
    class Meta:
        verbose_name = 'una afiliacion a plan Postpago'
        verbose_name_plural = 'Afiliaciones a planes Postpago'
        
    codplan = models.ForeignKey('PlanPostpago')
    numserie = models.ForeignKey('Producto')
    tipoplan = models.CharField(max_length=8,choices=PLANTYPECHOICES)

class Servicio(models.Model):
    codserv = models.PositiveIntegerField(unique=True)
    nombreserv = models.CharField(max_length=50)
    costo = models.FloatField(validators = [MinValueValidator(0)])
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

class Incluye(models.Model):
    codplan = models.ForeignKey('Plan')
    codserv = models.ForeignKey('Servicio')
    cantidad = models.PositiveIntegerField()
    tarifa = models.FloatField(validators = [MinValueValidator(0)])
    
class Recarga(models.Model):
    numserie = models.ForeignKey('Producto')
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()
    
# Accion asociada al eliminar un plan
post_delete.connect(borradoPlan, sender=Plan)
