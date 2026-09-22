from src.data.canchas_data import canchas

def obtener_canchas(id_deporte=None, nombre=None, techada=None, activa=None):
    resultado = []

    for cancha in canchas:
        if (cancha.get("id_deporte") ==  id_deporte):
           resultado.append(cancha) 

    return resultado