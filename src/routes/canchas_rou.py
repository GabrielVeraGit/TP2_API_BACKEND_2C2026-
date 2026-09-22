from flask import Blueprint, request, jsonify

canchas_bp = Blueprint("canchas",__name__)

canchas = [{
  "id_deporte": 1,
  "nombre": "futbol",
  "techada": true,
  "activa": true
},{
  "id_deporte": 2,
  "nombre": "natacion",
  "techada": true,
  "activa": false
}]

@canchas_bp.route("/canchas", methods=["GET"])
def obtener_canchas():
    
    id_deporte = request.args.get("id_deporte", type=int)
    nombre = request.args.get("nombre")
    techada = request.args.get("techada")
    activa = request.args.get("activa")

    for cancha in canchas:
        if (cancha.get("id_deporte") ==  id_deporte):
            return jsonify(user), 200

    return jsonify(users), 200

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