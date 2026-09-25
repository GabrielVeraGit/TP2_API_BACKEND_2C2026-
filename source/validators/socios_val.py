from re import match

from flask import jsonify
from source.repositories.socios_rep import existe_email_socio
from source.utils import validar_string_no_vacio
from source.utils import construir_error_api

def validar_email(valor: str) -> str:
    """
    Verifica que el email sea valido.
    """
    valor = validar_string_no_vacio(valor, 'email')
    valor = valor.lower()

    patron = r'^[^@\s]+@[^@\s]+\.[^@\s]+$' #Expresion regular para validar un email simple

    if not match(patron, valor):
        raise ValueError(construir_error_api(
            code = f'invalid.email.format',
            message = f"Formato de 'email' invalido",
            description = f"El valor '{valor}' no tiene un formato de email valido"
        ))

    return valor

def validar_nombre(valor: str) -> str:
    """
    Verifica que el nombre no este vacio
    """

    valor = validar_string_no_vacio(valor, 'nombre')
    return valor

def validar_socio(nombre: str, email: str, activo: bool = True) -> bool:
    """
    Valida que los datos de un socio sean correctos.
    """

    try:
        nombre = validar_nombre(nombre)
        email = validar_email(email)
    
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    if existe_email_socio(email):
        raise ValueError(construir_error_api(
            code = f'conflict.email.exists',
            message = f"El email '{email}' ya existe",
            description = f"El email '{email}' ya se encuentra registrado en la base de datos"
        ))