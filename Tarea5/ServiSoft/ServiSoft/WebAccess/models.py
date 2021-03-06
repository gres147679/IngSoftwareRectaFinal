# -*- coding: utf-8 -*-
import os, sys
from django.db import models
from signalActions import borradoPlan, insertadoServicio, borradoServicio
from django.core.validators import MinValueValidator
from django.db.models import signals
from django.db import connection, transaction
from django.conf import settings

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
	return u"Cédula: " + unicode(self.cedula) \
	    +" | Nombre: " + unicode(self.nombrecl)
	    
class Usuario(models.Model):
    cedula = models.ForeignKey('Cliente',related_name="username",unique=True)
    password = models.CharField('password',max_length=12)
    
    def __unicode__(self):
	return "username: " + unicode(self.cedula) \
	    +" | password: " + "*"*len(self.password)
    
    
class Empresa(models.Model):
    RIF = models.PositiveIntegerField(unique=True)
    razon_social = models.CharField(max_length=50)
    
    def __unicode__(self):
	return "Empresa: " + unicode(self.razon_social)

class Paquete(models.Model):
    codpaq = models.PositiveIntegerField('Código',unique=True)
    nombrepaq = models.CharField('Nombre',max_length=50)
    precio = models.FloatField('Renta',validators = [MinValueValidator(0)])
    
    def __unicode__(self):
	return u"Código: " + unicode(self.codpaq) \
	    +" | Nombre: " + unicode(self.nombrepaq)
	
class PlanPostpago(models.Model):
    codplan = models.ForeignKey('Plan')
    
    def __unicode__(self):
	return unicode(self.codplan)
    
class PlanPrepago(models.Model):
    codplan = models.ForeignKey('Plan')
    
    def __unicode__(self):
	return unicode(self.codplan)

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
	
		
    codplan = models.PositiveIntegerField('Código',unique=True)
    nombreplan = models.CharField('Nombre',max_length=50)
    descripcion = models.TextField('Descripcion')
    renta_basica = models.FloatField('Renta normal',validators = [MinValueValidator(0)])
    renta_ilimitada = models.FloatField('Renta ilimitada',validators = [MinValueValidator(0)])
    tipo = models.CharField('Tipo',max_length=8,choices=PLANMODECHOICES)
    
    def __unicode__(self):
	return u"Código: " + unicode(self.codplan) \
	    +" | Nombre: " + unicode(self.nombreplan)

class Producto(models.Model):
    numserie = models.CharField('Número de serie',max_length=10,unique=True)
    nombreprod = models.CharField('Nombre del producto',max_length=50)
    RIF = models.ForeignKey('Empresa',verbose_name="Empresa dueña")
    cedula = models.ForeignKey('Cliente',verbose_name="Cliente dueño")
    planPrepago  = models.ManyToManyField(PlanPrepago, through='Activa')
    planPostpago = models.ManyToManyField(PlanPostpago, through='Afilia')
    
    def __unicode__(self):
	return "Serial: " + unicode(self.numserie) \
	    +" | Nombre: " + unicode(self.nombreprod)
	
class Activa(models.Model):
    class Meta:
        verbose_name = 'afiliacion a plan Prepago'
        verbose_name_plural = 'Afiliaciones a planes Prepago'
    
    codplan = models.ForeignKey('PlanPrepago',verbose_name='Plan')
    numserie = models.ForeignKey('Producto',verbose_name='Producto')
    saldo = models.FloatField(validators = [MinValueValidator(0)],verbose_name='Saldo')
    
class Afilia(models.Model):
    
    class Meta:
        verbose_name = 'una afiliacion a plan Postpago'
        verbose_name_plural = 'Afiliaciones a planes Postpago'
        
    codplan = models.ForeignKey('PlanPostpago',verbose_name='Plan')
    numserie = models.ForeignKey('Producto',verbose_name='Producto')
    tipoplan = models.CharField(max_length=8,choices=PLANTYPECHOICES,verbose_name='Tipo de plan')

class Servicio(models.Model):
    codserv = models.PositiveIntegerField('Código',unique=True)
    nombreserv = models.CharField('Nombre',max_length=50)
    costo = models.FloatField('Costo',validators = [MinValueValidator(0)])
    unico = models.BooleanField('Servicio único',default=False)
    
    def __unicode__(self):
	return "Nombre: " + self.nombreserv
    
class Consume(models.Model):

    numserie = models.ForeignKey('Producto')
    codserv = models.ForeignKey('Servicio')
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()
    
class Contiene(models.Model):
    class Meta:
        verbose_name = 'servicio en un paquete'
        verbose_name_plural = 'Servicios en un paquete'
    
    codpaq = models.ForeignKey('Paquete',verbose_name='Paquete')
    codserv = models.ForeignKey('Servicio',verbose_name='Servicio')
    cantidad = models.PositiveIntegerField('Cantidad')
    
    def __unicode__(self):
	return "El paquete " + unicode(self.codpaq.nombrepaq) + " contiene " + unicode(self.cantidad)+"x"+unicode(self.codserv.nombreserv)

class Contrata(models.Model):
    class Meta:
        verbose_name = 'afiliacion a un paquete'
        verbose_name_plural = 'Afiliaciones a paquetes'
    
    numserie = models.ForeignKey('Producto',verbose_name='Producto')
    codpaq = models.ForeignKey('Paquete',verbose_name='Paquete')

class Incluye(models.Model):
    class Meta:
        verbose_name = 'servicio en un plan'
        verbose_name_plural = 'Servicios en un plan'
        
    def __unicode__(self):
	return 'El plan ' + str(self.codplan.nombreplan) + ' incluye '+ str(self.cantidad) + '*'+ str(self.codserv.nombreserv)
    
    codplan = models.ForeignKey('Plan',verbose_name='Plan')
    codserv = models.ForeignKey('Servicio',verbose_name='Servicio')
    cantidad = models.PositiveIntegerField('Cantidad')
    tarifa = models.FloatField('Tarifa',validators = [MinValueValidator(0)])
    
class Recarga(models.Model):
    numserie = models.ForeignKey('Producto')
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()
    
# Accion asociada al eliminar un plan
signals.post_delete.connect(borradoPlan, sender=Plan)

# Accion asociada al crear un Servicio, que crea el paquete
# asociado al servicio adicional
signals.post_save.connect(insertadoServicio, sender=Servicio)

# Accion asociada al crear un Servicio
signals.post_delete.connect(borradoServicio, sender=Servicio)


# Ejecucion de triggers
def load_customized_sql(app, created_models, verbosity=2, **kwargs):
    app_dir = os.path.normpath(os.path.join(os.path.dirname(app.__file__),      'sql'))
    custom_files = [os.path.join(app_dir, "triggers.sql")]

    for custom_file in custom_files: 
        if os.path.exists(custom_file):
            print "Loading customized SQL for %s" % app.__name__
            fp = open(custom_file, 'U')
            cursor = connection.cursor()
            try:
                cursor.execute(fp.read().decode(settings.FILE_CHARSET))
            except Exception, e:
                sys.stderr.write("Couldn't execute custom SQL for %s" % app.    __name__)
                import traceback
                traceback.print_exc()
                transaction.rollback_unless_managed()
            else:
                transaction.commit_unless_managed()
        
signals.post_syncdb.connect(load_customized_sql)

