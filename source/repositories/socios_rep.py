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
    query += " ORDER BY id ASC"
    query += " LIMIT %s OFFSET %s"
    valores.extend([limit, offset])

    return ejecutar_instruccion(query, tuple(valores))

def obtener_socio(id):
    query = """
        SELECT id, nombre, email, activo
        FROM socios
        WHERE id = %s
    """

    return ejecutar_instruccion(query, (id,))

def crear_socio_rep(nombre, email, activo):
    query = """
        INSERT INTO socios (nombre, email, activo)
        VALUES (%s, %s, %s)
    """

    return ejecutar_instruccion(query, (nombre, email, activo), autocommit=True)

def modificar_socio_rep(id, datos):
    campos = []
    valores = []

    if "nombre" in datos:
        campos.append("nombre = %s")
        valores.append(datos["nombre"])

    if "email" in datos:
        campos.append("email = %s")
        valores.append(datos["email"])

    if "activo" in datos:
        campos.append("activo = %s")
        valores.append(datos["activo"])

    if not campos:
        return []

    query = """
        UPDATE socios
        SET """ + ", ".join(campos) + """
        WHERE id = %s
    """

    valores.append(id)

    return ejecutar_instruccion(query, tuple(valores), autocommit=True)    