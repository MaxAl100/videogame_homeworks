"""
Modulo contiene la implementación principal del servidor
"""
import json
import socket
import threading
from logica import Logica


class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.conectado = False
        self.logica = Logica(self)
        self.id_cliente = 0
        self.socket_clientes = []
        self.socket_jugadores = []
        self.log("".center(80, "-"))
        self.log("Inicializando servidor...")
        self.iniciar_servidor()

    def iniciar_servidor(self):
        self.socket_servidor = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.conectado = True
        self.log(
            f"Escuchando a clientes en el host {self.host} y puerto {self.port}")
        self.comenzar_a_aceptar()

    def comenzar_a_aceptar(self):
        thread = threading.Thread(target=self.aceptar_clientes)
        thread.start()

    def aceptar_clientes(self):
        while self.conectado:
            try:
                client_socket, address = self.socket_servidor.accept()
                thread_escuchar_cliente = threading.Thread(
                    target=self.escuchar_cliente,
                    args=(self.id_cliente, client_socket, ),
                    daemon=True)
                thread_escuchar_cliente.start()
                self.id_cliente += 1
            except ConnectionError as e:
                self.log("Error de conexión")

    def escuchar_cliente(self, id_cliente, socket_cliente):
        self.log(f"Comenzando a escuchar al cliente {id_cliente}...")
        self.socket_clientes.append(socket_cliente)
        hecho = 0
        while True:
            try:
                mensaje_decodificado = self.recibir_mensaje(socket_cliente)
                if len(mensaje_decodificado) == 0:
                    raise(ConnectionError)
                mensaje_procesado = self.logica.procesar_mensaje(
                    mensaje_decodificado, socket_cliente)
                if len(mensaje_procesado) == 0:
                    raise(ConnectionError)
                try:
                    todos = mensaje_procesado["todos"]
                except KeyError:
                    todos = False
                if todos is True:
                    self.enviar_mensaje_todos(mensaje_procesado)
                else:
                    self.enviar_mensaje(mensaje_procesado, socket_cliente)
            except ConnectionResetError as c:
                self.log(
                    f"El cliente con el id {id_cliente} se ha desconectado")
                try:
                    self.eliminar_cliente(id_cliente, socket_cliente)
                    self.socket_clientes.remove(socket_cliente)
                    self.socket_jugadores.remove(socket_cliente)
                except ValueError as v:
                    pass
            except ConnectionError as e:
                if hecho == 0:
                    hecho += 1
                    try:
                        self.eliminar_cliente(id_cliente, socket_cliente)
                        self.socket_clientes.remove(socket_cliente)
                        self.socket_jugadores.remove(socket_cliente)
                    except ValueError as v:
                        pass

    def recibir_mensaje(self, socket_cliente):
        try:
            response_bytes_length = socket_cliente.recv(4)
            cant_bloques = int.from_bytes(
                response_bytes_length, byteorder='little')
            response = bytearray()
            for _ in range(cant_bloques):
                indice_bytes = socket_cliente.recv(4)
                indice = int.from_bytes(indice_bytes, byteorder="big")
                todos_bytes = socket_cliente.recv(1)
                todos = int.from_bytes(todos_bytes, byteorder="big")
                cant_bytes = socket_cliente.recv(1)
                cant = int.from_bytes(cant_bytes, byteorder="big")
                largo = min(20, cant)
                response.extend(socket_cliente.recv(largo))
            mensaje_desencriptado = self.desencriptar_mensaje(response)
            mensaje_decodificado = self.decodificar_mensaje(
                mensaje_desencriptado)
        except TypeError as t:
            # print(t)
            mensaje_decodificado = ""
        except OSError as os:
            mensaje_decodificado = ""
        return(mensaje_decodificado)

    def enviar_mensaje(self, mensaje, socket_cliente):
        cant_bloques, mensaje_codificado = self.codificar_mensaje(mensaje)
        msg_length = cant_bloques.to_bytes(4, byteorder="little")
        socket_cliente.send(msg_length + mensaje_codificado)

    def enviar_mensaje_todos(self, mensaje):
        for socket in self.socket_clientes:
            self.enviar_mensaje(mensaje, socket)

    def enviar_mensaje_siguiente(self, mensaje, actual):
        try:
            socket_enviar = self.socket_jugadores[actual]
        except IndexError as _:
            socket_enviar = self.socket_jugadores[0]
        finally:
            cant_bloques, mensaje_codificado = self.codificar_mensaje(mensaje)
            msg_length = cant_bloques.to_bytes(4, byteorder="little")
            socket_enviar.send(msg_length + mensaje_codificado)

    def enviar_archivo(self, socket_cliente, ruta):
        """
        Recibe una ruta a un archivo a enviar y los separa en chunks de 8 kb
        """
        with open(ruta, "rb") as archivo:
            chunk = archivo.read(8000)
            largo = len(chunk)
            while largo > 0:
                chunk = chunk.ljust(8000, b"\0")  # Padding
                msg = {
                    "comando": "chunk",
                    "argumentos": {"largo": largo, "contenido": chunk.hex()},
                    "ruta": ruta,
                }
                self.enviar_mensaje(msg, socket_cliente)
                chunk = archivo.read(8000)
                largo = len(chunk)

    def eliminar_cliente(self, id_cliente, socket_cliente):
        """
        Elimina un cliente del diccionario de clientes conectados
        """
        try:
            self.log(f"Borrando socket del cliente {id_cliente}.")
            if len(self.socket_clientes) > 1:
                if socket_cliente == self.socket_clientes[0]:
                    self.logica.hacer_admin(self.socket_clientes[1])
            socket_cliente.close()
            # Desconectamos el usuario de la lista de jugadores
            self.logica.procesar_mensaje(
                {"comando": "desconectar", "id": id_cliente}, socket_cliente
            )

        except KeyError as e:
            # self.log(f"ERROR: {e}")
            pass

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
