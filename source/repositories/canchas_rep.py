from config import db
from source.models import cancha_model


def consultar_canchas(id_deporte=None, nombre=None, techada=None, activa=None ):

    consulta = db.session.query(cancha_model.Cancha)

    if id_deporte is not None:
        consulta = consulta.filter(
            cancha_model.Cancha.id_deporte == id_deporte
        )

    if nombre is not None:
        consulta = consulta.filter(
            cancha_model.Cancha.nombre == nombre
        )

    if techada is not None:
        consulta = consulta.filter(
            cancha_model.Cancha.techada == techada
        )

    if activa is not None:
        consulta = consulta.filter(
            cancha_model.Cancha.activa == activa
        )

    canchas = consulta.all()

    return [cancha.to_dict() for cancha in canchas]



def crear_cancha(id_deporte, nombre, techada, activa, precio_hora):
    cancha = cancha_model.Cancha(
        id_deporte=id_deporte,
        nombre=nombre,
        techada=techada,
        activa=activa,
        precio_hora=precio_hora
    )

    db.session.add(cancha)
    db.session.commit()

    return cancha