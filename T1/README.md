# Tarea 1: DCCasino

## Consideraciones generales :octocat:

El codigo permite utilizar todas las funcionalidades del casino e insertar algún valor inválido no evita que el programa siga funcionando.


### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 38 pts (28%)
##### ✅ Diagrama <En el diagrama incluyo todas las relaciones entre las clases y las abstractas están detalladas al estar en cursiva\>
##### ✅ Definición de clases, atributos, métodos y properties <La modelación de todas las clases están en el archivo "clases.py" en la carpeta "codigo"\>
##### ✅ Relaciones entre clases <Utilicé clases y métodos abstractos cuando fue necesario, además de utilizar la agregación y composición correctamente, lo que también está visible en el archivo "clases.py"\>
#### Simulaciones: 10 pts (7%)
##### ✅ Crear partida <Múltiples partidas pueden ser creadas correctamente, instanciando las clases a través de los tres archivos .csv en la carpeta "registro". En el código esto es parte del archivo "cargar.py", también dentro de la carpeta "codigo"\>
#### Acciones: 35 pts (26%)
##### ✅ Jugador <Las condiciones para apostar están configuradas correctamente y esta apuesta está dentro del archivo "main.py", comienza en la línea 57. Además los distintos tipos de jugador están en el archivo "clases.py" como clases separadas\>
##### ✅ Juego <Las características del jugador cambian según el resultado de la partida y este resultado es calculado en la clase casino, utilizando las distintas probabilidades calculadas en jugador(l.115) y juego(l.205) en el archivo "clases.py"\>
##### ✅ Bebestible <Los bebestibles son comprables y surten efecto inmediato sobre las características del jugador, estos cambios están programados en cada subclase, dependiendo del tipo que sea, en el archivo "clases.py". Comienza en la línea 218.\>
##### ✅ Casino <El evento especial tiene cierta probabilidad de suceder y, cuando lo hace, el jugador recibe una bebida aleatoria. Además se le avisa después de cada partida si este evento sucede o no.\>
#### Consola: 41 pts (30%)
##### ✅ Menú de Inicio <Todo completo\>
##### ✅ Opciones de jugador <Todo completo\>
##### ✅ Menú principal <Todo completo\>
##### ✅ Opciones de juegos <Todos los juegos son seleccionables y la probabilidad de victoria es calculada correctamente en la ubicación ya mencionada en la categoría "Juego". Además cambian las características del jugador y se vuelve al menú principal.\>
##### ✅ Carta de bebestibles <Todo completo\>
##### ✅ Ver estado del Jugador <Todo completo\>
##### ✅ Robustez <A mi conocer no hay ningún error dentro del programa\>
#### Manejo de archivos: 13 pts (9%)
##### ✅ Archivos CSV  <El manejo de archivos está hecho en "cargar.py" y me aseguro de que se trate bien el path de los archivos utilizando os\>
##### ✅ parametros.py <Cree el archivo parametros.py y cree todas las constantes necesarias\>
#### Bonus: 3 décimas máximo
##### ✅ Ver Show <Se puede ver un show y se muestran los cambios de la información del jugador\>
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```jugadores.csv``` en ```registro```
2. ```juegos.csv``` en ```registro```
3. ```bebestibles.csv``` en ```registro```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```beautifultable```: ```Beautifultable()``` (debe instalarse)
2. ```os```: ```join() / path```
3. ```sys```: ```exit()``` 
4. ```random```: ```random()```
5. ```abc```: ```@abstractmethod``` y ```ABC```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases.py```: Contiene a todas las clases utilizadas en este programa
2. ```cargar.py```: Contiene al código necesario para cargar los archivos y transformarlos en información útil para el programa
3. ```parametros.py```: Contiene a los parametros de apoyo para las otras funciones

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. No es necesario editar los archivos ya que un issue así lo dijo.
2. Los parámetros no tienen que estar balanceados para la experiencia ya que los ayudantes serán los que los cambiarán para testearlos.
3. La primera línea de los archivos con la información, aunque estén desordenados, siempre estarán escritos de la misma manera, es decir, todo con minúscula, sin acentos y sólo con comas dividiendo las distintas columnas de información ya que así estaban los ejemplos del foro y se volvería demasiado complicado si hay que revisar todas las opciones.
4. Si uno escoge un jugador que ya tiene suficiente dinero para pagar la deuda, esto se hace instantáneamente y uno no juega ningún juego.
5. El valor de random() tiene que ser menor que el valor de la función para que el jugador gane, ya que cosas positivas, como si el juego es el favorito del jugador, acercan el valor hacia 1, mientras que cosas "negativas", como el valor de la apuesta o la esperanza del juego, disminuyen el valor de esta función.
6. Asumí que la suerte de principante sólo suceda una vez por juego significa por el nombre de este, ya que jugar dos blackjacks distintos (en caso de que un casino tenga dos distintos) solo debiera recibir la suerte de principiante una sóla vez, ya que el juego es el mismo. Por esto igual asumo que los nombres de dos juegos iguales van a estar escritos completamente iguales.

-------


## Referencias de código externo :book:

Para realizar mi tarea no saqué código de otras fuentes.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
