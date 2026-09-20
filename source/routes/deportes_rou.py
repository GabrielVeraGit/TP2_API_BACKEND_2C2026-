from flask import Blueprint

deportes_bp = Blueprint("deportes",__name__)

@deportes_bp.route("/deportes", methods=["GET"])
def obtener_deportes():
    print("obtener deportes")
    return "retornar deportes"