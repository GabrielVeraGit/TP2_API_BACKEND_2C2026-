from flask import Blueprint, jsonify, request, jsonify
from source.repositories.socios_rep import obtener_socios_rep
from source.repositories.socios_rep import obtener_socio
socios_bp=Blueprint("socios",__name__)

@socios_bp.route("/socios", methods=["GET"])
def obtener_socios():


    nombre = request.args.get("nombre")
    activo = request.args.get("activo")

    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)

    if limit is None or limit < 1 or limit > 100:
        return "", 400

    if offset is None or offset < 0:
        return "", 400

    if activo is not None:
        if activo.lower() == "true":
            activo = True
        elif activo.lower() == "false":
            activo = False
        else:
            return "", 400

    resultados = obtener_socios_rep(nombre, activo, limit, offset)
    
    if not resultados:
        return '', 204

    return jsonify(resultados), 200
    

@socios_bp.route("/socios", methods=["POST"])
def crear_reserva():
    print("crear socio")
    return "retorna codigo exito/fallo"

@socios_bp.route("/socios/<id>", methods=["GET"])
def obtener_socio_id(id):
    socio = obtener_socio(id)
    return jsonify(socio), 200 if socio else 404


@socios_bp.route("/socios/<id>", methods=["PATCH"])
def actualizar_socio_id(id):
    print("actualizar socio especifico")
    return "retorna codigo exito/fallo"