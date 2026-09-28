from flask import request
from source.db import ejecutar_instruccion
from urllib.parse import urlencode
from datetime import datetime

def aplicar_formato(registro:dict):
        #PARA EL FORMATO ISO 8601
        fecha_ini = registro['fecha_hora_inicio']
        fecha_fin = registro['fecha_hora_fin'] 

        registro['fecha_hora_inicio'] = f"{fecha_ini.strftime('%Y-%m-%dT%H:%M:%S.%f')}-03:00"
        registro['fecha_hora_fin'] = f"{fecha_fin.strftime('%Y-%m-%dT%H:%M:%S.%f')}-03:00"

        #PARA LOS PRECIOS DECIMAL(MYSQL) A int(PYTHON)
        if registro['precio_hora'] is not None:
            registro['precio_hora'] = int(registro['precio_hora']*100) 

        if registro['precio_total'] is not None:
            registro['precio_total'] = int(registro['precio_total']*100) 

def obtener_reservas_rep(filtros:list, query_filtros:str) -> list:
    
    query = """SELECT id, socio_id, cancha_id, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total FROM reservas"""
    query_paginacion=f"ORDER BY id ASC LIMIT %s OFFSET %s"

    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)
    
    if len(filtros) != 0: #hay filtros?
        query = f"{query} WHERE {query_filtros} {query_paginacion};"
    else:
        query = f"{query} {query_paginacion};"

    filtros.append(limit)
    filtros.append(offset)

    try:
        resultados =  ejecutar_instruccion(query, tuple(filtros))
    except Exception as error_interno:
        return ("error_interno", error_interno) 
    
    if len(resultados)==0:
        resultados=[{ "code": "No found", "message": "No se encontro algun resultado", "level": "error", "description": "NOT FOUND"}]
        return ("vacio", resultados)
    
    else:
        for registro in resultados:
            aplicar_formato(registro)
        return ("lleno", resultados)
    
def obtener_links_rep(filtros:list, query_filtros:str) -> dict:
    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)

    query="SELECT COUNT(*) AS total_general FROM reservas"

    if len(filtros) != 0: 
        query = f"{query} WHERE {query_filtros};"
        total = ejecutar_instruccion(query, tuple(filtros))
    else:
        query = f"{query};"
        total =  ejecutar_instruccion(query)

    total=total[0].get("total_general", 0)
    offset_first=0

    offset_prev=offset-limit
    if offset_prev < 0:
        offset_prev=0

    offset_next=offset+limit
    if offset_next >= total:
        offset_next = ((total - 1) // limit) * limit

    if total > 0:
        offset_last = ((total - 1) // limit) * limit
    else:
        offset_last = 0

    uri_params=request.base_url #http://localhost:5000/reservas
    
    query_params=request.args.to_dict() #los parametros como un dict

    query_params.pop("_limit", None)
    query_params.pop("_offset", None)

    query_params=urlencode(query_params) #reconstruirlos a query

    if len(query_params) !=0:
        query_params=f"&{query_params}"

    links={
    "_first": {"href": f"{uri_params}?_limit={limit}&_offset={offset_first}{query_params}"},
    "_prev": {"href": f"{uri_params}?_limit={limit}&_offset={offset_prev}{query_params}"},
    "_next": {"href": f"{uri_params}?_limit={limit}&_offset={offset_next}{query_params}"},
    "_last": {"href": f"{uri_params}?_limit={limit}&_offset={offset_last}{query_params}"}
  }

    return links

def obtener_reserva_id_rep(reserva_id:int) -> tuple[str, list]:
    query="""SELECT id, socio_id, cancha_id, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total FROM reservas WHERE id=%s"""

    try:
        resultado=ejecutar_instruccion(query, (reserva_id,))
    except Exception as error_interno:
        return ("error_interno", error_interno)
    
    if len(resultado)==0:
        resultado=[{ "code": "No found", "message": "No se encontro algun resultado", "level": "error", "description": "NOT FOUND"}]
        return ("vacio", resultado)
    
    else:
        for registro in resultado:
            aplicar_formato(registro)
        return (None, resultado)

def actualizar_reserva_rep(peticion_tipo:str, id:int):
    query="""UPDATE reservas SET estado = %s WHERE id = %s;"""
    try:
        ejecutar_instruccion(query,(peticion_tipo,id),True)
        return None, None
    except Exception as error_interno:
        return "error_interno", str(error_interno)



def verificar_existencia_actividad_rep(id:int, table:str):# si (existe y activo) -> true

    query = f"SELECT * FROM {table} WHERE id = %s;"

    try:
        resultado = ejecutar_instruccion(query, (id,))
        if not resultado:
            return "no_found", None
    except Exception as error_interno:
        return "error_interno", str(error_interno)

    if table == "socios" and resultado[0].get("activo") == 1:
        return "found_activo", resultado

    if table == "canchas" and resultado[0].get("activa") == 1:
        return "found_activo", resultado

    return "found_no_activo", None

def existe_interseccion_fechas_horas_rep(where:str, id_where:int, fh_inicio:datetime, fh_fin:datetime):
    estado="confirmada"
    query=f"SELECT COUNT(*) AS cant_interseccion FROM reservas WHERE {where}=%s AND estado=%s AND fecha_hora_inicio < %s AND fecha_hora_fin > %s;"
    try:
        resultado = ejecutar_instruccion(query, (id_where, estado, fh_fin.replace(tzinfo=None),fh_inicio.replace(tzinfo=None)))
        return None, resultado
    except Exception as error_interno:
        return "error_interno", str(error_interno)

def crear_reserva_rep(registro_socio:dict, registro_cancha:dict, fh_inicio:datetime, fh_fin:datetime):
    estado="confirmada"
    query=f"""INSERT INTO reservas (socio_id, cancha_id, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    
    precio_hora_centavos=registro_cancha["precio_hora"]
    horas_total=fh_fin.hour - fh_inicio.hour
    precio_total_centavos=precio_hora_centavos*horas_total

    valores=(registro_socio["id"], registro_cancha["id"], fh_inicio.replace(tzinfo=None), fh_fin.replace(tzinfo=None), estado, precio_hora_centavos, precio_total_centavos)

    try:
        ejecutar_instruccion(query, valores, True)
        return None, None
    except Exception as error_interno:
        return "error_interno", str(error_interno)