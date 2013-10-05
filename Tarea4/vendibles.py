

class Vendible:  
    #Clase Abstracta
    def __init__(self):  
        self._id = "Identificador abstracto"  
        self._desc = "Descripcion abstracta"
        self._costoServicios = 0
        
    def get_costoServicios(self):
        return self._costoServicios
   
    def get_id(self):  
        return self._id 

    def get_desc(self):  
        return self._desc  
    
class Producto(Vendible):  
    #Clase Concreta
    def __init__(self,id):  
        self._id = id  
        self._desc = "Producto: " + str(self._id)
        self._costoServicios = 0
        
    def __str__(self):
        return self._desc + "\ncostoServicios: " + str(self._costoServicios)
        
        
 ####################### TEST CODE ##########################
 
 
# Ejemplo de una clase concreta. Cuando la utilizen pidan la siere con validarSerie en productos.py
# Usen el id para agregarle el paquete al producto a traves de la BD.
#p = Producto(123);
#print p.get_desc()
 