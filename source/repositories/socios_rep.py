from source.db import ejecutar_instruccion

def obtener_socios_rep(limit, offset):
    query = """
        SELECT id, nombre, email, activo
        FROM socios
        LIMIT %s OFFSET %s
    """

    return ejecutar_instruccion(query, (limit, offset))