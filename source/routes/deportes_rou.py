from flask import Blueprint
from source.services import deportes_serv

deportes_bp = Blueprint("deportes",__name__)

@deportes_bp.route("/deportes", methods=["GET"])
def obtener_deportes():
    return deportes_serv.deportes_list()
    