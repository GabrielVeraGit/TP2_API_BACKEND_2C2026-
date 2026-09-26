import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def obtener_db_conexion_manual():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection


def ejecutar_instruccion(
    query: str,
    valores: tuple = None,
    autocommit: bool = False
) -> list[dict]:

    resultados = []

    conexion = obtener_db_conexion_manual()
    cursor = conexion.cursor(dictionary=True, buffered=True)

    try:
        if valores is None:
            cursor.execute(query)
        else:
            cursor.execute(query, valores)

        if autocommit:
            conexion.commit()

            # Si fue un INSERT, obtenemos el ID generado
            if cursor.lastrowid:
                resultados = [{"id": cursor.lastrowid}]
        else:
            resultados = cursor.fetchall()

    except Exception as e:
        print(f"Error interno: {e}")
        raise

    finally:
        cursor.close()
        conexion.close()

    return resultados