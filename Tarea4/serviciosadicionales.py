##***************************************************************************
##*************************** PATRON DECORADOR ******************************
##***************************************************************************

##*** Librerias a utilizar **************************************************

from vendibles import Vendible, Producto
#from afiliaciones import Afiliaciones

## Decorador Abstracto ##

class ServiciosAdicionales(Producto):
    def __init__(self):
        self._desc = "Clase Abstracta de Servicios"
        self.codigo = 0;
        self.costo = 0;

## Decoraciones ##

## Clase que anade el servicio adicional mensajes de texto a un producto
class MensajesDeTexto(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self.codigo = 4001;
        self.costo = 100;
        self.producto = producto;
        
        # Se crea la contratacion en la base de datos
        #afiliar = Afiliaciones(self.producto.get_id(),self.codigo);
        #afiliar.CrearContratacion();
        
        self._desc = self.producto.get_desc() + """ + Servicio de Mensajes \
de Texto """;
        self._costoServicios = self.costo + self.producto.get_costoServicios()
        
##
## Clase que anade el servicio adicional segundos a MOCEL, a un producto
##
class SegundosMOCEL(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self.codigo = 4002;
        self.costo = 150;
        self.producto = producto;
        
        # Se crea la contratacion en la base de datos
        #afiliar = Afiliaciones(self.producto.get_id(),self.codigo);
        #afiliar.CrearContratacion();
        self._desc = self.producto.get_desc() + """ + Servicio de Segundos \
adicionales a MOCEL""";
        self._costoServicios = self.costo + self.producto.get_costoServicios()
        
##
## Clase que anade el servicio adicional segundos a otras operadoras, a 
## un producto
##
class SegundosOtrasOperadoras(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self.codigo = 4003;
        self.costo = 200;
        self.producto = producto;
        
        # Se crea la contratacion en la base de datos
        #afiliar = Afiliaciones(self.producto.get_id(),self.codigo);
        #afiliar.CrearContratacion();
        
        self._desc = self.producto.get_desc() + """ + Servicio de Segundos \
adicionales a otras operadoras""";
        self._costoServicios = self.costo + self.producto.get_costoServicios()


##
## Clase que anade el servicio adicional megabytes de navegacion a un producto
##
class MegabytesDeNavegacion(ServiciosAdicionales):
    
    def __init__(self, producto):
        self._id = producto.get_id()
        self.codigo = 4004;
        self.costo = 150;
        self.producto = producto;
        
        # Se crea la contratacion en la base de datos
        #afiliar = Afiliaciones(self.producto.get_id(),self.codigo);
        #afiliar.CrearContratacion();
        
        self._desc = self.producto.get_desc() + """ + Servicio de Megabytes \
de Navegacion""";
        self._costoServicios = self.costo + self.producto.get_costoServicios()




 ####################### TEST CODE ##########################

p = Producto(123);
print p.get_desc();
print p.get_costoServicios()
p = SegundosMOCEL(SegundosOtrasOperadoras(MensajesDeTexto(Producto(123))));
print p.get_desc()
print p.get_costoServicios()

#q = Producto(1234)
#print q.get_desc()
#q = MensajesDeTexto(q)
#print q.get_desc()
#q = SegundosOtrasOperadoras(q)
#print q.get_desc()
