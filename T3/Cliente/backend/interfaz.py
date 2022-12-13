"""
Ventana principal del cliente que se encarga de funcionar como backend de la
mayoria de ventanas, de conectar señales y de procesar los mensajes recibidos
por el cliente
"""
from PyQt5.QtCore import pyqtSignal, QObject

from frontend.codigo.ventana_inicio import VentanaInicio
from frontend.codigo.ventana_espera import VentanaEspera
from frontend.codigo.ventana_juego import VentanaJuego
from frontend.codigo.ventana_final import VentanaFinal
from utils import guardar_archivo


class Interfaz(QObject):

    senal_login_rechazado = pyqtSignal(str)
    senal_abrir_ventana_espera = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.ventana_inicio = VentanaInicio()
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()
        self.ventana_final = VentanaFinal()
        # -----------------------------------------
        self.descarga_actual = bytearray()

        #  ==========> CONEXIONES <==========

        # Señales ventana de inicio
        self.ventana_inicio.senal_enviar_login.connect(parent.enviar)
        self.senal_abrir_ventana_espera.connect(self.abrir_ventana_espera)
        self.senal_login_rechazado.connect(self.ventana_inicio.mostrar_error)
        self.senal_abrir_ventana_espera.connect(
            self.ventana_espera.iniciar_actualizacion)

        # Señales ventana de espera
        self.ventana_espera.senal_pedir_actualizacion.connect(parent.enviar)
        self.ventana_espera.senal_pedir_comienzo_juego.connect(parent.enviar)
        self.ventana_espera.senal_comenzar_juego.connect(
            self.ventana_espera.ocultar)
        self.ventana_espera.senal_comenzar_juego.connect(
            self.ventana_juego.mostrar)
        self.ventana_espera.senal_comenzar_juego.connect(
            self.ventana_espera.detener_actualizacion)

        # Señales ventana de juego
        self.ventana_juego.senal_info_inicio.connect(
            self.ventana_juego.datos_inicio)
        self.ventana_juego.senal_lanzamiento_dado.connect(parent.enviar)
        self.ventana_juego.senal_actualizar_tablero.connect(
            self.ventana_juego.actualizar_tablero)
        self.ventana_juego.senal_fin_juego.connect(
            self.ventana_juego.fin_juego)
        self.ventana_juego.senal_fin_juego.connect(self.ventana_final.mostrar)
        self.ventana_juego.senal_info_ventana_final.connect(
            self.ventana_final.actualizar_ventana)

        # Señales ventana final
        self.ventana_final.senal_volver_menu_inicial.connect(
            self.ventana_final.ocultar)
        self.ventana_final.senal_volver_menu_inicial.connect(
            self.ventana_inicio.mostrar)
        self.ventana_final.senal_volver_menu_inicial.connect(
            self.ventana_espera.desactivar_admin)
        self.ventana_final.senal_volver_menu_inicial.connect(
            self.ventana_juego.no_poder_lanzar)

    def mostrar_ventana_inicio(self):
        self.ventana_inicio.mostrar()

    def abrir_ventana_espera(self):
        self.ventana_espera.mostrar()
        self.ventana_inicio.ocultar()

    def manejar_mensaje(self, mensaje: dict):
        """
        Maneja un mensaje recibido desde el servidor.
        """
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}

        if comando == "respuesta_validacion_login":
            if mensaje["estado"] == "aceptado":
                nombre_usuario = mensaje["nombre_usuario"]
                self.senal_abrir_ventana_espera.emit()
            else:
                self.senal_login_rechazado.emit(mensaje["error"])
        elif comando == "actualizar_ventana_espera":
            self.ventana_espera.actualizar_info_jugadores(mensaje["jugadores"])
        elif comando == "hacer_admin":
            self.ventana_espera.cambiar_estado_admin()
            self.ventana_juego.poder_lanzar_dado()
        elif comando == "comenzar_juego":
            self.ventana_espera.senal_comenzar_juego.emit()
            self.ventana_juego.senal_info_inicio.emit(mensaje["info"])
        elif comando == "no_comenzar_juego":
            self.ventana_espera.falta_jugadores()
        elif comando == "resultado_dado":
            self.ventana_juego.resultado_dado(
                mensaje["resultado"], mensaje["jugador"])
        elif comando == "en_turno":
            self.ventana_juego.poder_lanzar_dado()
        elif comando == "actualizar_tablero":
            self.ventana_juego.senal_actualizar_tablero.emit(
                mensaje["tablero"], mensaje["rectas_finales"], mensaje["estadisticas_jugadoras"])
        elif comando == "fin_juego":
            self.ventana_juego.senal_fin_juego.emit(mensaje["ganador"])
