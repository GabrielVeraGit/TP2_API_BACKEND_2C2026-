from flask import Blueprint, jsonify
from source.services import deportes_serv
from source.utils import construir_error_api

deportes_bp = Blueprint("deportes",__name__)

@deportes_bp.route("/deportes", methods=["GET"])
def obtener_deportes():
    try:
        deportes = deportes_serv.deportes_list()

        if not deportes:
            return "", 204

        return jsonify({
            "deportes" : deportes
        }), 200

    except Exception:
        return jsonify(
                    construir_error_api(
                        code="internal.db.error",
                        message="Error interno del servidor",
                        description="Ocurrio un error inesperado al procesar la solicitud"
                    )
                ), 500