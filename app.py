from flask import Flask
from source.routes.deportes_rou import deportes_bp
from source.routes.canchas_rou import canchas_bp
from source.routes.socios_rou import socios_bp
from source.routes.reservas_rou import reservas_bp

app  = Flask(__name__)

app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(reservas_bp)


if __name__ == "__main__":
    app.run(port=6969, debug=False)
