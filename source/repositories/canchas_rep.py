from source.db import ejecutar_instruccion


def consultar_canchas(id_deporte=None, nombre=None, techada=None, activa=None, limit=None):

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
        query += " AND nombre = %s"
        valores.append(nombre)

    if techada is not None:
        query += " AND techada = %s"
        valores.append(techada)

    if activa is not None:
        query += " AND activa = %s"
        valores.append(activa)

    if limit is not None:
        query += " LIMIT %s"
        valores.append(limit)

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