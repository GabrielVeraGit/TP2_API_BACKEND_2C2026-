from config import db
from src.models import cancha_model


def crear_cancha(id_deporte, nombre, techada, activa, precio):
    cancha = cancha_model.Cancha(
        id_deporte=id_deporte,
        nombre=nombre,
        techada=techada,
        activa=activa,
        precio=precio
    )

    db.session.add(cancha)
    db.session.commit()

    return cancha