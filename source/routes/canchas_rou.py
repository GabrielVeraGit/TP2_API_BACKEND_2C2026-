from flask import Blueprint, request, jsonify
from source.services import canchas_service

canchas_bp = Blueprint("canchas",__name__)

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():

    id_deporte = request.args.get("id_deporte", type=int)
    nombre = request.args.get("nombre")
    techada = request.args.get("techada")
    activa = request.args.get("activa")

    print("ID DEPORTE RECIBIDO:", id_deporte)

    resultado = canchas_service.obtener_canchas(
        id_deporte=id_deporte,
        nombre=nombre,
        techada=techada,
        activa=activa
    )

    return jsonify(resultado), 200

@canchas_bp.route("/canchas", methods=["POST"])
def crear_cancha():
    data = request.get_json()

    cancha = canchas_service.crear_cancha(data)

    return jsonify({
        "id": cancha.id,
        "id_deporte": cancha.id_deporte,
        "nombre": cancha.nombre,
        "techada": cancha.techada,
        "activa": cancha.activa,
        "precio_hora": cancha.precio_hora
    }), 201


@canchas_bp.route("/canchas/<id>", methods=["GET"])
def obtener_cancha_id(id):
    print(f"obtener cancha especifica {id}")
    return "retornar cancha"

@canchas_bp.route("/canchas/<id>", methods=["PATCH"])
def actualizar_cancha_id(id):
    print("actualizar cancha especifica")
    return "retornar codigo exito/fallo"

@canchas_bp.route("/canchas/<id>", methods=["DELETE"])
def eliminar_cancha_id(id):
    print("eliminar cancha especifica")
    return "retornar codigo exito/fallo"

@canchas_bp.route("/canchas/disponibles", methods=["GET"])
def obtener_canchas_disponibles():
    print("obtener canchas disponibles")
    return "retornar canchas disponibles"