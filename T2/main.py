import sys

from PyQt5.QtWidgets import QApplication

# importación de las ventanas y logicas
from backend.logica_ranking import LogicaRanking
from backend.logica_principal import LogicaPrincipal
from backend.logica_juego import LogicaJuego

from frontend.codigo.ventana_inicio import VentanaInicio
from frontend.codigo.ventana_ranking import VentanaRanking
from frontend.codigo.ventana_principal import VentanaPrincipal
from frontend.codigo.ventana_juego import VentanaJuego
from frontend.codigo.ventana_postnivel import VentanaPostnivel


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])

    # creación de las logicas
    logica_ranking = LogicaRanking()
    logica_principal = LogicaPrincipal()
    logica_juego = LogicaJuego()

    # creación de las ventanas
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_principal = VentanaPrincipal()
    ventana_juego = VentanaJuego()
    ventana_postnivel = VentanaPostnivel()

    # conexión de señales
    ventana_inicio.senal_ver_rankings.connect(ventana_ranking.mostrar_ventana)
    ventana_ranking.senal_volver_menu.connect(ventana_inicio.mostrar_ventana)
    ventana_ranking.senal_pedir_info.connect(logica_ranking.obtener_info)
    logica_ranking.senal_enviar_info.connect(ventana_ranking.actualizar_info)

    ventana_inicio.senal_iniciar_juego.connect(
        ventana_principal.mostrar_ventana)
    ventana_principal.senal_info.connect(logica_principal.verificar_info)
    logica_principal.senal_correccion.connect(ventana_principal.revision_info)
    ventana_principal.senal_comienzo_juego.connect(
        ventana_juego.comenzar_juego)

    ventana_juego.senal_comienzo_juego.connect(logica_juego.empezar_juego)
    ventana_juego.senal_pausa.connect(logica_juego.pausar)
    logica_juego.senal_aliens.connect(ventana_juego.actualizar_aliens)
    logica_juego.senal_mira.connect(ventana_juego.actualizar_mira)
    ventana_juego.senal_tecla.connect(logica_juego.mover_mira)
    logica_juego.senal_mundo.connect(ventana_juego.cambiar_fondo)
    logica_juego.senal_inicio_nivel.connect(ventana_juego.recepcion_datos)
    logica_juego.senal_tiempo.connect(ventana_juego.actualizar_tiempo)
    ventana_juego.senal_volver_menu.connect(ventana_inicio.mostrar_ventana)
    ventana_juego.senal_salir_juego.connect(logica_juego.parar_juego)
    ventana_juego.senal_salir_juego.connect(ventana_postnivel.guardar_puntos)
    ventana_juego.senal_disparo.connect(logica_juego.disparo)
    logica_juego.senal_fin_nivel.connect(ventana_postnivel.mostrar_ventana)
    logica_juego.senal_fin_nivel.connect(ventana_juego.pasar_a_postnivel)
    ventana_postnivel.senal_salida.connect(ventana_inicio.mostrar_ventana)
    logica_juego.senal_explosion.connect(ventana_juego.mostrar_explosion)

    ventana_postnivel.senal_otro_nivel.connect(logica_juego.otro_nivel)
    logica_juego.senal_actualizacion_lista.connect(
        ventana_juego.comenzar_juego)
    ventana_principal.senal_nueva_partida.connect(logica_juego.primer_nivel)
    logica_juego.senal_victoria.connect(ventana_juego.victoria)
    logica_juego.senal_victoria.connect(ventana_postnivel.victoria)

    ventana_juego.senal_ovni.connect(logica_juego.balas_infinitas)
    ventana_juego.senal_cia.connect(logica_juego.codigo_cia)
    logica_juego.senal_estrella_muerte.connect(ventana_juego.mover_estrella)
    logica_juego.senal_bomba_hielo.connect(ventana_juego.mover_bomba_hielo)
    logica_juego.senal_colision_especiales.connect(
        ventana_juego.revision_colision_especiales)
    ventana_juego.senal_colision_estrella.connect(
        logica_juego.colision_estrella)
    ventana_juego.senal_colision_bomba.connect(
        logica_juego.colision_bomba)

    ventana_inicio.show()
    sys.exit(app.exec())
