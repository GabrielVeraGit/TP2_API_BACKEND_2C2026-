from flask import Blueprint, request, jsonify
from source.services import canchas_serv
from source.validators import canchas_val

canchas_bp = Blueprint("canchas",__name__)

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():

    id_deporte = request.args.get("id_deporte", type=int)
    nombre = request.args.get("nombre")
    techada = request.args.get("techada")
    activa = request.args.get("activa")
    limite = request.args.get("_limit")

    resultado = canchas_serv.obtener_canchas(
        id_deporte=id_deporte,
        nombre=nombre,
        techada=techada,
        activa=activa,
        limit=limite
    )

    return jsonify(resultado), 200

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


@canchas_bp.route("/canchas/<id>", methods=["GET"])
def obtener_cancha_id(id):
    cancha = canchas_serv.cancha_por_id(id)

    if cancha is None:
        return jsonify({"error": "La cancha no existe"}), 404

    return jsonify(cancha), 200

@canchas_bp.route("/canchas/<id>", methods=["PATCH"])
def actualizar_cancha_id(id):
    data = request.get_json()
    cancha = canchas_serv.update_cancha(id, data)

    if isinstance(cancha, tuple):
        return jsonify({"error": cancha[1]}), 404

    return jsonify(cancha), 200

@canchas_bp.route("/canchas/<id>", methods=["DELETE"])
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
    print("obtener canchas disponibles")
    return "retornar canchas disponibles"