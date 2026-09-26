from source.data.canchas_data import canchas
from source.repositories import canchas_rep, deportes_rep, reservas_rep

def obtener_canchas(id_deporte=None, nombre=None, techada=None, activa=None, limit=None):
    return canchas_rep.consultar_canchas(id_deporte, nombre, techada, activa, limit)

def cancha_por_id(id):
    return canchas_rep.cancha_por_id(id)

def crear_cancha(data):
    deporte_id = deportes_rep.consulta_deporte(data.get("id_deporte"))

    if deporte_id is None:
        return None, "El deporte indicado no existe" 

    id_cancha= canchas_rep.crear_cancha(
        id_deporte=data.get("id_deporte"),
        nombre=data.get("nombre"),
        techada=data.get("techada"),
        activa=data.get("activa"),
        precio_hora=data.get("precio_hora")
        )

    return canchas_rep.cancha_por_id(id_cancha)

def update_cancha(id, data):
    existe_cancha = canchas_rep.cancha_por_id(id)
    if existe_cancha is None:
            return None, "El id indicado no existe"

    return canchas_rep.update_cancha(
        id=id,
        nombre=data.get("nombre",existe_cancha["nombre"]),
        techada=data.get("techada",existe_cancha["techada"]),
        activa=data.get("activa",existe_cancha["activa"]),
        precio_hora=data.get("precio_hora",existe_cancha["precio_hora"])
    )

def eliminar_cancha(id_cancha):

    filtros = [id_cancha]
    query_filtros = "id = %s"

    reservas = reservas_rep.obtener_reservas_rep(filtros, query_filtros)

    if not reservas:
        return None, "La reserva indicada no existe"

    return canchas_rep.eliminar_cancha(id_cancha)

    

