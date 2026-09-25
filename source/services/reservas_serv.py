from flask import request



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