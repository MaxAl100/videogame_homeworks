# Tarea 2: DCComando Espacial :school_satchel:

## Consideraciones generales :octocat:

En general: Todas las ventanas fueron diseñadas en PQDesigner, pero las señales creadas y conectadas por código. Las ventanas se preocupan de mostrar y cambiar cosas visuales mientras que los cálculos y revisiones son realizados por los archivos de lógica.
Todas las ventanas muestran todo el contenido y en el juego lo que aparece más arriba es la mira, luego los aliens y luego los especiales. Los aliens no se superponen al aparecer y en las otras ventanas nada se superpone a otra cosa. Las ventanas están conectadas con señales en main.py.
El botón de disparo es el botón control (no importa si es el izquierdo o derecho) ya que el botón espacio clickeaba botones al apretarlo. 
Intenté comentar lo más posible el código dentro de lo posible, pero es harto código.

### Cosas implementadas y no implementadas :white_check_mark: :x:
El juego está básicamente completo. Lo que no logré hacer es que se dispare continuamente al mantener apretado la tecla de disparo. Logré hacer los bonuses del sonido de risa, de la bomba de hielo y de la estrella de la muerte.
Además implementé movimiento en 8 direcciones (apretando arriba y derecha, por ejemplo, uno se puede mover hacia arriba y la derecha) y que los puntajes estén actualizados cuando uno vuelva a la ventana de inicio.
Respecto a la modelación; en algunas partes tuve que crear varios labels con distintas imágenes porque no me funcionaba cambiar el pixmap asociado al label. Además separé la lógica de lo visual lo más posible pero puede que algunas cosas se me hayan pasado, por lo que está con la flecha verde y el círculo naranjo.

#### ✅ Ventana de Inicio: 4 pts (4%) - Hecha completa. Se emiten señales al apretar los botones como se ve en el archivo ```ventana_inicio.py```. 
#### ✅ Ventana de Ranking: 5 pts (5%) - Hecha completa y bien actualizada durante el uso de la aplicación. Se emite una señal para volver a la ventana de inicio como se ve en el archivo ```ventana_ranking.py``` y en la línea 19 de ```logica_ranking.py``` se ordenan los puntajes del archivo ```puntajes.txt```.
#### ✅ Ventana principal: 7 pts (7%) - Hecha completa. En el archivo ```logica_principal.py``` se revisan los errores enviados por una señal desde ```ventana_principal.py```. En ```ventana_principal.py``` también se abren pop-ups por cada error y se envía una señal para abrir el juego en caso de que no hayan errores.
#### ✅ Ventana de juego: 14 pts (13%) - Hecha completa y bien actualizada durante el uso de la aplicación. Esta información es actualizada via señales envaidas desde ```logica_juego.py``` al archivo ```ventana_juego.py```. Además desde esta ventana se emite una señal a la logica del juego para poder salir del juego.
#### ✅ Ventana de post-nivel: 5 pts (5%) - Hecha completa y bien actualizada durante el uso de la aplicación (la que me quedó menos bonita eso sí...). En el archivo ```ventana_postnivel.py``` se emiten señales para salir de la partida/ir al siguiente nivel.

#### Mecánicas de juego: 47 pts (45%)
##### ✅🟠 Arma <Todo lo de la arma está bien hecho excepto que no se puede mantener apretado para disparar continuamente.\>
##### ✅ Aliens y Escenario de Juego <Los aliens y el escenario del juego cambian según el mundo elegido. Los aliens aumentan su velocidad en el avance de los niveles. También se puede observar el cambio de la duración del nivel y los rebotes de los aliens con los bordes de la pantalla\>
##### ✅ Fin de Nivel <El fin del nivel es activado en cualquiera de las 3 condiciones (y el cheatcode CIA) correctamente y se limpian las labels para el siguiente nivel.\>
##### ✅ Fin del juego <El juego finaliza cuando uno pierde un nivel y no se puede ir al siguiente o se sale a través del botón salir en la ventana de juego. En ambos casos el puntaje es guardado correctamente.\>

#### Cheatcodes: 8 pts (8%)
##### ✅ Pausa <Se puede pausar correctamente el juego, ya sea con el botón o con la tecla 'p'. Se hace a través de una señal emitida desde ventana_juego en el tratamiento de teclas presionadas.\>
##### ✅ O + V+ N + I <Al usar el código se "reciben" balas infinitas al no bajar el contador de balas durante el nivel. Se hace a través de una señal emitida desde ventana_juego en el tratamiento de teclas presionadas.\>
##### ✅  C + I + A <El código CIA hace que se pase al siguiente nivel como victoria al hacer que queden 0 aliens por matar. Este código hace que la animación de terminator dog con un alien en la mano se reproduzca. Se hace a través de una señal emitida desde ventana_juego en el tratamiento de teclas presionadas.\>

#### General: 14 pts (13%)
##### ✅ Modularización <Separo el back-end del front-end y hasta separo la lógica del juego en dos documentos apartes, modularizando más.\>
##### ✅🟠 Modelación <Utilicé señales para traspasar información del backend al frontend y viceversa.\>
##### ✅ Archivos  <Trabajé con los archivos dados en el enunciado de manera correcta, sin alterar el tamaño de estos. Además el archivo puntajes.txt lo trato de buena manera para que no se produzcan errores luego del uso de la aplicación.\>
##### ✅ Parametros.py <Están incluidos todos los parámetros necesarios y son utilizados (e importados) de manera correcta.\>

#### Bonus: 10 décimas máximo
##### ✅ Risa Dog <El sonido suena correctamente en caso de victoria en una partida.\>
##### ✅ Estrella <La estrella de la muerte aparece según rng, intentando ser menos que una probabilidad definida en parámetros. En caso de que se le dispare se pierde el tiempo TIEMPO_PERDIDO y desaparece la estrella de la pantalla. En caso de que no se le de, se queda en la pantalla por TIEMPO_ESTRELLA. Sólo puede aparecer 1 vez por partida.>
##### ❌✅🟠 Disparos extra <explicacion\>
##### ✅ Bomba <La bomba de hielo aparece según rng y aparece por TIEMPO_BOMBA. Además congela a los enemigos vivos por TIEMPO_CONGELAMIENTO y si mueren caen de manera normal.\>
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```puntajes.txt``` en ```la misma carpeta donde se ubica main```
2. ```Sonidos``` en ```la misma carpeta donde se ubica main con los archivos necesarios```
3. ```Sprites``` en ```la misma carpeta donde se ubica main con los archivos necesarios```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```random()```, ```randint``` y ```uniform``` para calcular las probabilidades de los eventos especiales, las ubicaciones aleatorias dentro del nivel y los ponderadores de dificultad.
2. ```PyQt5```: `Para todo lo relacionado con las ventanas y los cambios de estados en esta (debe instalarse)
3. ```sys```: para inciar la aplicación.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases_apoyo```: Contiene a ```Nivel```, ```Alien```, ```Mira``` y ```Explosión```. La clase nivel es la princpipal de estas y se relaciona con las otras tres para hacer funcionar cada nivel.
2. ```parametros```: Hecha para contener los parámetros necesarios para correr el código y editarlos fácilmente.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El puntaje que es guardado en caso de salir en la mitad de un nivel es aquel que ha sido acumulado en niveles anteriores hasta ese punto y es válido porque me dijeron que yo decidiera como funcionara esto. 
2. Los tiempos de los bonuses se pausan al pausar el juego para que uno no pueda esquivar la estrella de la muerte pausando el juego.
3. La tecla control se va a utilizar para disparar en vez de espacio, como ya mencioné anteriormente.
4. Al matar a la pareja de aliens estos desaparecen y aparecen dos nuevos sin esperar a que estos otros dos bajen completamente para que el jugador no pierda tiempo. Esto fue explicado en el issue 183.

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://stackoverflow.com/questions/7176951/how-to-get-multiple-key-presses-in-single-event: este permite tratar con múltiples teclas al mismo tiempo y está implementado en el archivo <ventana_juego.py> en las líneas <88 a 142> y hace que uno se pueda mover en 8 direcciones e identificar si todas las teclas de los codigos cia y ovni estén siendo apretadas.
2. https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/: permite crear pop-ups, está implementado en <ventana_principal.py> y crea pop-ups por cada error que uno haya hecho al intentar jugar en un nivel.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
