from source.data.canchas_data import canchas
from source.repositories import canchas_rep

def obtener_canchas(id_deporte=None, nombre=None, techada=None, activa=None):
    return canchas_rep.consultar_canchas()


def crear_cancha(data):
    return canchas_rep.crear_cancha(
        id_deporte=data.get("id_deporte"),
        nombre=data.get("nombre"),
        techada=data.get("techada"),
        activa=data.get("activa"),
        precio_hora=data.get("precio_hora")
        )