from flask import Blueprint
from source.repositories.deportes_rep import obtener_deportes_rep

deportes_bp = Blueprint("deportes",__name__)

@deportes_bp.route("/deportes", methods=["GET"])
def obtener_deportes():

    resultados = obtener_deportes_rep()

    if not resultados:
        return {"message": "No se encontraron deportes."}, 204

    return resultados, 200