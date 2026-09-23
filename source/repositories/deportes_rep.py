from source.db import ejecutar_instruccion


def obtener_deportes_rep():
    query = """
        SELECT id, nombre
        FROM deportes
    """

    return ejecutar_instruccion(query)