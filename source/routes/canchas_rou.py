from flask import Blueprint

canchas_bp = Blueprint("canchas",__name__)

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():
    print("obtener canchas")
    return "retornar canchas"

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