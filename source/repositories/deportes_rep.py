from source.db import ejecutar_instruccion


def consulta_deporte(id):

    query = """
        SELECT id
        FROM deportes
        WHERE id = %s
    """

    resultado = ejecutar_instruccion(query, (id,))

    if not resultado:
        return None

    return resultado[0]["id"]