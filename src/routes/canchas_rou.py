from flask import Blueprint, request, jsonify
from src.services import canchas_service

canchas_bp = Blueprint("canchas",__name__)

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():

    id_deporte = request.args.get("id_deporte", type=int)
    nombre = request.args.get("nombre")
    techada = request.args.get("techada")
    activa = request.args.get("activa")

    resultado = canchas_service.obtener_canchas(
        id_deporte=id_deporte,
        nombre=nombre,
        techada=techada,
        activa=activa
    )

    return jsonify(resultado), 200

@canchas_bp.route("/canchas", methods=["POST"])
def crear_cancha():
    print("crear cancha")
    return "retorna codigo exito/fallo"


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