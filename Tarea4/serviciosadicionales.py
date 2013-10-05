##***************************************************************************
##*************************** PATRON DECORADOR ******************************
##***************************************************************************

##*** Librerias a utilizar **************************************************

from vendibles import Vendible, Producto

## Decorador Abstracto ##

class ServiciosAdicionales(Producto):
    def __init__(self):
        self._desc = "Clase Abstracta de Servicios"
        self._codigo = 0;
        self._costo = 0;

    def get_codigo(self):
        return self._codigo
## Decoraciones ##

## Clase que anade el servicio adicional mensajes de texto a un producto
class MensajesDeTexto(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self._codigo = 4001;
        self._costo = 100;
        self.producto = producto;
                
        self._desc = self.producto.get_desc() + """ + Servicio de Mensajes \
de Texto """;
        self._costoServicios = self._costo + self.producto.get_costoServicios()
        
##
## Clase que anade el servicio adicional segundos a MOCEL, a un producto
##
class SegundosMOCEL(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self._codigo = 4002;
        self._costo = 150;
        self.producto = producto;

        self._desc = self.producto.get_desc() + """ + Servicio de Segundos \
adicionales a MOCEL""";
        self._costoServicios = self._costo + self.producto.get_costoServicios()
        
##
## Clase que anade el servicio adicional segundos a otras operadoras, a 
## un producto
##
class SegundosOtrasOperadoras(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self._codigo = 4003;
        self._costo = 200;
        self.producto = producto;
        
        self._desc = self.producto.get_desc() + """ + Servicio de Segundos \
adicionales a otras operadoras""";
        self._costoServicios = self._costo + self.producto.get_costoServicios()


##
## Clase que anade el servicio adicional megabytes de navegacion a un producto
##
class MegabytesDeNavegacion(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self._codigo = 4004;
        self._costo = 150;
        self.producto = producto;
        
        self._desc = self.producto.get_desc() + """ + Servicio de Megabytes \
de Navegacion""";
        self._costoServicios = self._costo + self.producto.get_costoServicios()




 ####################### TEST CODE ##########################

#q = Producto(1234)
#print q.get_desc()
#q = MensajesDeTexto(q)
#print q.get_desc()
#q = SegundosOtrasOperadoras(q)
#print q.get_desc()
