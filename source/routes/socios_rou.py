from flask import Blueprint, jsonify, request
from source.services.socios_serv import crear_socio, obtener_socios, obtener_socio, modificar_socio
from source.utils import construir_error_api, construir_links_paginacion
from source.constants import PAGINATION_LIMIT_MAX, PAGINATION_LIMIT_MIN, PAGINATION_OFFSET_MIN

socios_bp = Blueprint("socios",__name__)

@socios_bp.route("/socios", methods=["GET"])
def obtener_socios_route():


    nombre = request.args.get("nombre")
    activo = request.args.get("activo")

    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)

    if limit is None or limit < PAGINATION_LIMIT_MIN or limit > PAGINATION_LIMIT_MAX:
        return "", 400

    if offset is None or offset < PAGINATION_OFFSET_MIN:
        return "", 400

    if activo is not None:
        if activo.lower() == "true":
            activo = True
        elif activo.lower() == "false":
            activo = False
        else:
            return "", 400

    socios, total = obtener_socios(nombre, activo, limit, offset)
    
    if not socios:
        return '', 204

    links = construir_links_paginacion(total, limit, offset)

    respuesta = {
        "socios" : socios,
        "_links" : links
    }

    return jsonify(respuesta), 200

@socios_bp.route("/socios", methods=["POST"])
def crear_socio_route():

    datos = request.get_json()

    try:
        nombre = datos.get("nombre")
        email = datos.get("email")

        crear_socio(nombre, email)

        return jsonify({
            "nombre": nombre,
            "email": email
        }), 201

    except ValueError as e:
        error = e.args[0]

        if error["errors"][0]["code"] == "conflict.email.exists":
            return jsonify(error), 409

        return jsonify(error), 400

    except Exception as e:
        print(f"Error interno: {e}")

        return jsonify(
            construir_error_api(
                code="internal.db.error",
                message="Error interno del servidor",
                description="Ocurrio un error inesperado al procesar la solicitud"
            )
        ), 500

@socios_bp.route("/socios/<id>", methods=["GET"])
def obtener_socio_id(id):
    socio = obtener_socio(id)

    if not socio:
        return '', 204

    return jsonify(socio), 200

@socios_bp.route("/socios/<id>", methods=["PATCH"])
def actualizar_socio_id(id):
    datos = request.get_json()

    try:
        modificar_socio(id, datos)

        return jsonify(obtener_socio(id)), 200

    except ValueError as e:
        return jsonify(e.args[0]), 400