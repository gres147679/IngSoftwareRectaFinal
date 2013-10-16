import models

def borradoPlan(sender, **kwargs):
    borrada = kwargs['instance']
    if borrada.tipo == "pr":
	aBorrar = models.PlanPrepago.objects.filter(codplan=borrada)
    else:
	aBorrar = models.PlanPostpago.objects.filter(codplan=borrada)
    aBorrar.delete()