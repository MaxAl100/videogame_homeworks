# Tarea 0: DCCorreos de Chile :school_satchel:


## Consideraciones generales :octocat:

 - El menú principal funciona correctamente, permite iniciar sesión (o fallar en caso de información erronea), crear una cuenta nueva que es luego guardada en el **archivo usuarios.csv**. Además se puede iniciar sesión como administrador y cerrar la aplicación. Cada uno de los inicios de sesiones también lleva a su correcto submenú.
 - El menú de usuario también funciona completamente, permite crear envíos nuevos y luego visualizarlos. Además se puede revisar los envios que tienen como objetivo al usuario mismo y generar reclamos nuevos. Finalmente se puede cerrar sesión con lo que se vuelve al menú principal. Al iniciar sesión nuevamente los pedidos realizados por el usuario anterior ya no son visibles para el nuevo usuario.
 - El menú del administrador funciona correctamente y la información se actualiza sin la necesidad de cerrar la aplicación, esto para usuarios y administrador.


### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú de Inicio (18pts) (18%)
##### ✅ Requisitos <Hecha completa, están todas las opciones disponibles y son utilizables\>
##### ✅ Iniciar sesión <Hecha completa, se puede iniciar sesión correctamente\>
##### ✅ Ingresar como administrador <Hecha completa, se puede ingresar como administrador con la clave correcta\>
##### ✅ Registrar usuario <Hecha completa, se puede registrar un usuario y luego iniciar sesión sin la necesidad de cerrar y volver a abrir la aplicación\>
##### ✅ Salir <Hecha completa, se puede salir del programa con una selección del menú principal\>
#### Flujo del programa (31pts) (31%) 
##### ✅ Menú de Usuario <Hecho completo, todas las funciones funcionan y se siguen los parámetros en la creación de nuevas encomiendas\>
##### ✅ Menú de Administrador <Hecho completo, todas las funcionalidades funcionan como debiesen\>
#### Entidades 15pts (15%)
##### ✅ Usuarios <Los usuarios y el administrador tienen menús separados con distintas acciones posibles\>
##### ✅ Encomiendas <Las encomiendas son creables por los usuarios siguiendo los parámetros y actualizables por el administrador/a\>
##### ✅ Reclamos <Los reclamos son creables por los usuarios y legibles por el administrador\>
#### Archivos: 15 pts (15%)
##### ✅ Manejo de Archivos <Todos los archivos son leidos y expandidos correctamente y se utiliza la librería datetime de manera correcta. El manejo de los tres archivos principales está sobre todo en el código de "cargar.py". La librería datetime fue utilizada en el código de "menus.py", en la línea 126.\>
#### General: 21 pts (21%)
##### ✅ Menús <Los tres menús son a prueba de todo tipo de errores\>
##### ✅ Parámetros <Utilizados correctamente\>
##### ✅ Módulos <El programa fue modularizado, ver en la categoría de librerias propias para más información\>
##### ✅ PEP8 <Seguido, ninguna línea sobrepasa de los 100 caracteres, aunque algunos strings largos tuvieron que ser descritos durante múltiples líneas\>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se ```puede``` crear los siguientes archivos y directorios adicionales:
1. ```usuarios.csv``` en ```la carpeta donde está el codigo principal``` pero ```no es necesario crearlo ya que mi programa lo crea en caso de no existir```
2. ```encomiendas.csv``` en ```la carpeta donde está el codigo principal``` pero ```no es necesario crearlo ya que mi programa lo crea en caso de no existir```
3. ```reclamos.csv``` en ```la carpeta donde está el codigo principal``` pero ```no es necesario crearlo ya que mi programa lo crea en caso de no existir```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```datetime```: ```now() / datetime``` - obtener el momento en que una encomienda fue hecha
2. ```os```: ```exists() / path``` - ver si un archivo existe y, si no lo hace, crearlo 

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```cargar```: Contiene a ```User```, ```Reclamo```, ```Encomienda```
2. ```parametros```: Contiene algunos parametros que son utilizados para controlar ciertos aspectos del programa
3. ```menus```: Contiene a los dos menús no principales, del usuario y administrador y los códigos para sus funciones

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. No se permiten valores negativos de peso, ya que esto es irreal. Además se permite desde 0.01, ya que hay muy pocas cosas que pesen menos y se evita peso nulo, que podría llevar a errores o problemas en el caso de un sistema más grande.
2. Inserté todos los archivos dentro de una sola carpeta, ya que en un programa de este tamaño no es necesario organizar mucho la información, pero en caso de que fuere más grande, sí sería apto crear carpetas para las informaciones (.csv) y los programas (.py)
3. Asumí que las cosas no detalladas en la tarea (como si la clave **tiene** que ser alfanumérica o si puede estar hecha **sólo** por números o **sólo** por letras) funcionan de ambas maneras, es decir, ambas opciones son válidas. 
4. Asumí que uno no se puede enviar encomiendas a sí mismo, pero en caso de que sí deba ser posible, entonces hay que comentar las líneas 75 a 83 del programa *menus.py*
5. En varias partes di la opción entre volver al menú anterior y continuar con la acción realizada ya que esto es más amigable hacia el usuario.

PD: Se nota que esto ya no es introducción a la programación ;)


-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python: este reemplaza una linea en un archivo por algo distinto y esta implementado en menus.py en la linea 239 para reemplazar el estado de una encomienda



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
