from src.data.canchas_data import canchas
from src.repositories import canchas_rep

def obtener_canchas(id_deporte=None, nombre=None, techada=None, activa=None):
    resultado = []

    for cancha in canchas:
        if (cancha.get("id_deporte") ==  id_deporte):
           resultado.append(cancha) 

    return resultado

def crear_cancha(data):
    return canchas_rep.crear_cancha(
        id_deporte=data.get("id_deporte"),
        nombre=data.get("nombre"),
        techada=data.get("techada"),
        activa=data.get("activa"),
        precio=data.get("precio")
        )