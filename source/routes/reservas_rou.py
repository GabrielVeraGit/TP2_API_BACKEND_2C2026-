from flask import Blueprint, jsonify
from source.validators.reservas_val import obtener_reservas_val, obtener_reserva_id_val
from source.services.reservas_serv import obtener_reservas_serv
from source.repositories.reservas_rep import obtener_reservas_rep, obtener_reserva_id_rep, obtener_links_rep
reservas_bp = Blueprint("reservas",__name__)

@reservas_bp.route("/reservas", methods=["GET"])
def obtener_reservas():

    existe_error=obtener_reservas_val() #verificamos q los datos esten limpios
    if  existe_error is not None:
        return jsonify(existe_error), 400 #Falta un dato obligatorio, el formato de la fecha es incorrecto, mandaron texto en vez de números? => 400 BAD REQUEST
    
    parametros_filtro, query_filtros=obtener_reservas_serv() #con los datos limpios, obtenemos los parametros_filtro y su query_filtros
    
    tipo, resultado = obtener_reservas_rep(parametros_filtro.copy(), query_filtros)

    if tipo == "error_interno":
        return jsonify({tipo: resultado}), 500 #errores con el servidor, con mysql

    elif tipo == "vacio":
        return jsonify({tipo: resultado}), 404 #La petición llegó limpia y con el formato perfecto, pero fuiste a buscarlo a MySQL y no encontramos ningún registro? => 404 Not Found
    
    else:
        links=obtener_links_rep(parametros_filtro.copy(), query_filtros)
        return jsonify({"reservas":resultado, "links":links}), 200

@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva():
    print("crear reserva")
    return "retorna codigo exito/fallo"

@reservas_bp.route("/reservas/<string:id>", methods=["GET"])
def obtener_reserva_id(id):

    existe_error=obtener_reserva_id_val(id)
    if existe_error is not None:
        return jsonify(existe_error), 400
    
    tipo, resultado = obtener_reserva_id_rep(id)

    if tipo == "error_interno":
        return jsonify({tipo: resultado}), 500
    elif tipo == "vacio":
        return jsonify({tipo: resultado}), 404
    else:
        return jsonify(resultado), 200

@reservas_bp.route("/reservas/<id>/estado", methods=["PUT"])
def actualizar_reservas(id):
    print("actualizar reserva")
    return "retornar reserva"