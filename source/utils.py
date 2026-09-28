from urllib.parse import urlencode
from flask import request

def construir_error_api(code: str, message: str, description: str, level: str = "error") -> dict:
    """
    Construye un diccionario con la estructura de error de la API.
    """

    return {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": level,
                "description": description
            }
        ]
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

def construir_link_paginacion(offset, limit):
    parametros = request.args.to_dict()
    
    parametros["_offset"] = offset
    parametros["_limit"] = limit

    query_string = urlencode(parametros)

    return {
        "href" : f'{request.base_url}?{query_string}'
    }

def construir_links_paginacion(total, limit, offset):
    links = {}

    ultimo_offset = ((total - 1) // limit) * limit

    links["_first"] = construir_link_paginacion(0, limit)
    links["_last"] = construir_link_paginacion(ultimo_offset, limit)

    if offset >= limit:
        links["_prev"] = construir_link_paginacion(
            offset - limit,
            limit
        )

    if offset + limit < total:
        links["_next"] = construir_link_paginacion(
            offset + limit,
            limit
        )

    return links