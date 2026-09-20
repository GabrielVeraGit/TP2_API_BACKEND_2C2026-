from flask import Blueprint

reservas_bp = Blueprint("reservas",__name__)

@reservas_bp.route("/reservas", methods=["GET"])
def obtener_reservas():
    print("obtener reservas")
    return "retornar reservas"

@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva():
    print("crear reserva")
    return "retorna codigo exito/fallo"

@reservas_bp.route("/reservas/<id>", methods=["GET"])
def obtener_reserva_id(id):
    print("obtener reserva especifica")
    return "retornar reserva especifica"

@reservas_bp.route("/reservas/<id>/estado", methods=["PUT"])
def actualizar_reservas(id):
    print("actualizar reserva")
    return "retornar reserva"