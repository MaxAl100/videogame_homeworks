"""
Módulo principal del cliente.
"""
import sys
from os.path import join
from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from utils import data_json

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    try:
        # =========> Instanciamos la APP <==========
        app = QApplication(sys.argv)

        # =========> Iniciamos el cliente <==========
        cliente = Cliente(HOST, PORT)

        sys.exit(app.exec_())

    except ConnectionError as e:
        print("Ocurrió un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.salir()
        sys.exit()
