#!/usr/bin/env python
#!/usr/bin/py
# -*- coding: utf-8 -*-


# Obtiene la tabulacion del prompt
def tabPrompt(prompt):
    return " "*(len(prompt) -len(prompt.lstrip()))

#Lee la entrada hasta que sea un entero positivo.
def validarNumero(prompt):
    while True:
        arg = raw_input(prompt)
        try:
            x = int(arg)
        except ValueError:
            print tabPrompt(prompt) + "ERROR: Debe ser un numero."
        else:
            #Verifica que sea un entero positivo.
            if (x <= 0):
                print tabPrompt(prompt) + "ERROR: Debe ser un numero positivo."
            else:
                return str(x)

#Lee la entrada hasta que tenga al menos un caracter.
def validarInput(prompt):
    while True:
        arg = raw_input(prompt)
        #Verifica que sea distinto de una cadena vacia
        if (arg == ""):
            print tabPrompt(prompt) + "ERROR: Entrada no valida."
            continue
        return arg 
        