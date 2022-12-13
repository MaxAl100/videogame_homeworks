from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect, QUrl
from random import randint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

import parametros as p


# clase nivel para ir actualizando las caracteristicas de los aliens y el tiempo

class Nivel(QObject):

    def __init__(self, mundo, num, tiempo):
        super().__init__()
        self.num = num
        self.mundo = mundo
        self.aliens_por_matar = 2*num
        self.aliens_matados = 0
        self.balas = self.aliens_por_matar * 2
        self.balas_infinitas = False
        self.tamaño = []
        self.tamaño.append(p.ANCHO_JUEGO)
        self.tamaño.append(p.ALTO_JUEGO)
        self.finalizado = False
        self.tiempo = tiempo
        self.generar_mira()
        self.generar_aliens()
        self.actualizar_datos(num)
        self.instanciar_timer(self.tiempo)

    # revisa el mundo y nivel dado para actualizar los datos
    def actualizar_datos(self, veces):
        if self.mundo == 0:
            self.dificultad = p.PONDERADOR_TUTORIAL
        elif self.mundo == 1:
            self.dificultad = p.PONDERADOR_ENTRENAMIENTO
        else:
            self.dificultad = p.PONDERADOR_INVASION
        for i in range(veces):
            self.tiempo = self.tiempo * self.dificultad

    # crea el timer principal del juego
    def instanciar_timer(self, tiempo):
        self.timer_juego = QTimer()
        self.timer_juego.setInterval(tiempo)
        self.timer_juego.timeout.connect(self.terminar_juego)
        self.timer_juego.setSingleShot(True)
        self.timer_juego.start()

    # crea la mira
    def generar_mira(self):
        pos_mira = QRect(310, 190, 100, 100)
        self.mira = Mira(pos_mira)
    # crea los aliens

    def generar_aliens(self):
        ubic_1 = [randint(0, p.MAX_X), randint(0, p.MAX_Y)]
        ubic_2 = [randint(0, p.MAX_X), randint(0, p.MAX_Y)]
        # asegurarse de que los dos aliens no se sobrepongan
        while ubic_1[0] < ubic_2[0] < ubic_1[0] + 80 and ubic_1[1] < ubic_2[1] < ubic_1[1] + 80:
            ubic_2 = [randint(0, p.MAX_X), randint(0, p.MAX_Y)]
        pos_alien1 = QRect(ubic_1[0], ubic_1[1], 80, 80)
        pos_alien2 = QRect(
            randint(0, p.MAX_X), randint(0, p.MAX_Y), 80, 80)
        print(f"aumentar velocidad {self.num} veces")
        self.alien1 = Alien(pos_alien1, self.mundo)
        self.alien1.aumentar_velocidad(int(self.num))
        self.alien2 = Alien(pos_alien2, self.mundo)
        self.alien2.aumentar_velocidad(int(self.num))

    # se corre cada cierto tiempo para actualizar distintas cosas en la pantalla
    def avanzar_partida(self):
        if self.finalizado is False:
            self.alien1.mover()
            self.alien2.mover()

    def terminar_juego(self):
        self.finalizado = True

    # calcula el puntaje al terminar el nivel
    def calculo_puntaje(self):
        parte = (30 * self.timer_juego.remainingTime()/1000 + self.balas * 70)
        self.puntaje = int((200 * self.num + parte*self.num)/self.dificultad)


class Mira(QObject):

    def __init__(self, pos_mira):
        super().__init__()
        self.pos_mira = pos_mira
        ubic = QUrl.fromLocalFile(p.RUTA_SONIDO_DISPARO)
        contenido = QMediaContent(ubic)
        self.sonido_disparo = QMediaPlayer()
        self.sonido_disparo.setMedia(contenido)
        self.sonido_disparo.setVolume(50)

        self.iniciar_graficos()

    # actualiza los graficos
    def iniciar_graficos(self):
        self.label_mira = QLabel('')
        self.pix_mira = QPixmap(p.RUTA_MIRA_NORMAL)
        self.pix_disparo = QPixmap(p.RUTA_MIRA_DISPARO)
        self.label_mira.setPixmap(self.pix_mira)
        self.label_mira.setScaledContents(True)
        self.label_mira.setFixedSize(p.WIDTH_MIRA, p.HEIGHT_MIRA)
        self.label_mira.move(self.pos_mira.x(), self.pos_mira.y())

    # accion de disparar, con timer y sonido
    def disparar(self):
        self.label_mira.setPixmap(self.pix_disparo)
        self.sonido_disparo.play()

        self.timer_disparo = QTimer()
        self.timer_disparo.setInterval(1000)
        self.timer_disparo.timeout.connect(self.graficos_normales)
        self.timer_disparo.setSingleShot(True)
        self.timer_disparo.start()

    # vuelve a los graficos sin mira roja
    def graficos_normales(self):
        self.label_mira.setPixmap(self.pix_mira)

    # mueve la mira
    def mover(self, lista_direc):
        for direc in lista_direc:
            if direc == "L" and self.pos_mira.x() > p.MIN_X_MIRA:
                self.pos_mira.moveTo(self.pos_mira.x() -
                                     p.VELOCIDAD_MIRA, self.pos_mira.y())
            if direc == "R" and self.pos_mira.x() < p.MAX_X_MIRA:
                self.pos_mira.moveTo(self.pos_mira.x() +
                                     p.VELOCIDAD_MIRA, self.pos_mira.y())
            if direc == "U" and self.pos_mira.y() > p.MIN_Y_MIRA:
                self.pos_mira.moveTo(
                    self.pos_mira.x(), self.pos_mira.y() - p.VELOCIDAD_MIRA)
            if direc == "D" and self.pos_mira.y() < p.MAX_Y_MIRA:
                self.pos_mira.moveTo(
                    self.pos_mira.x(), self.pos_mira.y() + p.VELOCIDAD_MIRA)


class Alien(QObject):

    def __init__(self, pos_alien, mundo):
        super().__init__()
        self.pos_alien = pos_alien
        self.direccion = list(p.VELOCIDAD_ALIEN)
        self.mundo = mundo
        self.vivo = True
        self.afuera = False
        self.iniciar_graficos()
        self.congelado = False

    # aumenta la velocidad segun el nivel y mundo
    def aumentar_velocidad(self, veces):
        for i in range(veces):
            if self.mundo == 0:
                print("mundo 1!")
                self.direccion[0] = self.direccion[0] / p.PONDERADOR_TUTORIAL
                self.direccion[1] = self.direccion[1] / p.PONDERADOR_TUTORIAL
            elif self.mundo == 1:
                print("Mundo 2!")
                self.direccion[0] = self.direccion[0] / \
                    p.PONDERADOR_ENTRENAMIENTO
                self.direccion[1] = self.direccion[1] / \
                    p.PONDERADOR_ENTRENAMIENTO
            else:
                print("Mundo 3!")
                self.direccion[0] = self.direccion[0] / p.PONDERADOR_INVASION
                self.direccion[1] = self.direccion[1] / p.PONDERADOR_INVASION

    def reseteo_velocidad(self):
        self.direccion[0] = p.VELOCIDAD_ALIEN[0]
        self.direccion[1] = p.VELOCIDAD_ALIEN[1]

    # actualiza los graficos segun el mundo
    def iniciar_graficos(self):
        self.label_alien = QLabel('')

        if self.mundo == 0:
            self.pix_alien = QPixmap(p.RUTA_ALIEN_1)
            self.pix_muerto = QPixmap(p.RUTA_ALIEN_1_MUERTO)
        elif self.mundo == 1:
            self.pix_alien = QPixmap(p.RUTA_ALIEN_2)
            self.pix_muerto = QPixmap(p.RUTA_ALIEN_2_MUERTO)
        else:
            self.pix_alien = QPixmap(p.RUTA_ALIEN_3)
            self.pix_muerto = QPixmap(p.RUTA_ALIEN_3_MUERTO)

        self.label_alien.setPixmap(self.pix_alien)
        self.label_alien.setScaledContents(True)
        self.label_alien.resize(p.WIDTH_ALIEN, p.HEIGHT_ALIEN)
        self.label_alien.move(self.pos_alien.x(), self.pos_alien.y())

    def reaccion_bomba_hielo(self):
        self.congelar()
        self.timer_bomba = QTimer()
        self.timer_bomba.setInterval(p.TIEMPO_CONGELAMIENTO * 1000)
        self.timer_bomba.setSingleShot(True)
        self.timer_bomba.timeout.connect(self.congelar)
        self.timer_bomba.start()

    def congelar(self):
        if self.congelado is False:
            self.congelado = True
        else:
            self.congelado = False

    def morir(self):
        print("Oh me muero!!!")
        self.vivo = False
        self.direccion = [0, 7]
        self.label_alien.setPixmap(self.pix_muerto)

    def mover(self):
        if self.vivo is True:
            if self.congelado is False:
                nueva_ubicacion = (
                    self.pos_alien.x() + self.direccion[0], self.pos_alien.y() + self.direccion[1])
                self.pos_alien.moveTo(nueva_ubicacion[0], nueva_ubicacion[1])
                self.colision_con_bordes()
        else:
            nueva_ubicacion = (
                self.pos_alien.x() + self.direccion[0], self.pos_alien.y() + self.direccion[1])
            self.pos_alien.moveTo(nueva_ubicacion[0], nueva_ubicacion[1])
            self.colision_muerto()

    # hace que reboten los aliens
    def colision_con_bordes(self):
        chocax = False
        chocay = False
        if not (p.MIN_X <= self.pos_alien.x()
                <= p.MAX_X):
            chocax = True
        if not (p.MIN_Y <= self.pos_alien.y()
                <= p.MAX_Y):
            chocay = True

        if chocax is True:
            self.direccion[0] = -self.direccion[0]
            print(f"Tope vertical de {self.__str__}")
        if chocay is True:
            self.direccion[1] = -self.direccion[1]
            print(f"Tope horizontal de {self.__str__}")

    # en caso de haber muerto reacciona de otra manera con los bordes
    def colision_muerto(self):
        salido = False
        if not (p.MIN_Y <= self.pos_alien.y() - 80
                <= p.MAX_Y):
            salido = True
        if salido is True:
            # print("Me he salido de la pantalla!")
            self.label_alien.hide()
            self.afuera = True


# animación de explosión, hecho muy ineficientemente...
class Explosion(QObject):

    def __init__(self, ubic):
        super().__init__()
        self.ubic = [ubic.x(), ubic.y()]
        self.fase = 1
        self.label_explosion_1 = QLabel('')
        self.label_explosion_2 = QLabel('')
        self.label_explosion_3 = QLabel('')
        self.pix_explosion_1 = QPixmap(p.RUTA_EXPLOSION_1)
        self.pix_explosion_2 = QPixmap(p.RUTA_EXPLOSION_2)
        self.pix_explosion_3 = QPixmap(p.RUTA_EXPLOSION_3)
        self.label_explosion_1.setPixmap(self.pix_explosion_1)
        self.label_explosion_2.setPixmap(self.pix_explosion_2)
        self.label_explosion_3.setPixmap(self.pix_explosion_3)
        self.label_explosion_1.setScaledContents(True)
        self.label_explosion_1.resize(80, 80)
        self.label_explosion_2.setScaledContents(True)
        self.label_explosion_2.resize(80, 80)
        self.label_explosion_3.setScaledContents(True)
        self.label_explosion_3.resize(80, 80)
        self.label_explosion_1.move(self.ubic[0], self.ubic[1])
        self.label_explosion_2.move(-100, -100)
        self.label_explosion_3.move(-100, -100)
        print(f"creando explosión en {self.ubic[0]}, {self.ubic[1]}")
        self.vivo = True

    def cambiar_fase(self):
        if self.label_explosion_1.x() == self.ubic[0]:
            self.label_explosion_1.move(-100, -100)
            self.label_explosion_2.move(self.ubic[0], self.ubic[1])
            self.fase = 2
        elif self.label_explosion_2.x() == self.ubic[0]:
            self.label_explosion_2.move(-100, -100)
            self.label_explosion_3.move(self.ubic[0], self.ubic[1])
            self.fase = 3

        else:
            self.vivo = False
            self.label_explosion_3.move(-100, -100)
            self.fase = 0
