# Clase cliente.py
#!/usr/bin/env python
#!/usr/bin/py
# -*- coding: utf-8 -*-

import sys

class cliente:
    
    #
    # Se inicializa la clase cliente
    #
    def __init__(self, idCl, nombreCl, dirCl):
        self.id = idCl
        self.nombre = nombreCl
        self.dir = dirCl

    #
    # Guarda los datos del cliente en la variable writeRow
    #
    def __str__(self):
        writeRow = 'Cedula: ' + str(self.id)
        writeRow += '\nNombre: ' + self.nombre
        writeRow += '\nDireccion: ' + self.dir
        
        return writeRow
    
    
#END cliente.py