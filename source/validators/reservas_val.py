from flask import request
from datetime import datetime, timezone, timedelta

def fecha_str_correcta(fecha:str) -> bool: #yyy-mm-dd
    FECHA_MINIMA=1800
    FECHA_MAXIMA=2027
    fecha_list = fecha.split(sep="-")
    if len(fecha_list) != 3 or False in list(map( lambda dato: dato.isdecimal(), fecha_list )):
        return False
    if len(fecha_list[0])!=4 or not (FECHA_MINIMA<int(fecha_list[0])<FECHA_MAXIMA):
        return False
    if not 1<=len(fecha_list[1])<=2 or not (1<=int(fecha_list[1])<=12):
        return False
    if not 1<=len(fecha_list[2])<=2 or not (1<=int(fecha_list[1])<=31):
        return False
    return True
def fechas_cooerentes(fecha_desde:str, fecha_hasta:str)-> bool: #desde(yyy-mm-dd) <= hasta(yyy-mm-dd)
    fecha_desde_list = fecha_desde.split(sep="-")
    fecha_hasta_list = fecha_hasta.split(sep="-")
    fecha_desde_list = list(map( lambda dato: int(dato), fecha_desde_list ))
    fecha_hasta_list = list(map( lambda dato: int(dato), fecha_hasta_list ))
    if not fecha_desde_list[0] <= fecha_hasta_list[0]:
        return False
    if not fecha_desde_list[1] <= fecha_hasta_list[1]:
        return False
    if not fecha_desde_list[2] <= fecha_hasta_list[2]:
        return False
    
    return True


def obtener_reservas_val():
    existe_error=None
    errores={"error": [{ "code": "ERROR_VALIDACION", "message": "QUERY PARAMS inválidos", "level": "error", "description": None}]} 
    
    id_cancha = request.args.get("id_cancha", default=None)
    if (id_cancha is not None) and (not id_cancha.isdecimal()):
        errores["error"][0]["description"]="El parametro id_cancha, debe ser un entero > 0"
        existe_error=errores
        return existe_error
    
    id_socio = request.args.get("id_socio", default=None)
    if (id_socio is not None) and (not id_socio.isdecimal()):
        errores["error"][0]["description"]="El parametro id_socio, debe ser un entero > 0"
        existe_error=errores
        return existe_error
    
    estado = request.args.get("estado", default=None)
    if (estado is not None) and (estado not in ("confirmada", "cancelada", "finalizada")):
        errores["error"][0]["description"]="El parametro 'estado' tine que ser (confirmada, cancelada, finalizada) "
        existe_error=errores
        return existe_error
    
    fecha_desde = request.args.get("fecha_desde", default=None)
    if fecha_desde is not None and not fecha_str_correcta(fecha_desde):
        errores["error"][0]["description"]="El parametro fecha_desde, formato incorrecto"
        existe_error=errores
        return existe_error

    fecha_hasta = request.args.get("fecha_hasta", default=None)
    if fecha_hasta is not None and not fecha_str_correcta(fecha_hasta):
        errores["error"][0]["description"]="El parametro fecha_hasta, formato incorrecto"
        existe_error=errores
        return existe_error
    
    if fecha_desde is not None and fecha_hasta is not None:
        if not fechas_cooerentes(fecha_desde, fecha_hasta):
            errores["error"][0]["description"]="Los parametros fecha_hasta y fecha_desde no son cooerentes"
            existe_error=errores
            return existe_error

    limit = request.args.get("_limit", default=10)
    #si es int, no mandaron limit en la request
    #si es str, lo mandaron en la request, y veo si tiene un caracter no numerico
    if (type(limit) is str) and (not limit.isdecimal()) or (int(limit)==0):
        errores["error"][0]["description"]="El parametro _limit, debe ser un entero > 0"
        existe_error=errores
        return existe_error

    offset = request.args.get("_offset", default=0)
    #si es int, no mandaron limit en la request
    #si es str, lo mandaron en la request, y veo si tiene un caracter no numerico
    if (type(offset) is str) and (not offset.isdecimal()):
        errores["error"][0]["description"]="El parametro _offset, debe ser un entero >= 0"
        existe_error=errores
        return existe_error

    return existe_error

def obtener_reserva_id_val(id:str):
    existe_error=None
    errores={"error": [{ "code": "ERROR_VALIDACION", "message": "URI PARAM inválido", "level": "error", "description": None}]} 
    if (id is not None) and (not id.isdecimal()):
        errores["error"][0]["description"]="solo se permiten id enteros positivos"
        existe_error=errores
        return existe_error


def actualizar_reserva_val(id:str):
    existe_error=None

    errores={"error": [{ "code": "ERROR_VALIDACION", "message": "REQUEST inválido", "level": "error", "description": None}]}

    existe_error_id=obtener_reserva_id_val(id)
    if existe_error_id is not None:
        existe_error=existe_error_id
        return existe_error_id

    body = request.get_json(silent=True)
    # Captura tanto el Content-Type incorrecto como el JSON (estructura) mal formado
    if body is None or not isinstance(body, dict):
        errores["error"][0]["description"]="Estructura JSON inválida o Content-Type debe ser application/json"
        existe_error=errores
        return existe_error
    
    tipo_estado_solicitado = body.get("estado", None)
    if tipo_estado_solicitado is None:
        errores["error"][0]["description"]="Camp 'estado' inexistente"
        existe_error=errores
        return existe_error

    if tipo_estado_solicitado not in ["confirmada", "finalizada", "cancelada"]:
        errores["error"][0]["description"]="Tipo de solicitud invalida, solo se permiten confirmada, finalizada y cancelada"
        existe_error=errores
        return existe_error
    
    return existe_error


def verificar_formato_ISO(fecha_hora:str, name:str, errores:dict) -> (dict | None):
    zona_horaria_GMT_3 = timezone(timedelta(hours=-3))
    try:
        fecha_hora=datetime.fromisoformat(fecha_hora)

        if fecha_hora.tzinfo == None or fecha_hora.tzinfo != zona_horaria_GMT_3:
            errores["error"][0]["description"]=f"{name} con zona horaria invalida"
            return errores
        
        if fecha_hora.minute != 0 or fecha_hora.second != 0 or fecha_hora.microsecond != 0:
            errores["error"][0]["description"]=f"{name} con una hora distinta de empunto"
            return errores
    except (ValueError, TypeError):
        errores["error"][0]["description"]=f"{name} debe tener un formato ISO 8601 valido"
        return errores
    
    return None

def crear_reserva_val()-> (dict | None):
    errores={"error": [{ "code": "ERROR_VALIDACION", "message": "REQUEST JSON inválido", "level": "error", "description": None}]}

    body = request.get_json(silent=True)

    if body is None or not isinstance(body, dict):
        errores["error"][0]["description"]="Estructura JSON inválida o Content-Type debe ser application/json"
        return errores
 
    id_socio=body.get("id_socio",None)
    try:
        if id_socio is None:
            errores["error"][0]["description"]="campo id_socio inexistente"
            return errores
        
        id_socio=int(id_socio)

        if id_socio<=0:
            errores["error"][0]["description"]="solo se permiten id_socio enteros positivos"
            return errores
    except (ValueError, TypeError):
        errores["error"][0]["description"]="id_socio solo admite tipo int()"
        return errores
    
    id_cancha=body.get("id_cancha",None)
    try:
        if id_cancha is None:
            errores["error"][0]["description"]="campo id_cancha inexistente"
            return errores
        
        id_cancha=int(id_cancha)

        if id_cancha<=0:
            errores["error"][0]["description"]="solo se permiten id_cancha enteros positivos"
            return errores
    except (ValueError, TypeError):
        errores["error"][0]["description"]="id_cancha solo admite tipo int()"
        return errores

    
    fecha_hora_inicio=body.get("fecha_hora_inicio", None)

    if fecha_hora_inicio is None:
        errores["error"][0]["description"]="campo fecha_hora_inicio inexistente"
        return errores
    
    resultado=verificar_formato_ISO(fecha_hora_inicio, "fecha_hora_inicio", errores)
    if resultado != None:
        return resultado


    fecha_hora_fin=body.get("fecha_hora_fin", None)

    if fecha_hora_fin is None:
        errores["error"][0]["description"]="campo fecha_hora_fin inexistente"
        return errores
    
    resultado=verificar_formato_ISO(fecha_hora_fin, "fecha_hora_fin", errores)
    if resultado != None:
        return resultado
    
    return None