from flask import Blueprint

socios_bp=Blueprint("socios",__name__)

@socios_bp.route("/socios", methods=["GET"])
def obtener_socios():
    print("obtener socios")
    return "retornar socios"

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