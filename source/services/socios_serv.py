from source.repositories.socios_rep import (
    obtener_socios_rep,
    obtener_socio_rep,
    crear_socio_rep,
    modificar_socio_rep,
    existe_email_socio
)
from source.validators.socios_val import validar_socio, validar_email, validar_nombre
from source.utils import construir_error_api


def obtener_socios(nombre, activo, limit, offset):

    return obtener_socios_rep(
        nombre,
        activo,
        limit,
        offset
    )


def obtener_socio(id):

    return obtener_socio_rep(id)


def crear_socio(nombre, email):

    nombre, email = validar_socio(nombre, email)

    if existe_email_socio(email):
        raise ValueError(
            construir_error_api(
                code="conflict.email.exists",
                message=f"El email '{email}' ya existe",
                description=(
                    f"El email '{email}' ya se encuentra "
                    "registrado en la base de datos"
                )
            )
        )

    return crear_socio_rep(nombre, email, True)


def modificar_socio(id, datos):

    if not datos:
        raise ValueError(construir_error_api(
            code=f'invalid.request',
            message=f'No se enviaron datos para modificar',
            description=f'El cuerpo de la solicitud no contiene campos modificables'
        ))

    socio = obtener_socio_rep(id)

    if not socio:
        raise ValueError(
            construir_error_api(
                code=f'not.found.socio',
                message=f'Socio no encontrado',
                description=f'No existe un socio con id {id}'
            )
        )

    if "email" in datos:
        email = validar_email(datos["email"])

        if existe_email_socio(email):
            raise ValueError(construir_error_api(
                code=f'conflict.email.exist',
                message=f'EL email {email} ya existe',
                description=(
                    f'El email {email} ya se encuentra registrado en la base de datos'
                )
            ))

        datos["email"] = email

    if "nombre" in datos:
        datos["nombre"] = validar_nombre(datos["nombre"])

    return modificar_socio_rep(id, datos)