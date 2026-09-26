from flask import request
from datetime import datetime, timezone, timedelta

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