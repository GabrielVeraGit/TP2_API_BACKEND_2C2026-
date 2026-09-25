from source.data.canchas_data import canchas
from source.repositories import canchas_rep, deportes_rep

def obtener_canchas(id_deporte=None, nombre=None, techada=None, activa=None):
    return canchas_rep.consultar_canchas(id_deporte, nombre, techada, activa)


def crear_cancha(data):
    deporte_id = deportes_rep.consulta_deporte(data.get("id_deporte"))

    if deporte_id is None:
        return None, "El deporte indicado no existe" 

    return canchas_rep.crear_cancha(
        id_deporte=data.get("id_deporte"),
        nombre=data.get("nombre"),
        techada=data.get("techada"),
        activa=data.get("activa"),
        precio_hora=data.get("precio_hora")
        )