from flask import Flask, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

from source.routes.deportes_rou import deportes_bp
from source.routes.canchas_rou import canchas_bp
from source.routes.socios_rou import socios_bp
from source.routes.reservas_rou import reservas_bp


app = Flask(__name__)

app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(reservas_bp)

SWAGGER_URL = "/swagger"
API_URL = "/docs/swagger.yaml"

swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL
)

app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)


@app.route("/")
def index():
    return redirect("/swagger/")


@app.route("/docs/swagger.yaml")
def swagger_yaml():
    return send_from_directory("docs", "swagger.yaml")


@app.route("/api/hello", methods=["GET"])
def hello():
    return {
        "message": "Hola"
    }


if __name__ == "__main__":
    app.run(port=6969, debug=True)