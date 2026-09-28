from flask import Blueprint, request, jsonify
from source.services import canchas_serv
from source.validators import canchas_val
from source.utils import construir_links_paginacion
from source.constants import PAGINATION_LIMIT_MAX, PAGINATION_LIMIT_MIN, PAGINATION_OFFSET_MIN

canchas_bp = Blueprint("canchas",__name__)

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():

    id_deporte = request.args.get("id_deporte", type=int)
    nombre = request.args.get("nombre")
    techada = request.args.get("techada")
    activa = request.args.get("activa")
    limit_str = request.args.get('_limit', 10)
    offset_str = request.args.get('_offset', 0)

    try:
        limit = int(limit_str)
        offset = int(offset_str)

    except ValueError:
        return "", 400

    if limit < PAGINATION_LIMIT_MIN or limit > PAGINATION_LIMIT_MAX:
        return "", 400
    
    if offset < PAGINATION_OFFSET_MIN:
        return "", 400

    if activa is not None:
        if activa.lower() == "true":
            activa = True
        elif activa.lower() == "false":
            activa = False
        else:
            return "", 400

    if techada is not None:
        if techada.lower() == "true":
            techada = True
        elif techada.lower() == "false":
            techada = False
        else:
            return "", 400
    

    canchas = canchas_serv.obtener_canchas(
        id_deporte=id_deporte,
        nombre=nombre,
        techada=techada,
        activa=activa,
        limit=limit,
        offset=offset
    )

    total = canchas_serv.contar_canchas(id_deporte, nombre, techada, activa)

    if not canchas:
        return '', 204

    links = construir_links_paginacion(total, limit, offset)

    respuesta = {
        "canchas" : canchas,
        "_links" : links
    }

    return jsonify(respuesta), 200

@canchas_bp.route("/canchas", methods=["POST"])
def crear_cancha():
    data = request.get_json()

    validator = canchas_val.validar_cancha(data)

    if validator[0] is None:
        return jsonify({"error": validator[1]}), 400

    cancha = canchas_serv.crear_cancha(data)

    if isinstance(cancha, tuple):
        return jsonify({"error": cancha[1]}), 400

    return jsonify(cancha), 201


@canchas_bp.route("/canchas/<int:id>", methods=["GET"])
def obtener_cancha_id(id):
    cancha = canchas_serv.cancha_por_id(id)

    if cancha is None:
        return jsonify({"error": "La cancha no existe"}), 404

    return jsonify(cancha), 200

@canchas_bp.route("/canchas/<int:id>", methods=["PATCH"])
def actualizar_cancha_id(id):

    data = request.get_json()

    validator = canchas_val.validar_update_cancha(data)

    if validator[0] is None:
        return jsonify({"error": validator[1]}), 400

    cancha = canchas_serv.update_cancha(id, data)

    if isinstance(cancha, tuple):
        return jsonify({"error": cancha[1]}), 404

    return jsonify(cancha), 200

@canchas_bp.route("/canchas/<int:id>", methods=["DELETE"])
def eliminar_cancha_id(id):
    cancha_id = canchas_serv.cancha_por_id(id)
    
    if cancha_id is None:
        return jsonify({"error": "La cancha no existe"}), 404
    
    cancha=canchas_serv.eliminar_cancha(id)
    if isinstance(cancha, tuple):
        return jsonify({"error": cancha[1]}), 409

    return "", 204

@canchas_bp.route("/canchas/disponibles", methods=["GET"])
def obtener_canchas_disponibles():

    id_deporte_str = request.args.get("id_deporte")

    if id_deporte_str is not None:
        try:
            id_deporte = int(id_deporte_str)
        except ValueError:
            return "", 400
    else:
        id_deporte = None

    limit_str = request.args.get("_limit", "10")
    offset_str = request.args.get("_offset", "0")

    try:
        limit = int(limit_str)
        offset = int(offset_str)
    except ValueError:
        return "", 400

    if limit < PAGINATION_LIMIT_MIN or limit > PAGINATION_LIMIT_MAX:
        return "", 400

    if offset < PAGINATION_OFFSET_MIN:
        return "", 400

    techada = request.args.get("techada")

    if techada is not None:
        if techada.lower() == "true":
            techada = True
        elif techada.lower() == "false":
            techada = False
        else:
            return "", 400

    data = {
        "fecha": request.args.get("fecha"),
        "hora_inicio": request.args.get("hora_inicio"),
        "hora_fin": request.args.get("hora_fin"),
        "id_deporte": id_deporte,
        "techada": techada,
        "limit": limit,
        "offset": offset
    }

    validator = canchas_val.validar_canchas_disponibles(data)

    if validator[0] is None:
        return jsonify({"error": validator[1]}), 400

    return canchas_serv.canchas_disponibles(data)