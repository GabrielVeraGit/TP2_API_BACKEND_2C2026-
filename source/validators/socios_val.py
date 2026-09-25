from re import match
from source.utils import validar_string_no_vacio
from source.utils import construir_error_api

def validar_email(valor) -> str:
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

def validar_nombre(valor) -> str:
    """
    Verifica que el nombre no este vacio
    """

    valor = validar_string_no_vacio(valor, 'nombre')
    return valor