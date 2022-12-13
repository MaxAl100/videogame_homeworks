"""
Modulo contiene la clase Logica del servidor
"""
from utils import data_json
import clases_apoyo as ca
from random import choice
from random import randint


class Logica:
    def __init__(self, parent):
        # Esto permite ejecutar funciones de la clase Servidor
        self.parent = parent
        self.id_jugador = 0
        self.jugadores = 0
        self.en_partida = False
        self.colores = ["rojo", "azul", "amarillo", "verde"]
        self.caract_jugadores = []
        self.usuarios = {}
        self.tablero = ca.Tablero(self)

    def validar_login(self, nombre, socket_cliente):

        if self.jugadores == 0:
            self.colores = ["rojo", "azul", "amarillo", "verde"]

        if nombre.isalnum() is False:
            self.parent.log(
                f"Un cliente ha insertado el nombre {nombre} que no es valido")
            return{"comando": "respuesta_validacion_login",
                   "estado": "rechazado",
                   "error": "Nombre invalido", }
        elif nombre in self.usuarios.values():
            self.parent.log(
                f"Un cliente ha insertado el nombre {nombre} que no es valido")
            return{"comando": "respuesta_validacion_login",
                   "estado": "rechazado",
                   "error": "Nombre de usuario ya existente", }
        elif self.jugadores >= data_json("MAXIMO_JUGADORES"):
            self.parent.log(
                f"Un cliente ha insertado el nombre {nombre} que no es valido")
            return{"comando": "respuesta_validacion_login",
                   "estado": "rechazado",
                   "error": "Sala de espera llena", }
        elif self.en_partida is True:
            self.parent.log(
                f"Un cliente ha insertado el nombre {nombre} que no es valido")
            return{"comando": "respuesta_validacion_login",
                   "estado": "rechazado",
                   "error": "Partida ya comenzada", }
        elif len(nombre) > 10:
            self.parent.log(
                f"Un cliente ha insertado el nombre {nombre} que no es valido")
            return{"comando": "respuesta_validacion_login",
                   "estado": "rechazado",
                   "error": "Nombre demasiado largo", }
        else:
            if self.jugadores == 0:
                self.hacer_admin(socket_cliente)
                self.caract_jugadores = []

            self.usuarios[self.id_jugador] = nombre
            self.jugadores += 1
            jugador = self.generar_jugador(nombre)
            self.caract_jugadores.append(jugador)

            self.id_jugador += 1

            self.parent.socket_jugadores.append(socket_cliente)
            self.parent.log(
                f"Un cliente ha insertado el nombre {nombre} que es valido")
            return {
                "comando": "respuesta_validacion_login",
                "estado": "aceptado",
                "nombre_usuario": nombre,
            }

    def hacer_admin(self, socket_cliente):
        mensaje = dict()
        mensaje["comando"] = "hacer_admin"
        self.parent.enviar_mensaje(mensaje, socket_cliente)

    def generar_jugador(self, nombre):
        color = choice(self.colores)
        colores_2 = []
        for col in self.colores:
            if col != color:
                colores_2.append(col)
        self.colores = colores_2
        if color == "rojo":
            jug = ca.JugadorRojo(nombre, [0, 80], self.tablero, self)
        elif color == "azul":
            jug = ca.JugadorAzul(nombre, [0, 80], self.tablero, self)
        elif color == "verde":
            jug = ca.JugadorVerde(nombre, [0, 80], self.tablero, self)
        elif color == "amarillo":
            jug = ca.JugadorAmarillo(nombre, [0, 80], self.tablero, self)
        self.tablero.agregar_jugador(jug)
        return(jug)

    def eliminar_nombre(self, identidad):
        self.jugadores -= 1

        for jugador in self.caract_jugadores:
            if jugador.nombre == self.usuarios[identidad]:
                self.colores.append(jugador.color)
        self.usuarios.pop(identidad, None)

        lista_ids = []
        for identidad in self.usuarios.keys():
            lista_ids.append(identidad)

        i = 0
        new_players = []
        for usuario in self.usuarios.values():
            for jugador in self.caract_jugadores:
                if jugador.nombre == usuario:
                    new_players.append(jugador)
                    i += 1

        self.caract_jugadores = new_players

    def informacion_jugadores(self):
        lista_jugadores = []
        for jug in self.caract_jugadores:
            info_jug = []
            info_jug.append(jug.nombre)
            info_jug.append(jug.color)
            lista_jugadores.append(info_jug)

        while len(lista_jugadores) < 4:
            lista_jugadores.append([])

        if len(self.caract_jugadores) == data_json("MAXIMO_JUGADORES"):
            if self.en_partida is False:
                self.tablero.posiciones_iniciales()
            self.en_partida = True
            mensaje = {"comando": "comenzar_juego",
                       "todos": True,
                       "info": lista_jugadores
                       }

            self.parent.enviar_mensaje_todos(mensaje)

        return {
            "comando": "actualizar_ventana_espera",
            "jugadores": lista_jugadores,
        }

    def revision_comienzo_partida(self):
        if self.jugadores >= data_json("MINIMO_JUGADORES"):
            return(True)
        return(False)

    def lanzar_dado(self, jugador):
        resultado = randint(1, 3)
        self.caract_jugadores[jugador - 1].mover_pieza(resultado)
        respuesta = {"comando": "resultado_dado",
                     "resultado": resultado,
                     "jugador": jugador,
                     "todos": True
                     }
        siguiente = {"comando": "en_turno"}
        jug_siguiente = self.caract_jugadores[(
            jugador) % len(self.caract_jugadores)]
        self.parent.log(f"Comienza el turno de {jug_siguiente.nombre}")
        self.parent.enviar_mensaje_siguiente(
            siguiente, jugador % len(self.caract_jugadores))

        pos_tablero = self.tablero.info_a_enviar()
        if pos_tablero["comando"] == "fin_juego":
            self.en_partida = False
            self.parent.log(
                f"El jugador {pos_tablero['ganador']} ha ganado la partida!")
            self.caract_jugadores = []
            self.jugadores = 0
            self.colores = ["rojo", "azul", "amarillo", "verde"]
            self.usuarios = {}
            self.tablero = ca.Tablero(self)

        self.parent.enviar_mensaje_todos(pos_tablero)

        return(respuesta)

    def procesar_mensaje(self, mensaje, socket_cliente):
        """
        Procesa un mensaje recibido desde el cliente
        """
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}
        if comando == "validar_login":
            respuesta = self.validar_login(
                mensaje["nombre usuario"], socket_cliente
            )
        elif comando == "desconectar":
            self.eliminar_nombre(mensaje["id"])
            return ""
        elif comando == "actualizar_sala_espera":
            respuesta = self.informacion_jugadores()
        elif comando == "empezar_partida":
            if self.revision_comienzo_partida() is True:
                self.en_partida = True
                self.parent.log(
                    "Se ha comenzado la partida con los siguientes jugadores:")
                lista_jugadores = []
                for jug in self.caract_jugadores:
                    self.parent.log(str(jug))
                    info_jug = []
                    info_jug.append(jug.nombre)
                    info_jug.append(jug.color)
                    lista_jugadores.append(info_jug)
                mensaje = {"comando": "comenzar_juego",
                           "todos": True,
                           "info": lista_jugadores
                           }
                pos_tablero = self.tablero.info_a_enviar()
                self.parent.enviar_mensaje_todos(pos_tablero)
                self.parent.log(
                    f"Comienza el turno de {self.caract_jugadores[0].nombre}")
                self.tablero.posiciones_iniciales()
                respuesta = mensaje
            else:
                self.parent.log(
                    "Se ha intentado comenzar la partida pero no hay suficientes jugadores")
                respuesta = {"comando": "no_comenzar_juego"}
        elif comando == "lanzar_dado":
            respuesta = self.lanzar_dado(mensaje["turno"])
        return respuesta
