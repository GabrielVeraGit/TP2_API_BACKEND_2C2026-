from source.db import ejecutar_instruccion

def deportes_list():
    query = """
            SELECT *
            FROM deportes
        """
    
    return ejecutar_instruccion(query)

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