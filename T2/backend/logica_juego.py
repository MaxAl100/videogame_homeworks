from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect, QUrl
import backend.clases_apoyo as ca
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from random import randint, random

import parametros as p


class LogicaJuego(QObject):

    senal_aliens = pyqtSignal(list)
    senal_mira = pyqtSignal(ca.Mira)
    senal_mundo = pyqtSignal(int)
    senal_inicio_nivel = pyqtSignal(list)
    senal_tiempo = pyqtSignal(int)
    senal_fin_nivel = pyqtSignal(list)
    senal_traspaso_info = pyqtSignal(list)
    senal_explosion = pyqtSignal(ca.Explosion)
    senal_actualizacion_lista = pyqtSignal(list)
    senal_victoria = pyqtSignal()
    senal_estrella_muerte = pyqtSignal(list)
    senal_bomba_hielo = pyqtSignal(list)
    senal_colision_especiales = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.pausa = False
        self.puntos_acum = 0
        self.num = 1
        self.parado = False
        self.mostrado_estrella = False
        self.mostrado_bomba = False
        self.senal_estrella_muerte.emit([-100, -100])
        self.senal_bomba_hielo.emit([-100, -100])

    # crea el nivel en sí y ayuda a crear otros parámetros
    def setear_parametros(self, lista):
        self.nivel = ca.Nivel(lista[0], lista[1], lista[2])
        self.parado = False
        self.instanciar_timer()
        self.explosiones = []
#         self.disparando = False

    # crea timers
    def instanciar_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.timer_tick)
        self.subtick = 0

        self.timer_final = QTimer()
        self.timer_final.setInterval(p.TIEMPO_TERMINATOR_DOG * 1000)
        self.timer_final.setSingleShot(True)
        self.timer_final.timeout.connect(self.terminar_juego)

        self.timer_estrella = QTimer()
        self.timer_bomba = QTimer()

    # comienza el juego y llama la función que crea el nivel
    def empezar_juego(self, info_mundo):
        self.nombre = info_mundo[-1]
        print(self.nombre)
        info_mundo = info_mundo[:-1]
        i = 0
        elegido = -1
        for opcion in info_mundo:
            if opcion is True:
                elegido = i
            i += 1

        self.mundo = elegido

        self.senal_mundo.emit(elegido)

        self.setear_parametros(
            [elegido, self.num, p.DURACION_NIVEL_INICIAL * 1000])
        self.timer.start()
        print("juego comenzado")

        info_a_enviar = [self.nivel.num, self.puntos_acum, 0, self.nivel.aliens_por_matar,
                         self.nivel.balas, self.nivel.timer_juego.remainingTime()]

        self.senal_inicio_nivel.emit(info_a_enviar)

    # para resetear el número y puntos de la partida en caso de haber vuelto a al ventana inicial
    def primer_nivel(self):
        self.mostrado_estrella = False
        self.mostrado_bomba = False
        self.num = 1
        self.puntos_acum = 0

    # en caso de decidir seguir jugando desde la ventana postnivel se corre este código
    def otro_nivel(self, lista):
        self.num = lista[0]
        self.puntos_acum = int(lista[1])
        self.senal_actualizacion_lista.emit(lista[2])

    # esconde los labels pero no estoy seguro si dejan de "chocar", es decir si al dispararles
    # se gana puntaje o no

    # para el juego, ya sea con el botón o al ganar/perder con una de las condiciones
    def parar_juego(self):
        if self.parado is False:
            self.parado = True
            self.nivel.calculo_puntaje()
            self.puntos_acum += self.nivel.puntaje
            # info a enviar: nombre, nivel, balas, tiempo restante, puntaje nivel, puntaje acum
            info = []
            print("Escondiendo labels")
            self.nivel.alien1.label_alien.clear()
            self.nivel.alien2.label_alien.clear()
            self.nivel.mira.label_mira.clear()
            self.nivel.mira.label_mira.move(-100, -100)
            self.nivel.timer_juego.stop()

    # pausa y despausa el juego
    def pausar(self):
        if self.pausa is False:
            self.pausa = True
            self.tiempo = self.nivel.timer_juego.remainingTime()
            self.nivel.timer_juego.stop()
            self.tiempo_estrella = self.timer_estrella.remainingTime()
            self.timer_estrella.stop()
            self.tiempo_bomba = self.timer_bomba.remainingTime()
            self.timer_bomba.stop()
            self.tiempo_alien_1 = self.nivel.alien1.timer_bomba.remainingTime()
            self.nivel.alien1.timer_bomba.stop()
            self.tiempo_alien_2 = self.nivel.alien2.timer_bomba.remainingTime()
            self.nivel.alien2.timer_bomba.stop()
        else:
            self.pausa = False
            self.nivel.instanciar_timer(self.tiempo)
            self.timer_estrella.setInterval(self.tiempo_estrella)
            self.timer_estrella.start()
            self.timer_bomba.setInterval(self.tiempo_bomba)
            self.timer_bomba.start()
            self.nivel.alien1.timer_bomba.setInterval(self.tiempo_alien_1)
            self.nivel.alien1.timer_bomba.start()
            self.nivel.alien2.timer_bomba.setInterval(self.tiempo_alien_2)
            self.nivel.alien2.timer_bomba.start()

    # funcion unida a la señal de disparo de ventana_juego

    def disparo(self):
        self.timer_disparo = QTimer()
        self.timer_disparo.setInterval(200)
        self.disparar()
#        self.disparando = True
#        self.timer_disparo.timeout.connect(self.no_disparo)
        self.timer_disparo.start()

#    def no_disparo(self):
#        self.timer_disparo.stop()
#        self.disparando = False

    # cada vez que se dispara se corre esto. lo comentado era un intento de hacer que
    # se dispare continuamente

    def disparar(self):
        # if self.disparando is False:
        self.nivel.mira.disparar()
        if self.nivel.balas_infinitas is False:
            self.nivel.balas -= 1
        # ademas añadir la revisión si está sobre un alien
        ubicacion_centro_mira = (
            self.nivel.mira.pos_mira.x()+p.WIDTH_MIRA/2,
            self.nivel.mira.pos_mira.y()+p.HEIGHT_MIRA/2)
        aliens = [self.nivel.alien1, self.nivel.alien2]
        self.senal_colision_especiales.emit(ubicacion_centro_mira)

        i = 1
        hits = []
        for alien in aliens:
            ubi = (alien.pos_alien.x(), alien.pos_alien.y())
            if ubi[0] < ubicacion_centro_mira[0] < ubi[0] + 80:
                if ubi[1] < ubicacion_centro_mira[1] < ubi[1] + 80:
                    print(f"Estas sobre el alien {i}!")
                    if alien.vivo is True:
                        hits.append(i)
                        print("Y estaba vivo!")
                    else:
                        print("Estaba muerto y no te dió puntos...")

            i += 1
        for hit in hits:
            self.nivel.aliens_matados += 1
            self.nivel.aliens_por_matar -= 1
            if hit == 1:
                self.nivel.alien1.morir()
                self.crear_explosion(self.nivel.alien1.pos_alien)
            else:
                self.nivel.alien2.morir()
                self.crear_explosion(self.nivel.alien2.pos_alien)
        if self.nivel.alien1.vivo is False and self.nivel.alien2.vivo is False:
            self.nivel.alien1.label_alien.hide()
            self.nivel.alien2.label_alien.hide()
            if self.nivel.aliens_matados < self.num * 2:
                self.nivel.alien1.reseteo_velocidad()
                self.nivel.alien2.reseteo_velocidad()
                self.nivel.generar_aliens()  # ARREGLAR QUE APARECEN ALIENS SIN MATAR A LOS 2

    # actualiza la ubicación de la mira

    def mover_mira(self, direc):
        if self.parado is False:
            self.nivel.mira.mover(direc)

    # hace que el codigo ovni funcione
    def balas_infinitas(self):
        self.nivel.balas_infinitas = True

    # hace que el codigo cia funcione
    def codigo_cia(self):
        # esto hace que se termine el nivel de manera correcta
        self.nivel.aliens_por_matar = 0

    # crea una explosión al darle a un alien

    def crear_explosion(self, ubic):
        explosion = ca.Explosion(ubic)
        self.explosiones.append(explosion)
        self.senal_explosion.emit(explosion)
        self.timer_explosion = QTimer()
        self.timer_explosion.setInterval(750)
        self.timer_explosion.timeout.connect(self.actualizar_explosion)
        self.timer_explosion.start()

    # pasa por las distintas fases de la explosión

    def actualizar_explosion(self):
        for expl in self.explosiones:
            expl.cambiar_fase()
            if expl.vivo is False:
                expl.label_explosion_3.hide()
            # self.timer_explosion.timeout.connect(self.actualizar_explosion)
            self.senal_explosion.emit(expl)

    # en caso de victoria se corre esto para permitir pasar al siguiente nivel
    # Además, se corre la animación de victoria

    def victoria(self):
        self.senal_victoria.emit()

        ubic = QUrl.fromLocalFile(p.RUTA_SONIDO_RISA)
        contenido = QMediaContent(ubic)
        self.sonido_risa = QMediaPlayer()
        self.sonido_risa.setMedia(contenido)
        self.sonido_risa.setVolume(50)
        self.sonido_risa.play()

    # funciones para el bonus estrella de la muerte
    def estrella_muerte(self):
        if self.mostrado_estrella is False:
            self.mover_estrella()
            self.timer_estrella = QTimer()
            self.timer_estrella.setInterval(p.TIEMPO_ESTRELLA * 1000)
            self.timer_estrella.setSingleShot(True)
            self.timer_estrella.timeout.connect(self.mover_estrella)
            self.timer_estrella.start()

    def mover_estrella(self):
        if self.mostrado_estrella is False:
            lista = [randint(0, p.ANCHO_JUEGO - 100),
                     randint(0, p.ALTO_JUEGO - 100)]
            self.senal_estrella_muerte.emit(lista)
            self.mostrado_estrella = True
        else:
            self.senal_estrella_muerte.emit([-100, -100])

    def colision_estrella(self):
        print("Le has disparado a la estrella!")
        self.senal_estrella_muerte.emit([-100, -100])
        tiempo_original = self.nivel.timer_juego.remainingTime()
        tiempo_restante = tiempo_original - p.TIEMPO_PERDIDO * 1000
        if tiempo_restante < 0:
            tiempo_restante = 0
        self.nivel.timer_juego.setInterval(tiempo_restante)

    # funciones para el bonus bomba de hielo
    def bomba_hielo(self):
        if self.mostrado_bomba is False:
            self.mover_bomba()
            self.timer_bomba = QTimer()
            self.timer_bomba.setInterval(p.TIEMPO_BOMBA * 1000)
            self.timer_bomba.setSingleShot(True)
            self.timer_bomba.timeout.connect(self.mover_bomba)
            self.timer_bomba.start()

    def mover_bomba(self):
        if self.mostrado_bomba is False:
            lista = [randint(0, p.ANCHO_JUEGO - 100),
                     randint(0, p.ALTO_JUEGO - 100)]
            self.senal_bomba_hielo.emit(lista)
            self.mostrado_bomba = True
        else:
            lista = [-100, -100]
            self.senal_bomba_hielo.emit(lista)

    def colision_bomba(self):
        print("Le has disparado a la bomba de hielo!")
        self.senal_bomba_hielo.emit([-100, -100])
        self.nivel.alien1.reaccion_bomba_hielo()
        self.nivel.alien2.reaccion_bomba_hielo()

    # corre cada cierto tiempo para actualizar todo

    def timer_tick(self):
        if self.parado is False:
            if self.nivel.aliens_por_matar == 0:
                self.nivel.calculo_puntaje()
                tiempo = int(self.nivel.timer_juego.remainingTime()/1000)
                self.parar_juego()
                self.info = [self.nombre, self.num, self.nivel.balas,
                             tiempo, self.nivel.puntaje, self.puntos_acum]
                self.victoria()
                self.timer_final.start()

            elif self.nivel.balas == 0:
                self.nivel.calculo_puntaje()
                tiempo = int(self.nivel.timer_juego.remainingTime()/1000)
                self.parar_juego()
                self.info = [self.nombre, self.num, self.nivel.balas,
                             tiempo, self.nivel.puntaje, self.puntos_acum]
                self.timer_final.start()

            elif self.nivel.finalizado is True:
                self.nivel.calculo_puntaje()
                tiempo = int(self.nivel.timer_juego.remainingTime()/1000)
                self.parar_juego()
                self.info = [self.nombre, self.num, self.nivel.balas,
                             tiempo, self.nivel.puntaje, self.puntos_acum]
                self.timer_final.start()

            if self.pausa is False:
                if random() < p.PROBABILIDAD_ESTRELLA:
                    self.estrella_muerte()
                if random() < p.PROBABILIDAD_BOMBA:
                    self.bomba_hielo()
                self.nivel.avanzar_partida()
                self.senal_aliens.emit([self.nivel.alien1, self.nivel.alien2])
                self.senal_mira.emit(self.nivel.mira)
                if self.nivel.timer_juego.isActive() is True:
                    self.senal_tiempo.emit(
                        self.nivel.timer_juego.remainingTime())
            info_a_enviar = [self.nivel.num, self.puntos_acum, self.nivel.aliens_matados,
                             self.nivel.aliens_por_matar, self.nivel.balas]

            self.senal_inicio_nivel.emit(info_a_enviar)

    # termina el juego luego de la animación de terminator dog final
    # (o un tiempo muerto que dura lo mismo)
    def terminar_juego(self):
        self.senal_estrella_muerte.emit([-100, -100])
        self.senal_bomba_hielo.emit([-100, -100])
        self.nivel.mira.label_mira.move(-100, -100)
        self.info.append(self.mundo)
        self.senal_fin_nivel.emit(self.info)
