from flask import Blueprint, jsonify
from source.validators.reservas_val import obtener_reservas_val, obtener_reserva_id_val, actualizar_reserva_val, crear_reserva_val
from source.services.reservas_serv import obtener_reservas_serv, actualizar_reserva_serv, crear_reserva_serv
from source.repositories.reservas_rep import obtener_reservas_rep, obtener_reserva_id_rep, actualizar_reserva_rep, obtener_links_rep
reservas_bp = Blueprint("reservas",__name__)

@reservas_bp.route("/reservas", methods=["GET"])
def obtener_reservas():

    existe_error=obtener_reservas_val() #verificamos q los datos esten limpios
    if  existe_error is not None:
        return jsonify(existe_error), 400 #Falta un dato obligatorio, el formato de la fecha es incorrecto, mandaron texto en vez de números? => 400 BAD REQUEST
    
    parametros_filtro, query_filtros=obtener_reservas_serv() #con los datos limpios, obtenemos los parametros_filtro y su query_filtros
    
    tipo, registros = obtener_reservas_rep(parametros_filtro.copy(), query_filtros)

    if tipo == "error_interno":
        return jsonify({tipo: registros}), 500 #errores con el servidor, con mysql

    elif tipo == "vacio":
        return jsonify({tipo: registros}), 404 #La petición llegó limpia y con el formato perfecto, pero fuiste a buscarlo a MySQL y no encontramos ningún registro? => 404 Not Found
    
    else:
        links=obtener_links_rep(parametros_filtro.copy(), query_filtros)

        return jsonify({"reservas":registros, "links":links}), 200



@reservas_bp.route("/reservas/<string:id>", methods=["GET"])
def obtener_reserva_id(id:str):

    existe_error=obtener_reserva_id_val(id)
    if existe_error is not None:
        return jsonify(existe_error), 400
    
    tipo, registro = obtener_reserva_id_rep(int(id))

    if tipo == "error_interno":
        return jsonify({tipo: registro}), 500
    elif tipo == "vacio":
        return jsonify({tipo: registro}), 404
    else:
        return jsonify({"reserva":registro}), 200

@reservas_bp.route("/reservas/<string:id>/estado", methods=["PUT"])
def actualizar_reserva(id:str):

    existe_error=actualizar_reserva_val(id)
    if existe_error is not None:
        return jsonify(existe_error), 400

    
    tipo, registro = obtener_reserva_id_rep(int(id))
    if tipo == "error_interno":
        return jsonify({tipo: registro}), 500
    elif tipo == "vacio":
        return jsonify({tipo: registro}), 404
        
    
    tipo, dato = actualizar_reserva_serv(registro)
    if tipo == "iguales":
        return jsonify({"estados iguales, sin cambios" : registro}), 200
    
    elif tipo == "error":
        return jsonify({"error":dato}), 409

    else: #tipo == "cancelada" o "finalizada"

        tipo, respuesta=actualizar_reserva_rep(tipo, int(id))

        if tipo == "error_interno":
            return jsonify({"error_interno": respuesta}), 500
        else:

            tipo, registro = obtener_reserva_id_rep(int(id))
            if tipo == "error_interno":
                return jsonify({"error_interno": registro}), 500
            else:
                return jsonify({"reserva actualizada":registro}), 200

@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva():
    error_val = crear_reserva_val()
    if error_val is not None:
        return jsonify(error_val), 400
    
    error_serv = crear_reserva_serv()
    if error_serv is not None:
        return jsonify(error_serv), 400

    return jsonify({"exito": "Reserva creada"}), 201
