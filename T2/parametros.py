import os
from random import uniform

# Valores numéricos
VELOCIDAD_ALIEN = [2, 1]
TIEMPO_TERMINATOR_DOG = 2.5  # en segundos
DURACION_NIVEL_INICIAL = 120  # en segundos
const1 = uniform(0.9, 1)
PONDERADOR_TUTORIAL = const1
const2 = uniform(0.8, 0.9)
PONDERADOR_ENTRENAMIENTO = const2
const3 = uniform(0.7, 0.8)
PONDERADOR_INVASION = const3

# Info pantalla
ANCHO_JUEGO = 720
ALTO_JUEGO = 480

# Info alien
WIDTH_ALIEN = 60
HEIGHT_ALIEN = 60
MIN_X = 0
MAX_X = 660
MIN_Y = 0
MAX_Y = 420

# Info mira
WIDTH_MIRA = 120
HEIGHT_MIRA = 80
MIN_X_MIRA = -50
MAX_X_MIRA = 670
MIN_Y_MIRA = -50
MAX_Y_MIRA = 430
VELOCIDAD_MIRA = 8


# Teclas
TECLA_ARRIBA = "w"
TECLA_IZQUIERDA = "a"
TECLA_ABAJO = "s"
TECLA_DERECHA = "d"

# Rutas para el programa

# Rutas de archivos .ui

RUTA_UI_VENTANA_INICIO = os.path.join(
    "frontend", "ventanas_designer", "ventana_inicio.ui")
RUTA_UI_VENTANA_RANKING = os.path.join(
    "frontend", "ventanas_designer", "ventana_ranking.ui")
RUTA_UI_VENTANA_PRINCIPAL = os.path.join(
    "frontend", "ventanas_designer", "ventana_principal.ui")
RUTA_UI_VENTANA_JUEGO = os.path.join(
    "frontend", "ventanas_designer", "ventana_juego.ui")
RUTA_UI_VENTANA_POSTNIVEL = os.path.join(
    "frontend", "ventanas_designer", "ventana_postnivel.ui")


# Rutas imágenes

RUTA_LOGO = os.path.join("Sprites", "Logo", "Logo.png")

RUTA_ALIEN_1 = os.path.join("Sprites", "Aliens", "Alien1.png")
RUTA_ALIEN_1_MUERTO = os.path.join("Sprites", "Aliens", "Alien1_dead.png")
RUTA_ALIEN_2 = os.path.join("Sprites", "Aliens", "Alien2.png")
RUTA_ALIEN_2_MUERTO = os.path.join("Sprites", "Aliens", "Alien2_dead.png")
RUTA_ALIEN_3 = os.path.join("Sprites", "Aliens", "Alien3.png")
RUTA_ALIEN_3_MUERTO = os.path.join("Sprites", "Aliens", "Alien3_dead.png")

RUTA_MIRA_NORMAL = os.path.join(
    "Sprites", "Elementos juego", "Disparador_negro.png")
RUTA_MIRA_DISPARO = os.path.join(
    "Sprites", "Elementos juego", "Disparador_rojo.png")

RUTA_EXPLOSION_1 = os.path.join("Sprites", "Elementos juego", "Disparo_f1.png")
RUTA_EXPLOSION_2 = os.path.join("Sprites", "Elementos juego", "Disparo_f2.png")
RUTA_EXPLOSION_3 = os.path.join("Sprites", "Elementos juego", "Disparo_f3.png")

RUTA_FONDO_1 = os.path.join("Sprites", "Fondos", "Luna.png")
RUTA_FONDO_2 = os.path.join("Sprites", "Fondos", "Jupiter.png")
RUTA_FONDO_3 = os.path.join("Sprites", "Fondos", "Galaxia.png")

RUTA_TERMDOG_NORMAL = os.path.join("Sprites", "Terminator-Dog", "Dog1.png")
RUTA_TDOG_ALIEN1 = os.path.join(
    "Sprites", "Terminator-Dog", "Perro_y_alien1.png")
RUTA_TDOG_ALIEN2 = os.path.join(
    "Sprites", "Terminator-Dog", "Perro_y_alien2.png")
RUTA_TDOG_ALIEN3 = os.path.join(
    "Sprites", "Terminator-Dog", "Perro_y_alien3.png")

# Rutas sonidos
RUTA_SONIDO_DISPARO = os.path.join("Sonidos", "disparo.wav")
RUTA_SONIDO_RISA = os.path.join("Sonidos", "risa_robotica.wav")


# Rutas otros

RUTA_PUNTAJE = os.path.join("puntajes.txt")
TECLA_PAUSA = "p"
TIEMPO_ESTRELLA = 10  # en segundos
TIEMPO_PERDIDO = 18  # en segundos
# esto significa 0.2% de probabilidad en cada momento que se actualiza la pantalla
PROBABILIDAD_ESTRELLA = 0.002
TIEMPO_BOMBA = 5  # en segundos
TIEMPO_CONGELAMIENTO = 8  # en segundos
PROBABILIDAD_BOMBA = 0.0005  # lo mismo que en PROBABILIDAD_ESTRELLA
