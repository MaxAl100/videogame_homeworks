import os
# en este archivo hice clases para las tres informaciones más relevantes
# para que sea más legible cuando uno busque información de aquí
# ya que en vez de tener un índice, existe una keyword :)


class User:
    def __init__(self, nombre, clave):
        self.nombre = nombre
        self.clave = clave
        pass


def cargar_usuarios(ruta_archivo):
    if os.path.exists(ruta_archivo) is False:
        with open(ruta_archivo, encoding='utf-8', mode="w+") as archivo:
            archivo.write("usuario,contrasena")
    with open(ruta_archivo, encoding='utf-8', mode="r+") as archivo:
        usuarios = archivo.readlines()

    usuarios_correcto = []

    for usuario in usuarios:
        usuario = usuario.split(",")
        usuario[1] = usuario[1].strip()
        user = User(usuario[0], usuario[1])
        usuarios_correcto.append(user)

    usuarios_correcto = usuarios_correcto[1:]

    return(usuarios_correcto)


class Reclamo:
    def __init__(self, usuario, titulo, descripcion):
        self.usuario = usuario
        self.titulo = titulo
        self.descripcion = descripcion
        pass


def cargar_reclamos(ruta_archivo):
    if os.path.exists(ruta_archivo) is False:
        with open(ruta_archivo, encoding='utf-8', mode="w+") as archivo:
            archivo.write("usuario,titulo,descripcion")
    with open(ruta_archivo, encoding='utf-8', mode="r+") as archivo:
        reclamos = archivo.readlines()

    reclamos_correcto = []

    for reclamo in reclamos:
        reclamo = reclamo.split(",", 2)
        reclamo[-1] = reclamo[-1].strip()
        reclamo_c = Reclamo(reclamo[0], reclamo[1], reclamo[2])
        reclamos_correcto.append(reclamo_c)

    reclamos_correcto = reclamos_correcto[1:]

    return(reclamos_correcto)


class Encomienda:
    def __init__(self, nombre, receptor, peso, destino, fecha, estado):
        self.nombre = nombre
        self.receptor = receptor
        self.peso = peso
        self.destino = destino
        self.fecha = fecha
        self.estado = estado
        pass

    def __str__(self):
        texto1 = "NOMBRE:   " + self.nombre
        texto2 = "RECEPTOR: " + self.receptor
        texto3 = "PESO:     " + self.peso
        texto4 = "DESTINO:  " + self.destino
        texto5 = "FECHA:    " + self.fecha
        texto6 = "ESTADO:   " + self.estado
        return(f"{texto1}\n{texto2}\n{texto3}\n{texto4}\n{texto5}\n{texto6}\n")


def cargar_encomiendas(ruta_archivo):
    if os.path.exists(ruta_archivo) is False:
        with open(ruta_archivo, encoding='utf-8', mode="w+") as archivo:
            archivo.write("nombre_articulo,receptor,peso,destino,fecha,estado")
    with open(ruta_archivo, encoding='utf-8', mode="r+") as archivo:
        encomiendas = archivo.readlines()

    encomiendas_correcto = []

    for encom in encomiendas:
        encom = encom.split(",")
        encom[-1] = encom[-1].strip()
        encomienda_c = Encomienda(
            encom[0], encom[1], encom[2], encom[3], encom[4], encom[5])
        encomiendas_correcto.append(encomienda_c)

    encomiendas_correcto = encomiendas_correcto[1:]
    return(encomiendas_correcto)
