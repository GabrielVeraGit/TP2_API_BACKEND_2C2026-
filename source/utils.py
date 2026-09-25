from re import sub, match

def construir_error_api(code: str, message: str, description: str) -> dict:
    """
    Construye un diccionario con la estructura de error de la API.
    """
    return {
        'error': {
            'code': code,
            'message': message,
            'description': description
        }
    }

def validar_string_no_vacio(valor, campo: str = 'campo') -> str:
    """ 
    Valida que el valor sea un string no vacío. 
    """

    if valor is None or not str(valor).strip():
        raise ValueError(construir_error_api(
            code=f'required.{campo}',
            message=f"Campo requerido: '{campo}'",
            description=f"El campo '{campo}' es obligatorio y no puede estar vacio"
        ))

    return str(valor).strip()