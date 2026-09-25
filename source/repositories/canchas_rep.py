from config import db
from source.models import cancha_model


def consultar_canchas():

    resultado = db.session.query(cancha_model.Cancha).all()
    return [cancha.to_dict() for cancha in resultado]


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