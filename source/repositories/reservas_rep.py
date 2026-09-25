from flask import request
from source.db import ejecutar_instruccion
from urllib.parse import urlencode

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

    resultados =  ejecutar_instruccion(query, tuple(filtros))

    if len(resultados)!=0 and resultados[0].get("error",False):
        return ("error_interno", resultados) #errores con el servidor, con mysql
    
    elif len(resultados)==0:
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
            
    links={
    "_first": {"href": f"{uri_params}?_limit={limit}&_offset={offset_first}&{query_params}"},
    "_prev": {"href": f"{uri_params}?_limit={limit}&_offset={offset_prev}&{query_params}"},
    "_next": {"href": f"{uri_params}?_limit={limit}&_offset={offset_next}&{query_params}"},
    "_last": {"href": f"{uri_params}?_limit={limit}&_offset={offset_last}&{query_params}"}
  }

    return links

def obtener_reserva_id_rep(reserva_id:int) -> tuple[str, list]:
    query="""SELECT id, socio_id, cancha_id, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total FROM reservas WHERE id=%s"""
    
    resultado=ejecutar_instruccion(query, (reserva_id,))

    if len(resultado)!=0 and resultado[0].get("error",False): #entra solo si esta el dict error interno
        return ("error_interno", resultado)
    
    elif len(resultado)==0:
        resultado=[{ "code": "No found", "message": "No se encontro algun resultado", "level": "error", "description": "NOT FOUND"}]
        return ("vacio", resultado)
    
    else:
        for registro in resultado:
            aplicar_formato(registro)
        return ("lleno", resultado)
