from flask import request
from datetime import datetime, timezone, timedelta
from source.repositories.reservas_rep import verificar_existencia_actividad_rep, existe_interseccion_fechas_horas_rep, crear_reserva_rep

def obtener_reservas_serv():
    filtros=[]
    query_filtros=[]

    id_cancha = request.args.get("id_cancha", default=None)
    if id_cancha != None:
        filtros.append(int(id_cancha))
        query_filtros.append("cancha_id = %s ")

    id_socio = request.args.get("id_socio", default=None)
    if id_socio != None:
        filtros.append(int(id_socio))
        query_filtros.append("socio_id = %s ")

    estado = request.args.get("estado", default=None)
    if estado != None:
        filtros.append(estado)
        query_filtros.append("estado = %s ")
    
    fecha_desde = request.args.get("fecha_desde", default=None)
    fecha_hasta = request.args.get("fecha_hasta", default=None)

    if fecha_desde != None and fecha_hasta != None :
        filtros.append(f"{fecha_desde} 00:00:00")
        filtros.append(f"{fecha_hasta} 23:59:59")
        query_filtros.append("fecha_hora_inicio BETWEEN %s AND %s")
    else:
        if fecha_desde != None:
            filtros.append(fecha_desde + " 00:00:00")
            query_filtros.append("fecha_hora_inicio >= %s")
        if fecha_hasta != None:
            filtros.append(fecha_hasta + " 23:59:59")
            query_filtros.append("fecha_hora_inicio <= %s")
    query= "AND ".join(query_filtros)

    return filtros, query

def actualizar_reserva_serv(registro:list[dict]) -> tuple:

    gmt_3 = timezone(timedelta(hours=-3))

    ahora = datetime.now(gmt_3) #class datetime
    reserva_inicio=registro[0].get("fecha_hora_inicio")#class str
    reserva_fin=registro[0].get("fecha_hora_fin")
    reserva_inicio=datetime.fromisoformat(reserva_inicio) #class datetime
    reserva_fin=datetime.fromisoformat(reserva_fin)

    body = request.get_json(silent=True)

    estado_solicitado = str(body.get("estado")).lower()
    estado_actual=str(registro[0].get("estado")).lower()

    errores=[{ "code": "ERROR_SERVICIOS", "message": "solicitud de cambio de estado RECHAZADO", "level": "error", "description": None}]
    
    if estado_actual != estado_solicitado:

        if estado_actual in ["finalizada", "cancelada"]: #Una transición no permitida, o solicitada fuera del momento permitido, producirá 409.
            errores[0]["description"]="transición no permitida (estado actual es finalizada o cancelada)"
            return "error", errores

        if estado_solicitado in ["finalizada", "cancelada"]:

            if estado_solicitado == "cancelada" and ahora < reserva_inicio:
                return "cancelada", None
            if estado_solicitado == "finalizada" and reserva_fin <= ahora:
                return "finalizada", None

            errores[0]["description"]="solicitud fuera del momento permitido"
            return "error", errores
    
    return "iguales", None


def verificar_coherencia__fechas_horas(fh_inicio:datetime, fh_fin:datetime, errores:dict) -> (list | None):
    MAX_RANGO_HORARIO=3
    HORA_MINIMA=8
    HORA_MAXIMA=23
    gmt_3 = timezone(timedelta(hours=-3))
    ahora = datetime.now(gmt_3)

    if fh_inicio <= ahora:
        errores["error"][0]["description"]="fecha_hora_inicio tiene que ser posterior a la actual"
        return errores
    if not (fh_inicio < fh_fin) or fh_inicio.date() != fh_fin.date():
        errores["error"][0]["description"]="fecha_hora_inicio y fecha_hora_fin, deben tener la misma fecha, pero horas disintas inicio < fin"
        return errores
    if (fh_fin.hour - fh_inicio.hour) > MAX_RANGO_HORARIO:
        errores["error"][0]["description"]="El tiempo de reserva permitido es de 1, 2 o 3 hrs"
        return errores
    if not (HORA_MINIMA<=fh_inicio.hour and fh_fin.hour<=HORA_MAXIMA):
        errores["error"][0]["description"]="El rango de reserva esta fuera del horario del Club"
        return errores
    
    return None

def verificar_existencia_actividad_serv(id:int, table:str, errores:dict):
    tipo, registro = verificar_existencia_actividad_rep(id,table)

    if tipo == "no_found":
        errores["error"][0]["description"]=f"id={id} de la tabla {table}, no found"
        return errores, None
    elif tipo == "error_interno":
        return {"error_interno": str(registro)}, None
    elif tipo == "found_no_activo":
        errores["error"][0]["description"]=f"id={id} de la tabla {table}, no activo para reservas"
        return errores, None
    return None, registro

def crear_reserva_serv():

    body = request.get_json(silent=True)

    id_socio=int(body.get("id_socio"))
    id_cancha=int(body.get("id_cancha"))
    fh_inicio=datetime.fromisoformat(body.get("fecha_hora_inicio"))
    fh_fin=datetime.fromisoformat(body.get("fecha_hora_fin"))

    errores={"error": [{ "code": "ERROR_SERVICIOS", "message": "REQUEST JSON inválido", "level": "error", "description": None}]}

    resultado=verificar_coherencia__fechas_horas(fh_inicio, fh_fin, errores)

    if resultado is not None:
        return resultado
    
    #verificar ids existan y si estan disponibles/activos para lograr una reserva
    aux, registro_socio=verificar_existencia_actividad_serv(id_socio, "socios", errores)
    if aux is not None:
        return aux
    
    aux, registro_cancha=verificar_existencia_actividad_serv(id_cancha, "canchas", errores)
    if aux is not None:
        return aux

    #ver que la cancha pedida no tenga intervalos que se solapen con la peticion
    aux, resultado=existe_interseccion_fechas_horas_rep("cancha_id", id_cancha, fh_inicio, fh_fin)
    if aux == "error_interno":
        return {"error_interno": str(resultado)}
    else:
        if resultado[0]["cant_interseccion"] != 0:
            errores["error"][0]["description"]=f"La id_cancha={id_cancha} cuenta con otras reservas que solapan el intervalo de tiempo pedido"
            return errores
        
    #ver que el socio no tenga otras reservas en el mismo intervalo en otras canchas
    aux, resultado=existe_interseccion_fechas_horas_rep("socio_id", id_socio, fh_inicio, fh_fin)
    if aux == "error_interno":
        return {"error_interno": str(resultado)}
    else:
        if resultado[0]["cant_interseccion"] != 0:
            errores["error"][0]["description"]=f"El id_socio={id_socio} cuenta con otras reservas en otras canchas, solapando el intervalo de tiempo pedido"
            return errores

    aux1, aux2 = crear_reserva_rep(registro_socio[0], registro_cancha[0], fh_inicio, fh_fin)
    if aux1 == "error_interno":
        return {"error_interno": aux2}
    
    return None