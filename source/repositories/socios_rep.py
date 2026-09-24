from source.db import ejecutar_instruccion

def obtener_socios_rep(nombre, activo, limit, offset):
    query = """
        SELECT id, nombre, email, activo
        FROM socios
    """

    condiciones = []
    valores = []

    if nombre is not None:
        condiciones.append("LOWER(nombre) LIKE LOWER(%s)")
        valores.append(f"%{nombre}%")

    if activo is not None:
        condiciones.append("activo = %s")
        valores.append(activo)

    query += " WHERE " + " AND ".join(condiciones) if condiciones else "" 
    query += " LIMIT %s OFFSET %s"
    valores.extend([limit, offset])

    return ejecutar_instruccion(query, tuple(valores))