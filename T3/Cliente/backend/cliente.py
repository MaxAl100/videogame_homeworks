"""
Modulo contiene implementación principal del cliente
"""
import socket
import json
from threading import Thread
from backend.interfaz import Interfaz


class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.interfaz = Interfaz(self)
        self.iniciar_cliente()

    def iniciar_cliente(self):
        """
        Se encarga de iniciar el cliente y conectar el socket
        """
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.comenzar_a_escuchar()
            self.interfaz.mostrar_ventana_inicio()
        except ConnectionError as e:
            self.log(f"Error de conexión {e}")

    def comenzar_a_escuchar(self):
        """
        Instancia el Thread que escucha los mensajes del servidor
        """
        thread = Thread(target=self.escuchar_servidor, daemon=True)
        thread.start()

    def escuchar_servidor(self):
        """
        Recibe mensajes constantes desde el servidor y responde.
        """
        while True:
            try:
                mensaje = self.recibir()
                self.interfaz.manejar_mensaje(mensaje)
            except ConnectionError as e:
                self.log(f"Error de conexión {e}")

    def recibir(self):
        """
        Se encarga de recibir los mensajes del servidor.
        """
        try:
            response_bytes_length = self.socket_cliente.recv(4)
            cant_bloques = int.from_bytes(
                response_bytes_length, byteorder='little')
            response = bytearray()

            for _ in range(cant_bloques):
                indice_bytes = self.socket_cliente.recv(4)
                indice = int.from_bytes(indice_bytes, byteorder="big")
                todos_bytes = self.socket_cliente.recv(1)
                todos = int.from_bytes(todos_bytes, byteorder="big")
                cant_bytes = self.socket_cliente.recv(1)
                cant = int.from_bytes(cant_bytes, byteorder="big")
                largo = min(20, cant)
                response.extend(self.socket_cliente.recv(largo))

            mensaje_desencriptado = self.desencriptar_mensaje(response)
            mensaje_decodificado = self.decodificar_mensaje(
                mensaje_desencriptado)
        except TypeError as t:
            # print(t)
            mensaje_decodificado = ""
        return(mensaje_decodificado)

    def enviar(self, mensaje):
        """
        Envía un mensaje a un cliente.
        """
        # TODO: Codificar el mensaje bien
        cant_bloques, mensaje_codificado = self.codificar_mensaje(mensaje)
        msg_length = cant_bloques.to_bytes(4, byteorder="little")
        self.socket_cliente.sendall(msg_length + mensaje_codificado)

    def codificar_mensaje(self, mensaje):
        try:
            datos_json = json.dumps(mensaje).encode("utf-8")
            datos_encriptados = self.encriptar_mensaje(datos_json)
            cant_bloques = 0
            mensaje_codificado = bytearray()
            while (cant_bloques)*20 < len(datos_encriptados):
                bloque = bytearray()
                bloque.extend(cant_bloques.to_bytes(4, byteorder='big'))

                if len(datos_encriptados) - (cant_bloques+1)*20 < 0:
                    num = 0
                    bloque.extend(num.to_bytes(1, byteorder="big"))
                    num = len(datos_encriptados) - cant_bloques*20
                    bloque.extend(num.to_bytes(1, byteorder="big"))
                else:
                    num = 1
                    bloque.extend(num.to_bytes(1, byteorder="big"))
                    num = 20
                    bloque.extend(num.to_bytes(1, byteorder="big"))

                bloque.extend(
                    datos_encriptados[cant_bloques*20:cant_bloques*20 + num])
                mensaje_codificado.extend(bloque)

                cant_bloques += 1
            return((cant_bloques, mensaje_codificado))
        except json.JSONDecodeError:
            print("ERROR: No se pudo codificar el mensaje")
            return b""

    def decodificar_mensaje(self, mensaje_bytes):
        """
        Decodifica el mensaje del servidor
        """
        try:
            mensaje_decodificado = json.loads(mensaje_bytes.decode("utf-8"))
            return(mensaje_decodificado)
        except json.JSONDecodeError:
            print("ERROR: No se pudo decodificar el mensaje")
            return {}

    def encriptar_mensaje(self, mensaje):
        parte_1 = bytearray()
        parte_2 = bytearray()
        mensaje_encriptado = bytearray()
        pos = 0
        try:
            while (len(parte_1) + len(parte_2)) < len(mensaje):
                for fase in range(4):
                    if fase == 0:
                        parte_1.extend(
                            mensaje[pos].to_bytes(1, byteorder="big"))
                        pos += 1
                    elif fase == 1:
                        parte_2.extend(
                            mensaje[pos].to_bytes(1, byteorder="big"))
                        pos += 1
                    elif fase == 2:
                        parte_1.extend(
                            mensaje[pos].to_bytes(1, byteorder="big"))
                        pos += 1
                        parte_1.extend(
                            mensaje[pos].to_bytes(1, byteorder="big"))
                        pos += 1
                    elif fase == 3:
                        parte_2.extend(
                            mensaje[pos].to_bytes(1, byteorder="big"))
                        pos += 1
                        parte_2.extend(
                            mensaje[pos].to_bytes(1, byteorder="big"))
                        pos += 1
        except IndexError as i:
            pass

        suma_1 = self.sacar_suma(parte_1)
        suma_2 = self.sacar_suma(parte_2)

        if suma_1 > suma_2:
            mensaje_encriptado.extend(int.to_bytes(0, 1, byteorder="big"))
            mensaje_encriptado.extend(parte_2)
            mensaje_encriptado.extend(parte_1)
        else:
            mensaje_encriptado.extend(int.to_bytes(1, 1, byteorder="big"))
            mensaje_encriptado.extend(parte_1)
            mensaje_encriptado.extend(parte_2)

        return(mensaje_encriptado)

    def desencriptar_mensaje(self, mensaje):
        mensaje_desencriptado = bytearray()
        orden = mensaje[0]
        mensaje = mensaje[1:]

        if orden == 0:
            mensaje_desencriptado.extend(self.orden_0(mensaje))
        else:
            mensaje_desencriptado.extend(self.orden_1(mensaje))
        return(mensaje_desencriptado)

    def orden_0(self, mensaje):
        # B y luego A
        nuevo_mensaje = bytearray()
        largo = len(mensaje)
        if largo % 2 == 1:
            centro = int(largo/2 - 0.5)
            parte_B = mensaje[:centro]
            parte_A = mensaje[centro:]
        else:
            if (largo + 2) % 6 == 0:
                # len(A) = len(B) + 2
                centro = int(largo/2) - 1
            else:
                # len(A) = len(B)
                centro = int(largo/2)
            parte_B = mensaje[:centro]
            parte_A = mensaje[centro:]
        pos_1 = 0
        pos_2 = 0
        try:
            while len(nuevo_mensaje) < largo:
                fase = 0
                for fase in range(4):
                    if fase == 0:
                        nuevo_mensaje.extend(
                            parte_A[pos_1].to_bytes(1, byteorder="big"))
                        pos_1 += 1
                    elif fase == 1:
                        nuevo_mensaje.extend(
                            parte_B[pos_2].to_bytes(1, byteorder="big"))
                        pos_2 += 1
                    elif fase == 2:
                        nuevo_mensaje.extend(
                            parte_A[pos_1].to_bytes(1, byteorder="big"))
                        pos_1 += 1
                        nuevo_mensaje.extend(
                            parte_A[pos_1].to_bytes(1, byteorder="big"))
                        pos_1 += 1
                    elif fase == 3:
                        nuevo_mensaje.extend(
                            parte_B[pos_2].to_bytes(1, byteorder="big"))
                        pos_2 += 1
                        nuevo_mensaje.extend(
                            parte_B[pos_2].to_bytes(1, byteorder="big"))
                        pos_2 += 1
                    fase += 1
        except IndexError as i:
            pass
        return(nuevo_mensaje)

    def orden_1(self, mensaje):
        # A y luego B
        nuevo_mensaje = bytearray()
        largo = len(mensaje)
        if largo % 2 == 1:
            centro = int(largo/2 + 0.5)
            parte_A = mensaje[:centro]
            parte_B = mensaje[centro:]
        else:
            if (largo + 2) % 6 == 0:
                # len(A) = len(B) + 2
                centro = int(largo/2) + 1
            else:
                # len(A) = len(B)
                centro = int(largo/2)
            parte_B = mensaje[centro:]
            parte_A = mensaje[:centro]
        pos_1 = 0
        pos_2 = 0
        try:
            while len(nuevo_mensaje) < largo:

                fase = 0
                for fase in range(4):
                    if fase == 0:
                        nuevo_mensaje.extend(
                            parte_A[pos_1].to_bytes(1, byteorder="big"))
                        pos_1 += 1
                    elif fase == 1:
                        nuevo_mensaje.extend(
                            parte_B[pos_2].to_bytes(1, byteorder="big"))
                        pos_2 += 1
                    elif fase == 2:
                        nuevo_mensaje.extend(
                            parte_A[pos_1].to_bytes(1, byteorder="big"))
                        pos_1 += 1
                        nuevo_mensaje.extend(
                            parte_A[pos_1].to_bytes(1, byteorder="big"))
                        pos_1 += 1
                    elif fase == 3:
                        nuevo_mensaje.extend(
                            parte_B[pos_2].to_bytes(1, byteorder="big"))
                        pos_2 += 1
                        nuevo_mensaje.extend(
                            parte_B[pos_2].to_bytes(1, byteorder="big"))
                        pos_2 += 1
                    fase += 1

        except IndexError as i:
            pass
        return(nuevo_mensaje)

    def sacar_suma(self, parte):
        largo = len(parte)
        if largo % 2 == 0:
            suma = parte[int(largo/2)] + parte[int(largo/2) - 1]
        else:
            medio = int(largo/2 - 0.5)
            promedio = (parte[medio - 1] + parte[medio + 1]) / 2
            suma = parte[medio] + promedio
        return(suma)

    def log(self, mensaje: str):
        """
        Imprime un mensaje en consola
        """
        print("|" + mensaje.center(80, " ") + "|")
