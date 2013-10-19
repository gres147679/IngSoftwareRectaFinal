****************************************************************************************************
*                                                                                                  *
*                                        ARCHIVO README                                            *
*                                                                                                  *
*                                                                                                  *
*                                                                                                  *
*   Desarrollado por: Gamar Azuaje       Rosangelis Garcia                                         *
*                     Reinaldo Verdugo   Jose L. Jiménez                                           *
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
sistema planteado en la tarea 5 del curso de Ingeniería de Software. El sistema es de nuestra 
autoría y las conceptualizaciones del sistema (diseño) se encuentran plasmadas en el informe 
entregado. 

Las plataformas utilizadas fueron Django y PostgreSQL, siendo esta última de vital importancia en 
para el correcto funcionamiento del sistema. El uso de otro lenguaje/backend para la base de datos 
acabará en un completo desastre.


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

A) Para la inserción de los triggers de integridad de la base de datos utilizada en las tareas 
anteriores, se presentaron problemas que obedecen al siguiente ticket de error presente en Django:

https://code.djangoproject.com/ticket/3214

La forma más sana de corregir el problema consiste en crear un manejador de señales que capture la 
señal de sincronización de la DB, y que luego inserte los triggers, según se explica aquí:
http://djangosnippets.org/snippets/1338/

Desafortunadamente este mecanismo no distingue si la operación de inserción de triggers ya fue 
realizada o no. En conclusión, al ejecutar syncdb más de una vez se observan errores que indican 
que ya los triggers existen. Una solución posible (aun asi, difícil de llevar a cabo en tan poco 
tiempo) es transformar los triggers de la base de datos en funciones save de django. Esto se ha
logrado en dos de los triggers de integridad: crear una categoría de Plan Prepago o Postpago
al insertar un plan, y crear paquetes de servicios adicionales automáticamente al insertar un servicio.
Pedimos disculpas por este inconveniente que se escapa de nuestras manos.

B) En esta oportunidad, debido a que habían bastantes puntos (casos de uso) a cubrir para la 
entrega, se decidió dividir el trabajo en áreas.

Informe, documentación y diagramas: Leopoldo Pimentel y Reinaldo Verdugo.
Traduccion de base de datos: Rebeca Machado y Gustavo El Khoury
Interfaz gráfica: Reinaldo Verdugo
Refactorizaciones: Rebeca Machado
Implementación: Gustavo El Khoury, Gamar Azuaje, Rosangelis Garcia, Jose Luis Jimenez

Las parejas iniciales están al inicio del archivo.

C) En el código de los escenarios de prueba, se encuentra un grupo de pruebas comentadas. Al momento de
realizarlas, el equipo de desarrollo notó que existía un problema cuando se agregaban consumos desde el
escenario de pruebas de Django, lo cual incide en las pruebas de facturación. Sin embargo, al simular
estos escenarios desde la interfaz de administrador, no se notaron problemas algunos.

D) Al correr los escenarios de prueba con manage.py test WebAccess, se observará un error referente a
triggers en la creación de la base de datos temporal. Esto no influye en la ejecución, y ocurre
pues Django intenta insertar el script custom de sql DOS veces a la base de datos, lo cual provoca
conflictos sobre triggers que ya existen
