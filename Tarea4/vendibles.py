

class Vendible:  
    #Clase Abstracta
    def __init__(self):  
        self._id = "Identificador abstracto"  
        self._desc = "Descripcion abstracta"
   
    def get_id(self):  
        return self._id 

    def get_desc(self):  
        return self._desc  
    
class Producto(Vendible):  
    #Clase Concreta
    def __init__(self,id):  
        self._id = id  
        self._desc = "Producto: " + str(self._id)
        
        
 ####################### TEST CODE ##########################
 
 
# Ejemplo de una clase concreta. Cuando la utilizen pidan la siere con validarSerie en productos.py
# Usen el id para agregarle el paquete al producto a traves de la BD.
# p = Producto(123);
# print p.get_desc()
 