# Tarea 3: DCCasillas :school_satchel:

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

Si uno jugara sólo una partida sin que nadie se desconecte sólo se encontraría con un error que es que al comienzo se visualizan las piezas de manera extraña. Pero además de eso no hay problemas. Todos los logs funcionan correctamente y las funcionalidades están bien separadas. El mensaje está bien encriptado y codificado y se decodifica y desencripta correctamente. No hay ninguna comunicación entre usuarios y realicé el bonus del rebote, por lo que cualquier lanzamiento de dado va a realizar que la pieza se mueva (aunque no lo parezca cuando sale 2 y la ficha está a uno de distancia de la meta).

### Cosas implementadas y no implementadas :white_check_mark: :x:
Se puede jugar una partida bien y si los jugadores se desconectan en cualquier ventana menos la del juego el programa funciona bien. Se pueden jugar varias partidas una después de otra mientras los jugadores sean los mismos en la primera partida que en las siguientes (nadie se conecta o desconecta). Si un jugador se desconecta en la mitad de la partida, lo que sucede es que otro jugador va a empezar a lanzar sus dados por este.

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Networking: 23 pts (18%)
##### ✅ Protocolo <Cuando inicio los sockets en servidor.py y cliente.py lo hago con el protocolo correcto\>
##### ✅ Correcto uso de sockets <Además los instancio de manera correcta y, al menos a mi conocer, las aplicaciones pueden trabajar concurrentemente sin bloquearse por un socket.\>
##### ✅🟠 Conexión <La conexión se mantiene bien, pero hay veces que se me crashea alguna aplicación, pero creo que es por mi computador, que no es de la mejor calidad, aunque no estoy seguro. Además, respecto a las desconexiones: Aguanto las desconexiones dentro de las ventanas de inicio, espera y postjuego, pero no en el juego. O sea un jugador sí se puede desconectar, pero lo que va a suceder es que otro jugador va a empezar a lanzar dados por este en vez de irse completamente de la partida.\>
##### ✅ Manejo de clientes <Se pueden conectar múltiples clientes sin problemas.\>
#### Arquitectura Cliente - Servidor: 31 pts (25%)
##### ✅ Roles <Separo al servidor de los clientes a través de carpetas separadas. Sus responsabilidades son consistentes con el enunciado.\>
##### ✅🟠 Consistencia <La información se mantiene coordinada, pero no logré implementar locks, ya que cuando lo intenté me falló el programa.\>
##### ✅ Logs <He implementado todos los logs.\>
#### Manejo de Bytes: 26 pts (21%)
##### ✅ Codificación <Codifico correctamente la información. Esto en servidor y en cliente.\>
##### ✅ Decodificación <Decodifico correctamente la información. Esto en servidor y en cliente.\>
##### ✅ Encriptación <Encripto como se pide en el enunciado. Esto en servidor y en cliente.\>
##### ✅ Desencriptación <Desencripto la información utilizando que en impares len(A)>len(B) y en pares que existe un loop que se repite cada 6 respecto a si len(A) = len(B) o len(A) = len(B) + 2. Esto en servidor y en cliente.\>
##### ✅ Integración <Utilizo el protocolo correcto para enviar mensajes.\>
#### Interfaz: 23 pts (18%)
##### ✅ Ventana inicio <La ventana de inicio está completa y se le avisa al usuario correctamente en caso de un error.\>
##### ✅ Sala de Espera <Esta completa y solo le permite al administrador empezar la partida si hay al menos MIN_JUGADORES y comienza al tiro cuando la sala se llena (MAXIMO_JUGADORES).\>
##### ✅🟠 Sala de juego <Se visualiza correctamente y se actualiza para todos los usuarios. Al comienzo de la partida (antes del primer lanzamiento del dado) las fichas se ven extrañas, pero se arregla luego del primer lanzamiento. Los lanzamientos de dado funcionan correctamente y la partida finaliza cuando debe hacerlo.\>
##### ✅🟠 Ventana final <Indica el ganador correctamente y muestra los datos de la partida. Pero al ganador no le aparecen dos fichas en la meta... :|\>
#### Reglas de DCCasillas: 18 pts (14%)
##### ✅ Inicio del juego <Los turnos se asignan según el orden de llegada ya que se organizan los jugadores en una lista y se va avanzando en esta para que lancen sus dados. Los colores se asignan aleatoriamente.\>
##### ✅ Ronda <Todas las reglas están completas. Tengo el rebote implementado, por lo que no tiene que ser exactamente igual para avanzar.\>
##### ✅ Termino del juego <Se asigna el ganador correctamente.\>
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON) <Tengo los parámetros en formato json, separados con uno para los clientes y otro para el servidor.\>
#### Bonus: 5 décimas máximo
##### ❌ Cheatcode <No lo pienso implementar por dos razones. Primero que todo me parece moralmente incorrecto ocupar cheats en un juego multijugador, aún más cuando es competitivo (¡Queremos ganar el tesoro!). Además el bonus de los turnos con tiempo menciona que BigCat quiere que el juego termine de manera pronta, pero con este cheatcode perfectamente puede durar para siempre, echando a perder el uso de los turnos con tiempo.\>
##### ❌ Turnos con tiempo <No lo he realizado por temas de tiempo y que tengo que ver cosas de otros ramos.\>
##### ✅ Rebote <Implementado correctamente.\>

## Ejecución :computer:
Hay dos módulos principales de la tarea, uno en la carpeta Servidor, otro en la carpeta Cliente. Ambos se llaman ```main.py``` y se debe ejecutar una vez el servidor antes de ejecutar un cliente.
No es necesario crear archivos adicionales para este programa.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket``` y ```json```: Para la comunicación entre servidor y cliente.
2. ```Thread```: Para escuchar a los clientes constantemente y actualizar la ventana de espera.
3. ```PyQt5```: Para conectar botones y cambiar ciertas características de cosas visuales.
4. ```os```: ```path.join``` Para unir la dirección de la información y poder cambiar imágenes, etc... correctamente.
5. ```sys```: Para iniciar la aplicación para los usuarios y el servidor
6. ```abc```: Para crear una clase abstracta de Jugador tal que los jugadores de cada color tengan ciertas características
7. ```random```: Para escoger un color aleatorio y lanzar el dado "aleatoriamente"

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases_apoyo```: Contiene a ```Tablero```, ```Pieza```, y las clases de todos los jugadores
2. ```utils```: Hecha para tratar con los archivos parametros.json

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. No es necesario escribir que una ficha rebotó, ya que se puede ver a través del cambio de su posición.
2. <Descripción/consideración 2 y justificación del por qué es válido/a>
3. ...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/: permite crear pop-ups, está implementado en <ventana_inicio.py> y crea en caso de que el nombre de usuario no cumpla con las condiciones necesarias. [Es el mismo que utilicé para la Tarea 2]
