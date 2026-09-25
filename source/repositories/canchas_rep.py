from source.db import ejecutar_instruccion


def consultar_canchas(id_deporte=None, nombre=None, techada=None, activa=None):

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

    return {
        "id": resultado[0]["id"],
        "id_deporte": id_deporte,
        "nombre": nombre,
        "techada": techada,
        "activa": activa,
        "precio_hora": precio_hora
    }


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

    return ejecutar_instruccion(query, (id,))

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