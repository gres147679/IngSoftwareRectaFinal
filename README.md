****************************************************************************************************
*                                                                                                  *
*                                        ARCHIVO README                                            *
*                                                                                                  *
*                                                                                                  *
*                                                                                                  *
*   Desarrollado por: Gamar Azuaje       Rosangelis Garcia                                         *
*                     Reinaldo Verdugo   Jose L. Jim�nez                                           *
*                     Gustavo El Khoury  Rebeca Machado                                            *
*                     Leopoldo Pimentel                                                            *
*                                                                                                  *
*                                                                                                  *
*                                          SERVISOFT                                               *
*                                                                                                  *
****************************************************************************************************

DISCLAIMER
==========
Este archivo describe las instrucciones, consideraciones y justificaciones del desarrollo del 
sistema planteado en la tarea 5 del curso de Ingenier�a de Software. El sistema es de nuestra 
autor�a y las conceptualizaciones del sistema (dise�o) se encuentran plasmadas en el informe 
entregado. 

Las plataformas utilizadas fueron Django y PostgreSQL, siendo esta �ltima de vital importancia en 
para el correcto funcionamiento del sistema. El uso de otro lenguaje/backend para la base de datos 
acabar� en un completo desastre.


INSTRUCCIONES
=============

1) Crear una base de datos, si no existe una que se desee utilizar para el sistema.

2) Introducir las credenciales de la base de datos en settings.py del proyecto.

3) Ejecutar 
      $ python manage.py syncdb 
   una vez.
   
4) Ejecutar 
      $ python manage.py runserver 8080
   El puerto 8080 puede ser sustituido por el de su preferencia.
   
   
5) Utilizar la interfaz de administrador (http://127.0.0.1:8000/admin/WebAccess) para ingresar tantos 
usuarios del sistema, clientes, productos, servicios, planes y afiliaciones como se desee. Tambien
puede accesar a las opciones de administrador referentes a la facturacion desde la barra lateral

6) Utilizar la interfaz de control regular (http://127.0.0.1:8000) para acceder a las funciones de 
los clientes


CONSIDERACIONES
===============

A) Para la inserci�n de los triggers de integridad de la base de datos utilizada en las tareas 
anteriores, se presentaron problemas que obedecen al siguiente ticket de error presente en Django:

https://code.djangoproject.com/ticket/3214

La forma m�s sana de corregir el problema consiste en crear un manejador de se�ales que capture la 
se�al de sincronizaci�n de la DB, y que luego inserte los triggers, seg�n se explica aqu�:
http://djangosnippets.org/snippets/1338/

Desafortunadamente este mecanismo no distingue si la operaci�n de inserci�n de triggers ya fue 
realizada o no. En conclusi�n, al ejecutar syncdb m�s de una vez se observan errores que indican 
que ya los triggers existen. Una soluci�n posible (aun asi, dif�cil de llevar a cabo en tan poco 
tiempo) es transformar los triggers de la base de datos en funciones save de django. Esto se ha
logrado en dos de los triggers de integridad: crear una categor�a de Plan Prepago o Postpago
al insertar un plan, y crear paquetes de servicios adicionales autom�ticamente al insertar un servicio.
Pedimos disculpas por este inconveniente que se escapa de nuestras manos.

B) En esta oportunidad, debido a que hab�an bastantes puntos (casos de uso) a cubrir para la 
entrega, se decidi� dividir el trabajo en �reas.

Informe, documentaci�n y diagramas: Leopoldo Pimentel y Reinaldo Verdugo.
Traduccion de base de datos: Rebeca Machado y Gustavo El Khoury
Interfaz gr�fica: Reinaldo Verdugo
Refactorizaciones: Rebeca Machado
Implementaci�n: Gustavo El Khoury, Gamar Azuaje, Rosangelis Garcia, Jose Luis Jimenez

Las parejas iniciales est�n al inicio del archivo.

C) En el c�digo de los escenarios de prueba, se encuentra un grupo de pruebas comentadas. Al momento de
realizarlas, el equipo de desarrollo not� que exist�a un problema cuando se agregaban consumos desde el
escenario de pruebas de Django, lo cual incide en las pruebas de facturaci�n. Sin embargo, al simular
estos escenarios desde la interfaz de administrador, no se notaron problemas algunos.

D) Al correr los escenarios de prueba con manage.py test WebAccess, se observar� un error referente a
triggers en la creaci�n de la base de datos temporal. Esto no influye en la ejecuci�n, y ocurre
pues Django intenta insertar el script custom de sql DOS veces a la base de datos, lo cual provoca
conflictos sobre triggers que ya existen


    Copyright (C) 2014  Gustavo El Khoury <gustavoelkhoury@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    The full GPLv2 License can be fount at the root of the repo, in the 
    LICENSE file.
