from flask import Blueprint, jsonify, request
from source.repositories.socios_rep import obtener_socios_rep
from source.repositories.socios_rep import crear_socio_rep
from source.repositories.socios_rep import obtener_socio
from source.repositories.socios_rep import modificar_socio_rep
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
def crear_socio():
    datos = request.get_json()

    nombre = datos.get("nombre")
    email = datos.get("email")
    activo = True

    crear_socio_rep(nombre, email, activo)

    print("datos recibidos: ", datos)
    return jsonify(datos), 201

@socios_bp.route("/socios/<id>", methods=["GET"])
def obtener_socio_id(id):
    socio = obtener_socio(id)
    if socio:
        return jsonify(socio), 200
    if not socio:
        return '', 204


@socios_bp.route("/socios/<id>", methods=["PATCH"])
def actualizar_socio_id(id):
    datos = request.get_json()

    modificar_socio_rep(id, datos)

    return '', 200