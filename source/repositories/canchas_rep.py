from source.db import ejecutar_instruccion

def contar_canchas_rep(id_deporte=None, nombre=None, techada=None, activa=None):
    query = """
        SELECT COUNT(*) AS total
        FROM canchas
        WHERE 1=1
    """

    valores = []

    if id_deporte is not None:
        query += " AND deporte_id = %s"
        valores.append(id_deporte)

    if nombre is not None:
        query += " AND LOWER(nombre) LIKE LOWER(%s)"
        valores.append(f"%{nombre}%")

    if techada is not None:
        query += " AND techada = %s"
        valores.append(techada)

    if activa is not None:
        query += " AND activa = %s"
        valores.append(activa)

    resultados = ejecutar_instruccion(query, tuple(valores))

    return resultados[0]["total"]

def consultar_canchas(id_deporte=None, nombre=None, techada=None, activa=None, limit=None, offset=0):

    query = """
        SELECT
            id,
            deporte_id AS id_deporte,
            nombre,
            techada,
            activa,
            precio_hora
        FROM canchas
        WHERE 1=1
    """

    valores = []

    if id_deporte is not None:
        query += " AND deporte_id = %s"
        valores.append(id_deporte)

    if nombre is not None:
        query += " AND LOWER(nombre) LIKE LOWER(%s)"
        valores.append(f"%{nombre}%")

    if techada is not None:
        query += " AND techada = %s"
        valores.append(techada)

    if activa is not None:
        query += " AND activa = %s"
        valores.append(activa)

    query += " ORDER BY id ASC"
    query += " LIMIT %s OFFSET %s"
    valores.extend([limit, offset])

    return ejecutar_instruccion(query, tuple(valores))


def crear_cancha(id_deporte, nombre, techada, activa, precio_hora):

    query = """
        INSERT INTO canchas
            (deporte_id, nombre, techada, activa, precio_hora)
        VALUES
            (%s, %s, %s, %s, %s)
    """

    valores = (
        id_deporte,
        nombre,
        techada,
        activa,
        precio_hora
    )

    resultado = ejecutar_instruccion(
        query,
        valores,
        autocommit=True
    )

    return resultado[0]["id"]


def cancha_por_id(id):

    query = """
        SELECT
            id,
            deporte_id AS id_deporte,
            nombre,
            techada,
            activa,
            precio_hora
        FROM canchas
        WHERE id = %s
    """

    resultado = ejecutar_instruccion(query, (id,))
    if not resultado:
        return None

    return resultado[0]

def update_cancha(
        id,
        nombre,
        techada,
        activa,
        precio_hora
    ):

    query = """
        update canchas set 
        nombre = %s,
        techada = %s,
        activa = %s,
        precio_hora = %s
        where id = %s
    """

    valores = (
        nombre,
        techada,
        activa,
        precio_hora,
        id
    )

    ejecutar_instruccion(query, valores, autocommit=True)

    return cancha_por_id(id)

def eliminar_cancha(id_cancha):

    query = """
        DELETE FROM canchas
        WHERE id = %s
    """

    ejecutar_instruccion(
        query,
        (id_cancha,),
        autocommit=True
    )

def consultar_canchas_disponibles(data):
    fecha = data.get("fecha")
    
    hora_inicio = data.get("hora_inicio")
    fecha_hora_inicio = fecha + " " + hora_inicio
    
    hora_fin = data.get("hora_fin")
    fecha_hora_fin = fecha + " " + hora_fin

    id_deporte = data.get("id_deporte")
    techada = data.get("techada")
    limit = data.get("limit")
    offset = data.get("offset")
    

    query = """
        SELECT
            c.id,
            c.deporte_id AS id_deporte,
            c.nombre,
            c.techada,
            c.activa,
            c.precio_hora
        FROM canchas c
        LEFT JOIN reservas r
            ON r.cancha_id = c.id
            AND r.estado = 'Confirmada'
            AND r.fecha_hora_inicio < %s
            AND r.fecha_hora_fin > %s
        WHERE c.activa = TRUE
            AND r.id IS NULL
    """

    valores = [fecha_hora_fin, fecha_hora_inicio]

    if id_deporte is not None:
        query += " AND c.deporte_id = %s"
        valores.append(id_deporte)

    if techada is not None:
        query += " AND c.techada = %s"
        valores.append(techada)

    query += " ORDER BY c.id ASC LIMIT %s OFFSET %s"
    valores.extend([limit, offset])

    return ejecutar_instruccion(query, tuple(valores))