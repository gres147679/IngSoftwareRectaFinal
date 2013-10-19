import models

def borradoPlan(sender, **kwargs):
    borrada = kwargs['instance']
    if borrada.tipo == "pr":
	aBorrar = models.PlanPrepago.objects.filter(codplan=borrada)
    else:
	aBorrar = models.PlanPostpago.objects.filter(codplan=borrada)
    aBorrar.delete()
    
def insertadoServicio(sender, **kwargs):
    
    insertado = kwargs['instance']
    print insertado
    if insertado.id is not None:
	nuevoPaq = models.Paquete(codpaq=insertado.codserv,nombrepaq=insertado.nombreserv + ' Paquete',precio=insertado.costo)
	nuevoPaq.save()
	nuevoContiene = models.Contiene(codpaq=nuevoPaq,codserv=insertado,cantidad=1)
	nuevoContiene.save()
	
def borradoServicio(sender, **kwargs):
    borrado = kwargs['instance']
    if borrado.id is not None:
	contieneBorrar = models.Contiene.objects.all().filter(codpaq=borrado.codserv)
	contieneBorrar.delete()
	paqBorrar = models.Paquete.objects.all().filter(codpaq=borrado.codserv)
	paqBorrar.delete()
	