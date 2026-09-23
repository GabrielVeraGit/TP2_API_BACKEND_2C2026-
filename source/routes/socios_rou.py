from flask import Blueprint, request
from source.repositories.socios_rep import obtener_socios_rep

socios_bp=Blueprint("socios",__name__)

@socios_bp.route("/socios", methods=["GET"])
def obtener_socios():

    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)

    resultados = obtener_socios_rep(limit, offset)
    
    if not resultados:
        return '', 204

    return resultados, 200
    

@socios_bp.route("/socios", methods=["POST"])
def crear_reserva():
    print("crear socio")
    return "retorna codigo exito/fallo"

@socios_bp.route("/socios/<id>", methods=["GET"])
def obtener_socio_id(id):
    print("obtener socio especifico")
    return "retornar socio especifico"

@socios_bp.route("/socios/<id>", methods=["PATCH"])
def actualizar_socio_id(id):
    print("actualizar socio especifico")
    return "retorna codigo exito/fallo"